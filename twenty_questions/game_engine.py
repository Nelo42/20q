"""
Game Engine for the 20 Questions game.

Orchestrates all components and manages the game flow.
"""

from typing import Optional, List, Tuple, Callable, Dict
from dataclasses import dataclass, field
from enum import Enum

from .models import BeliefState, GameSession
from .knowledge_base import KnowledgeBase
from .belief_tracker import BeliefTracker
from .question_selector import QuestionSelector
from .weight_learner import WeightLearner
from .implications import ImplicationEngine


class GameState(Enum):
    """Possible states of the game."""
    NOT_STARTED = "not_started"
    ASKING_QUESTIONS = "asking_questions"
    MAKING_GUESS = "making_guess"
    LEARNING_NEW = "learning_new"
    GAME_OVER = "game_over"


@dataclass
class GameConfig:
    """Configuration for the game."""
    max_questions: int = 20
    guess_threshold: float = 0.5
    guess_margin: float = 0.15
    learning_rate: float = 0.1
    show_debug: bool = False


@dataclass
class TurnResult:
    """Result of a single turn."""
    question_number: int
    question_text: str
    attribute_id: str
    entropy_before: float
    entropy_after: float
    top_entities: List[Tuple[str, float]]
    confidence: float


class GameEngine:
    """
    Main game engine that orchestrates all components.

    Handles the game flow:
    1. Initialize with uniform beliefs
    2. Select and ask questions
    3. Update beliefs based on answers
    4. Decide when to guess
    5. Learn from outcomes
    """

    def __init__(
        self,
        data_dir: Optional[str] = None,
        config: Optional[GameConfig] = None
    ):
        """
        Initialize the game engine.

        Args:
            data_dir: Directory for data files
            config: Game configuration
        """
        self.config = config or GameConfig()

        # Initialize components
        self.kb = KnowledgeBase(data_dir)
        self.bt = BeliefTracker(self.kb)
        self.qs = QuestionSelector(self.kb, self.bt)
        self.wl = WeightLearner(self.kb, learning_rate=self.config.learning_rate)
        self.implication_engine = ImplicationEngine()

        # Game state
        self.state = GameState.NOT_STARTED
        self.beliefs: Optional[BeliefState] = None
        self.asked_questions: set = set()
        self.question_answers: List[Tuple[str, float]] = []
        self.current_question: int = 0
        self.guessed_entity: Optional[str] = None
        self.turn_history: List[TurnResult] = []

    def start_game(self) -> None:
        """Start a new game."""
        self.beliefs = self.bt.initialize_beliefs()
        self.asked_questions = set()
        self.question_answers = []
        self.current_question = 0
        self.guessed_entity = None
        self.turn_history = []
        self.state = GameState.ASKING_QUESTIONS

    def get_next_question(self) -> Optional[Tuple[str, str]]:
        """
        Get the next question to ask.

        Returns:
            Tuple of (attribute_id, question_text) or None if should guess
        """
        if self.state != GameState.ASKING_QUESTIONS:
            return None

        if self.beliefs is None:
            return None

        # Check if we should guess instead
        if self._should_guess():
            self.state = GameState.MAKING_GUESS
            return None

        # Check if we've reached max questions
        if self.current_question >= self.config.max_questions:
            self.state = GameState.MAKING_GUESS
            return None

        # Build known answers dict for implication filtering
        known_answers = self._get_known_answers()

        # Select best question (with hierarchy and implication awareness)
        attr_id = self.qs.select_best_question(
            self.beliefs,
            self.asked_questions,
            known_answers
        )

        if attr_id is None:
            # No more useful questions
            self.state = GameState.MAKING_GUESS
            return None

        question_text = self.qs.get_question_text(attr_id)
        return (attr_id, question_text)

    def _get_known_answers(self) -> Dict[str, float]:
        """
        Build a dictionary of known answers from the question history,
        including answers that are logically implied by previous answers.

        Returns:
            Dict mapping attribute_id -> answer_value
        """
        # Start with directly answered questions
        known = {attr_id: answer for attr_id, answer in self.question_answers}

        # Propagate implications to build complete set of known answers
        # We need to iterate until no new implications are found
        # Limit iterations to prevent infinite loops from circular implications
        max_iterations = 100
        iteration = 0
        changed = True
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            for attr_id, answer in list(known.items()):
                implications = self.implication_engine.get_implications(attr_id, answer)
                for implied_attr, implied_val in implications:
                    if implied_attr not in known:
                        known[implied_attr] = implied_val
                        changed = True

        return known

    def process_answer(self, attribute_id: str, answer: float) -> TurnResult:
        """
        Process user's answer to a question.

        Args:
            attribute_id: The attribute that was asked about
            answer: User's answer (1.0=yes, 0.0=no, 0.5=maybe)

        Returns:
            TurnResult with information about this turn
        """
        if self.beliefs is None:
            raise ValueError("Game not started")

        # Record entropy before
        entropy_before = self.bt.get_entropy(self.beliefs)

        # Update beliefs
        self.beliefs = self.bt.update_beliefs(self.beliefs, attribute_id, answer)

        # Record entropy after
        entropy_after = self.bt.get_entropy(self.beliefs)

        # Track question
        self.asked_questions.add(attribute_id)
        self.question_answers.append((attribute_id, answer))
        self.current_question += 1

        # Get current state info
        top_entities = self.beliefs.get_top_entities(5)
        confidence = self.bt.get_confidence(self.beliefs)

        # Create turn result
        result = TurnResult(
            question_number=self.current_question,
            question_text=self.qs.get_question_text(attribute_id) or "",
            attribute_id=attribute_id,
            entropy_before=entropy_before,
            entropy_after=entropy_after,
            top_entities=[(eid, prob) for eid, prob in top_entities],
            confidence=confidence
        )

        self.turn_history.append(result)

        return result

    def _should_guess(self) -> bool:
        """Check if we should make a guess now."""
        if self.beliefs is None:
            return False

        return self.qs.should_guess(
            self.beliefs,
            threshold=self.config.guess_threshold,
            min_margin=self.config.guess_margin
        )

    def get_guess(self) -> Optional[Tuple[str, str, float]]:
        """
        Get the system's guess.

        Returns:
            Tuple of (entity_id, entity_name, confidence) or None
        """
        if self.beliefs is None:
            return None

        entity_id, confidence = self.beliefs.get_max_probability()
        if entity_id is None:
            return None

        entity = self.kb.get_entity(entity_id)
        if entity is None:
            return None

        self.guessed_entity = entity_id
        return (entity_id, entity.name, confidence)

    def process_guess_result(self, was_correct: bool, actual_entity_name: Optional[str] = None) -> None:
        """
        Process the result of the guess.

        Args:
            was_correct: Whether the guess was correct
            actual_entity_name: If wrong, the name of the actual entity
        """
        if self.guessed_entity is None:
            return

        if was_correct:
            # Reinforce correct guess
            self.wl.update_from_session(
                self.guessed_entity,
                self.question_answers,
                was_correct_guess=True
            )
            self.state = GameState.GAME_OVER
        else:
            # Handle wrong guess
            if actual_entity_name:
                # Check if entity exists
                actual_entity = self._find_entity_by_name(actual_entity_name)

                if actual_entity:
                    # Entity exists - adjust weights to distinguish
                    self.wl.adjust_weights_for_confusion(
                        self.guessed_entity,
                        actual_entity.id,
                        self.question_answers
                    )
                    self.state = GameState.GAME_OVER
                else:
                    # New entity - need to learn it
                    self.state = GameState.LEARNING_NEW
            else:
                self.state = GameState.LEARNING_NEW

    def _find_entity_by_name(self, name: str):
        """Find an entity by name (case-insensitive).

        Uses a multi-pass matching strategy:
        1. Exact match (after normalizing articles)
        2. Core noun match (removing 'a', 'an', 'the')
        """
        def normalize_name(n: str) -> str:
            """Remove leading articles and normalize."""
            n = n.lower().strip()
            for article in ("a ", "an ", "the "):
                if n.startswith(article):
                    n = n[len(article):]
            return n

        name_normalized = normalize_name(name)

        # Pass 1: Exact match after normalization
        for entity in self.kb.get_all_entities():
            entity_normalized = normalize_name(entity.name)
            if name_normalized == entity_normalized:
                return entity

        # Pass 2: Check if the normalized name matches as a whole word
        # (prevents "cat" matching "catfish")
        for entity in self.kb.get_all_entities():
            entity_normalized = normalize_name(entity.name)
            # Split into words and check for whole word match
            entity_words = entity_normalized.split()
            name_words = name_normalized.split()
            if name_words == entity_words:
                return entity
            # Also check if all name words appear in entity words
            if all(word in entity_words for word in name_words):
                return entity

        return None

    def learn_new_entity(
        self,
        name: str,
        distinguishing_question: Optional[str] = None,
        distinguishing_answer: Optional[float] = None
    ) -> str:
        """
        Learn a new entity from a failed guess.

        Args:
            name: Name of the new entity
            distinguishing_question: Optional question to distinguish it
            distinguishing_answer: Answer to the distinguishing question

        Returns:
            ID of the newly created entity
        """
        new_entity = self.wl.learn_new_entity(
            name=name,
            question_answers=self.question_answers,
            distinguishing_question=distinguishing_question,
            distinguishing_answer=distinguishing_answer
        )

        self.state = GameState.GAME_OVER
        return new_entity.id

    def get_game_summary(self) -> dict:
        """
        Get a summary of the completed game.

        Returns:
            Dictionary with game statistics
        """
        return {
            "questions_asked": self.current_question,
            "guessed_entity": self.guessed_entity,
            "final_confidence": self.bt.get_confidence(self.beliefs) if self.beliefs else 0,
            "final_entropy": self.bt.get_entropy(self.beliefs) if self.beliefs else 0,
            "turn_history": [
                {
                    "question": t.question_text,
                    "entropy_reduction": t.entropy_before - t.entropy_after
                }
                for t in self.turn_history
            ]
        }

    def get_stats(self) -> dict:
        """Get global learning statistics."""
        return self.wl.get_global_stats()

    def get_current_state(self) -> dict:
        """
        Get the current game state for display.

        Returns:
            Dictionary with current state information
        """
        if self.beliefs is None:
            return {"state": self.state.value}

        top_entities = self.beliefs.get_top_entities(5)

        return {
            "state": self.state.value,
            "question_number": self.current_question,
            "entropy": self.bt.get_entropy(self.beliefs),
            "confidence": self.bt.get_confidence(self.beliefs),
            "top_entities": [
                {
                    "id": eid,
                    "name": self.kb.get_entity(eid).name if self.kb.get_entity(eid) else eid,
                    "probability": prob
                }
                for eid, prob in top_entities
            ]
        }
