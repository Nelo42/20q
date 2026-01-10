"""
Question Selector for the 20 Questions game.

Implements entropy-based question selection to maximize information gain.
"""

import numpy as np
from typing import Set, Optional, List, Tuple
from .models import BeliefState
from .knowledge_base import KnowledgeBase
from .belief_tracker import BeliefTracker


class QuestionSelector:
    """
    Selects optimal questions using information gain (entropy reduction).

    The best question is the one that maximizes:
    Information Gain = H(current) - E[H(after_answer)]

    Where E[H(after)] = P(yes)*H(if_yes) + P(no)*H(if_no)
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        belief_tracker: BeliefTracker,
        min_info_gain: float = 0.001
    ):
        """
        Initialize the question selector.

        Args:
            knowledge_base: The knowledge base to use
            belief_tracker: The belief tracker for simulating updates
            min_info_gain: Minimum information gain to consider a question
        """
        self.kb = knowledge_base
        self.bt = belief_tracker
        self.min_info_gain = min_info_gain

    def select_best_question(
        self,
        beliefs: BeliefState,
        asked_questions: Set[str]
    ) -> Optional[str]:
        """
        Select the question that maximizes expected information gain.

        Args:
            beliefs: Current belief state
            asked_questions: Set of attribute IDs already asked

        Returns:
            Attribute ID of the best question, or None if no good questions remain
        """
        best_question = None
        best_gain = -float('inf')

        current_entropy = self.bt.get_entropy(beliefs)

        for attr in self.kb.get_all_attributes():
            if attr.id in asked_questions:
                continue

            info_gain = self._calculate_info_gain(
                beliefs, attr.id, current_entropy
            )

            if info_gain > best_gain and info_gain >= self.min_info_gain:
                best_gain = info_gain
                best_question = attr.id

        return best_question

    def _calculate_info_gain(
        self,
        beliefs: BeliefState,
        attribute_id: str,
        current_entropy: float
    ) -> float:
        """
        Calculate expected information gain for a question.

        IG = H(current) - E[H(after)]
           = H(current) - [P(yes)*H(if_yes) + P(no)*H(if_no) + P(maybe)*H(if_maybe)]

        Args:
            beliefs: Current belief state
            attribute_id: The attribute/question to evaluate
            current_entropy: Pre-calculated current entropy

        Returns:
            Expected information gain
        """
        # Estimate P(yes) across all entities weighted by belief
        p_yes = self.bt.get_answer_probability(beliefs, attribute_id)
        p_no = 1.0 - p_yes

        # Avoid division by zero and handle edge cases
        if p_yes < 0.01 or p_no < 0.01:
            # Question is nearly deterministic, might still be useful
            # but calculate carefully
            p_yes = max(0.01, min(0.99, p_yes))
            p_no = 1.0 - p_yes

        # Simulate beliefs after each possible answer
        beliefs_if_yes = self.bt.simulate_answer(beliefs, attribute_id, 1.0)
        beliefs_if_no = self.bt.simulate_answer(beliefs, attribute_id, 0.0)

        # Calculate entropy for each outcome
        entropy_if_yes = self.bt.get_entropy(beliefs_if_yes)
        entropy_if_no = self.bt.get_entropy(beliefs_if_no)

        # Expected entropy after asking this question
        expected_entropy = p_yes * entropy_if_yes + p_no * entropy_if_no

        # Information gain is reduction in entropy
        info_gain = current_entropy - expected_entropy

        return info_gain

    def get_top_questions(
        self,
        beliefs: BeliefState,
        asked_questions: Set[str],
        n: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Get the top N questions by information gain.

        Args:
            beliefs: Current belief state
            asked_questions: Set of attribute IDs already asked
            n: Number of questions to return

        Returns:
            List of (attribute_id, info_gain) tuples, sorted by gain descending
        """
        current_entropy = self.bt.get_entropy(beliefs)
        gains = []

        for attr in self.kb.get_all_attributes():
            if attr.id in asked_questions:
                continue

            info_gain = self._calculate_info_gain(
                beliefs, attr.id, current_entropy
            )
            gains.append((attr.id, info_gain))

        # Sort by information gain descending
        gains.sort(key=lambda x: x[1], reverse=True)

        return gains[:n]

    def should_guess(
        self,
        beliefs: BeliefState,
        threshold: float = 0.5,
        min_margin: float = 0.15
    ) -> bool:
        """
        Determine if we should make a guess instead of asking another question.

        Args:
            beliefs: Current belief state
            threshold: Minimum probability for top entity to trigger guess
            min_margin: Minimum margin over second-best entity

        Returns:
            True if we should guess, False if we should ask another question
        """
        top_entities = beliefs.get_top_entities(2)

        if len(top_entities) == 0:
            return False

        if len(top_entities) == 1:
            return top_entities[0][1] >= threshold

        top_prob = top_entities[0][1]
        second_prob = top_entities[1][1]

        # Guess if top entity is above threshold AND has sufficient margin
        return top_prob >= threshold and (top_prob - second_prob) >= min_margin

    def get_question_text(self, attribute_id: str) -> Optional[str]:
        """
        Get the question text for an attribute.

        Args:
            attribute_id: The attribute ID

        Returns:
            Question text or None if not found
        """
        attr = self.kb.get_attribute(attribute_id)
        return attr.question if attr else None
