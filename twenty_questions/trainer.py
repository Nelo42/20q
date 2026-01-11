"""
Training and Simulation System for the 20 Questions game.

Runs thousands of simulated games to:
1. Optimize question selection strategy
2. Learn optimal attribute weights
3. Test coverage and accuracy
4. Identify weak points in the knowledge base
"""

import random
import json
import math
import os
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import time

from .models import Entity, BeliefState
from .knowledge_base import KnowledgeBase
from .belief_tracker import BeliefTracker
from .question_selector import QuestionSelector


@dataclass
class SimulationResult:
    """Result of a single simulated game."""
    target_entity_id: str
    target_entity_name: str
    guessed_correctly: bool
    num_questions: int
    final_rank: int  # Rank of target in final beliefs (1 = top)
    final_probability: float
    questions_asked: List[str]
    entropy_progression: List[float]


@dataclass
class TrainingStats:
    """Aggregate statistics from training runs."""
    total_games: int = 0
    correct_guesses: int = 0
    total_questions: int = 0
    avg_questions_when_correct: float = 0.0
    avg_questions_overall: float = 0.0
    accuracy: float = 0.0

    # Per-category stats
    category_stats: Dict[str, Dict] = field(default_factory=dict)

    # Question effectiveness
    question_info_gains: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    question_usage_count: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    # Entity difficulty
    entity_attempts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    entity_successes: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    entity_avg_questions: Dict[str, List[int]] = field(default_factory=lambda: defaultdict(list))

    # Failure analysis
    failed_entities: List[str] = field(default_factory=list)
    confusion_pairs: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))


class Trainer:
    """
    Trains and optimizes the 20 Questions system through simulation.
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        max_questions: int = 20,
        guess_threshold: float = 0.5,
        guess_margin: float = 0.15,
        use_popularity_prior: bool = True
    ):
        """
        Initialize the trainer.

        Args:
            knowledge_base: The knowledge base to use
            max_questions: Maximum questions per game
            guess_threshold: Confidence threshold to make a guess
            guess_margin: Required margin over second-best
            use_popularity_prior: Whether to use popularity-weighted priors
        """
        self.kb = knowledge_base
        self.max_questions = max_questions
        self.guess_threshold = guess_threshold
        self.guess_margin = guess_margin
        self.use_popularity_prior = use_popularity_prior

        self.bt = BeliefTracker(knowledge_base)
        self.qs = QuestionSelector(knowledge_base, self.bt)

        self.stats = TrainingStats()
        self.results: List[SimulationResult] = []

    def run_simulation(
        self,
        num_games: int = 1000,
        weighted_selection: bool = True,
        verbose: bool = False,
        progress_interval: int = 100
    ) -> TrainingStats:
        """
        Run multiple simulated games.

        Args:
            num_games: Number of games to simulate
            weighted_selection: Weight entity selection by popularity
            verbose: Print detailed progress
            progress_interval: How often to print progress

        Returns:
            Aggregate training statistics
        """
        self.stats = TrainingStats()
        self.results = []

        entities = self.kb.get_all_entities()
        if not entities:
            print("No entities in knowledge base!")
            return self.stats

        # Calculate selection weights based on popularity
        if weighted_selection:
            weights = self._calculate_selection_weights(entities)
        else:
            weights = [1.0 / len(entities)] * len(entities)

        start_time = time.time()

        for i in range(num_games):
            # Select target entity (weighted by popularity)
            target = random.choices(entities, weights=weights, k=1)[0]

            # Run single game simulation
            result = self._simulate_single_game(target)
            self.results.append(result)

            # Update stats
            self._update_stats(result)

            if verbose and (i + 1) % progress_interval == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                eta = (num_games - i - 1) / rate if rate > 0 else 0
                print(f"Progress: {i+1}/{num_games} ({100*(i+1)/num_games:.1f}%) "
                      f"Accuracy: {100*self.stats.accuracy:.1f}% "
                      f"Avg Questions: {self.stats.avg_questions_overall:.1f} "
                      f"ETA: {eta:.0f}s")

        # Finalize statistics
        self._finalize_stats()

        return self.stats

    def _calculate_selection_weights(self, entities: List[Entity]) -> List[float]:
        """Calculate selection weights based on popularity rank."""
        weights = []
        for entity in entities:
            # Get popularity rank (lower = more popular)
            rank = getattr(entity, 'popularity_rank', 500)
            # Convert to weight: more popular = higher weight
            # Using inverse square root for smoother distribution
            weight = 1.0 / math.sqrt(rank + 1)
            weights.append(weight)

        # Normalize
        total = sum(weights)
        return [w / total for w in weights]

    def _simulate_single_game(self, target: Entity) -> SimulationResult:
        """
        Simulate a single game with the given target entity.

        Args:
            target: The entity the "player" is thinking of

        Returns:
            Result of the simulation
        """
        # Initialize beliefs (with popularity prior if enabled)
        if self.use_popularity_prior:
            beliefs = self._initialize_with_popularity_prior()
        else:
            beliefs = self.bt.initialize_beliefs()

        asked_questions: Set[str] = set()
        known_answers: Dict[str, float] = {}
        questions_asked: List[str] = []
        entropy_progression: List[float] = [self.bt.get_entropy(beliefs)]

        num_questions = 0
        guessed_correctly = False

        for turn in range(self.max_questions):
            # Check if we should guess
            if self.qs.should_guess(beliefs, self.guess_threshold, self.guess_margin):
                top_entity = self.bt.get_top_entity(beliefs)
                guessed_correctly = (top_entity == target.id)
                break

            # Select best question
            question_id = self.qs.select_best_question(
                beliefs, asked_questions, known_answers
            )

            if question_id is None:
                # No more questions, make a guess
                top_entity = self.bt.get_top_entity(beliefs)
                guessed_correctly = (top_entity == target.id)
                break

            # "Answer" the question based on target's attributes
            answer = self._get_target_answer(target, question_id)

            # Update tracking
            asked_questions.add(question_id)
            known_answers[question_id] = answer
            questions_asked.append(question_id)
            num_questions += 1

            # Add implied answers to known_answers for proper question filtering
            # Use recursive propagation to get ALL determined attributes
            from .implications import ImplicationEngine
            impl_engine = ImplicationEngine()

            # First add direct implications
            implications = impl_engine.get_implications(question_id, answer)
            for implied_attr, implied_val in implications:
                known_answers[implied_attr] = implied_val

            # Then recursively propagate to get all determined attributes
            all_determined = impl_engine.get_all_determined_attributes(known_answers)
            known_answers.update(all_determined)

            # Track question usage
            self.stats.question_usage_count[question_id] += 1

            # Calculate and track info gain
            current_entropy = self.bt.get_entropy(beliefs)

            # Update beliefs
            beliefs = self.bt.update_beliefs(beliefs, question_id, answer)

            new_entropy = self.bt.get_entropy(beliefs)
            info_gain = current_entropy - new_entropy
            self.stats.question_info_gains[question_id].append(info_gain)

            entropy_progression.append(new_entropy)

        # If we exhausted questions, check final beliefs
        if num_questions == self.max_questions:
            top_entity = self.bt.get_top_entity(beliefs)
            guessed_correctly = (top_entity == target.id)

        # Calculate final rank and probability
        final_rank = self._get_entity_rank(beliefs, target.id)
        final_probability = beliefs.probabilities.get(target.id, 0.0)

        # Track confusion if failed
        if not guessed_correctly:
            top_entity = self.bt.get_top_entity(beliefs)
            if top_entity:
                self.stats.confusion_pairs[target.id].append(top_entity)

        return SimulationResult(
            target_entity_id=target.id,
            target_entity_name=target.name,
            guessed_correctly=guessed_correctly,
            num_questions=num_questions,
            final_rank=final_rank,
            final_probability=final_probability,
            questions_asked=questions_asked,
            entropy_progression=entropy_progression
        )

    def _initialize_with_popularity_prior(self) -> BeliefState:
        """Initialize beliefs weighted by entity popularity."""
        entities = self.kb.get_all_entities()
        probs = {}

        for entity in entities:
            rank = getattr(entity, 'popularity_rank', 500)
            # More popular items get higher prior probability
            # Using inverse of rank with softening
            probs[entity.id] = 1.0 / math.log2(rank + 2)

        # Normalize
        total = sum(probs.values())
        for eid in probs:
            probs[eid] /= total

        return BeliefState(probabilities=probs)

    def _get_target_answer(self, target: Entity, attribute_id: str) -> float:
        """
        Get the target's answer for a question.

        Simulates a real player's answer based on the entity's attributes.
        Uses implication system to infer answers for unset attributes.
        """
        # First check if answer can be inferred from implications
        from .implications import ImplicationEngine
        impl_engine = ImplicationEngine()

        # Build known attributes from the target entity
        known_attrs = {k: v for k, v in target.attributes.items() if v >= 0.8 or v <= 0.2}

        # Check if this attribute is determined by implications
        is_det, implied_val = impl_engine.is_already_determined(attribute_id, known_attrs)
        if is_det:
            return implied_val

        # Also check recursively determined attributes
        all_determined = impl_engine.get_all_determined_attributes(known_attrs)
        if attribute_id in all_determined:
            implied_val = all_determined[attribute_id]
            if implied_val >= 0.8:
                return 1.0
            elif implied_val <= 0.2:
                return 0.0

        # If not implied, use the entity's direct attribute
        prob = target.get_attribute_probability(attribute_id)

        # Convert probability to yes/no/maybe
        if prob >= 0.8:
            return 1.0  # Yes
        elif prob <= 0.2:
            return 0.0  # No
        else:
            # For uncertain attributes, be more conservative
            # Default to 0.5 (maybe) to avoid false answers
            return 0.5

    def _get_entity_rank(self, beliefs: BeliefState, entity_id: str) -> int:
        """Get the rank of an entity in the belief distribution."""
        sorted_entities = beliefs.get_top_entities(len(beliefs.probabilities))
        for rank, (eid, _) in enumerate(sorted_entities, 1):
            if eid == entity_id:
                return rank
        return len(sorted_entities) + 1

    def _update_stats(self, result: SimulationResult):
        """Update aggregate statistics with a game result."""
        self.stats.total_games += 1
        self.stats.total_questions += result.num_questions

        if result.guessed_correctly:
            self.stats.correct_guesses += 1

        self.stats.accuracy = self.stats.correct_guesses / self.stats.total_games
        self.stats.avg_questions_overall = self.stats.total_questions / self.stats.total_games

        # Per-entity tracking
        self.stats.entity_attempts[result.target_entity_id] += 1
        if result.guessed_correctly:
            self.stats.entity_successes[result.target_entity_id] += 1
        self.stats.entity_avg_questions[result.target_entity_id].append(result.num_questions)

        if not result.guessed_correctly:
            if result.target_entity_id not in self.stats.failed_entities:
                self.stats.failed_entities.append(result.target_entity_id)

    def _finalize_stats(self):
        """Finalize statistics after all games."""
        # Calculate avg questions when correct
        correct_questions = [
            r.num_questions for r in self.results if r.guessed_correctly
        ]
        if correct_questions:
            self.stats.avg_questions_when_correct = sum(correct_questions) / len(correct_questions)

        # Categorize entities and calculate per-category stats
        for entity in self.kb.get_all_entities():
            category = self._get_entity_category(entity)
            if category not in self.stats.category_stats:
                self.stats.category_stats[category] = {
                    'total': 0, 'correct': 0, 'questions': []
                }

            attempts = self.stats.entity_attempts.get(entity.id, 0)
            successes = self.stats.entity_successes.get(entity.id, 0)
            questions = self.stats.entity_avg_questions.get(entity.id, [])

            self.stats.category_stats[category]['total'] += attempts
            self.stats.category_stats[category]['correct'] += successes
            self.stats.category_stats[category]['questions'].extend(questions)

    def _get_entity_category(self, entity: Entity) -> str:
        """Determine the high-level category of an entity."""
        attrs = entity.attributes
        if attrs.get('is_animal', 0) > 0.5:
            return 'animal'
        elif attrs.get('is_vegetable', 0) > 0.5:
            return 'plant'
        elif attrs.get('is_mineral', 0) > 0.5:
            return 'object'
        return 'unknown'

    def get_question_effectiveness(self) -> List[Tuple[str, float, int]]:
        """
        Get questions ranked by average information gain.

        Returns:
            List of (question_id, avg_info_gain, usage_count) tuples
        """
        effectiveness = []
        for qid, gains in self.stats.question_info_gains.items():
            if gains:
                avg_gain = sum(gains) / len(gains)
                count = self.stats.question_usage_count[qid]
                effectiveness.append((qid, avg_gain, count))

        effectiveness.sort(key=lambda x: x[1], reverse=True)
        return effectiveness

    def get_difficult_entities(self) -> List[Tuple[str, float, int]]:
        """
        Get entities ranked by difficulty (lowest success rate).

        Returns:
            List of (entity_id, success_rate, attempts) tuples
        """
        difficulties = []
        for eid, attempts in self.stats.entity_attempts.items():
            if attempts >= 3:  # Need minimum attempts
                successes = self.stats.entity_successes.get(eid, 0)
                rate = successes / attempts
                difficulties.append((eid, rate, attempts))

        difficulties.sort(key=lambda x: x[1])
        return difficulties

    def get_confusion_matrix(self) -> Dict[str, List[Tuple[str, int]]]:
        """
        Get confusion analysis - what entities get confused with what.

        Returns:
            Dict mapping entity_id to list of (confused_with_id, count) tuples
        """
        confusion = {}
        for eid, confused_list in self.stats.confusion_pairs.items():
            counts = defaultdict(int)
            for confused_with in confused_list:
                counts[confused_with] += 1
            confusion[eid] = sorted(
                counts.items(), key=lambda x: x[1], reverse=True
            )
        return confusion

    def suggest_improvements(self) -> Dict:
        """
        Analyze results and suggest improvements.

        Returns:
            Dictionary with improvement suggestions
        """
        suggestions = {
            'add_questions': [],
            'improve_entities': [],
            'remove_questions': [],
            'adjust_hierarchy': []
        }

        # Find ineffective questions (low info gain)
        for qid, avg_gain, count in self.get_question_effectiveness():
            if count > 10 and avg_gain < 0.1:
                suggestions['remove_questions'].append({
                    'question': qid,
                    'avg_gain': avg_gain,
                    'reason': 'Low average information gain'
                })

        # Find difficult entities
        for eid, rate, attempts in self.get_difficult_entities():
            if rate < 0.5:  # Less than 50% success
                # Find what it's confused with
                confused_with = self.stats.confusion_pairs.get(eid, [])
                suggestions['improve_entities'].append({
                    'entity': eid,
                    'success_rate': rate,
                    'confused_with': confused_with[:3],
                    'reason': 'Low success rate, needs distinguishing attributes'
                })

        # Analyze category performance
        for category, stats in self.stats.category_stats.items():
            if stats['total'] > 0:
                rate = stats['correct'] / stats['total']
                if rate < 0.7:
                    suggestions['adjust_hierarchy'].append({
                        'category': category,
                        'success_rate': rate,
                        'reason': 'Category has low success rate'
                    })

        return suggestions

    def save_results(self, filepath: str):
        """Save training results to a file."""
        data = {
            'stats': {
                'total_games': self.stats.total_games,
                'correct_guesses': self.stats.correct_guesses,
                'accuracy': self.stats.accuracy,
                'avg_questions_overall': self.stats.avg_questions_overall,
                'avg_questions_when_correct': self.stats.avg_questions_when_correct,
                'category_stats': {
                    cat: {
                        'total': s['total'],
                        'correct': s['correct'],
                        'accuracy': s['correct'] / s['total'] if s['total'] > 0 else 0,
                        'avg_questions': sum(s['questions']) / len(s['questions']) if s['questions'] else 0
                    }
                    for cat, s in self.stats.category_stats.items()
                }
            },
            'question_effectiveness': self.get_question_effectiveness()[:50],
            'difficult_entities': self.get_difficult_entities()[:20],
            'suggestions': self.suggest_improvements()
        }

        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def print_summary(self):
        """Print a summary of training results."""
        print("\n" + "="*60)
        print("TRAINING SUMMARY")
        print("="*60)

        print(f"\nOverall Statistics:")
        print(f"  Total games: {self.stats.total_games}")
        print(f"  Accuracy: {100*self.stats.accuracy:.1f}%")
        print(f"  Avg questions (all): {self.stats.avg_questions_overall:.1f}")
        print(f"  Avg questions (correct): {self.stats.avg_questions_when_correct:.1f}")

        print(f"\nPer-Category Performance:")
        for category, stats in self.stats.category_stats.items():
            if stats['total'] > 0:
                rate = 100 * stats['correct'] / stats['total']
                avg_q = sum(stats['questions']) / len(stats['questions']) if stats['questions'] else 0
                print(f"  {category}: {rate:.1f}% accuracy, {avg_q:.1f} avg questions")

        print(f"\nTop 10 Most Effective Questions:")
        for qid, gain, count in self.get_question_effectiveness()[:10]:
            attr = self.kb.get_attribute(qid)
            q_text = attr.question if attr else qid
            print(f"  {qid}: {gain:.3f} avg gain ({count} uses)")

        print(f"\nMost Difficult Entities:")
        for eid, rate, attempts in self.get_difficult_entities()[:10]:
            entity = self.kb.get_entity(eid)
            name = entity.name if entity else eid
            print(f"  {name}: {100*rate:.1f}% success ({attempts} attempts)")

        suggestions = self.suggest_improvements()
        if suggestions['improve_entities']:
            print(f"\nEntities Needing Improvement:")
            for item in suggestions['improve_entities'][:5]:
                entity = self.kb.get_entity(item['entity'])
                name = entity.name if entity else item['entity']
                print(f"  {name}: {100*item['success_rate']:.1f}% success")
                if item['confused_with']:
                    print(f"    Often confused with: {', '.join(item['confused_with'][:3])}")


class AutoOptimizer:
    """
    Automatically optimizes the knowledge base based on training results.
    """

    def __init__(self, knowledge_base: KnowledgeBase, trainer: Trainer):
        self.kb = knowledge_base
        self.trainer = trainer

    def optimize(
        self,
        iterations: int = 5,
        games_per_iteration: int = 500,
        verbose: bool = True
    ) -> List[TrainingStats]:
        """
        Run iterative optimization.

        Each iteration:
        1. Run training simulation
        2. Analyze results
        3. Apply automatic improvements
        4. Repeat

        Args:
            iterations: Number of optimization iterations
            games_per_iteration: Games to run per iteration
            verbose: Print progress

        Returns:
            List of TrainingStats for each iteration
        """
        all_stats = []

        for i in range(iterations):
            if verbose:
                print(f"\n{'='*60}")
                print(f"OPTIMIZATION ITERATION {i+1}/{iterations}")
                print(f"{'='*60}")

            # Run training
            stats = self.trainer.run_simulation(
                num_games=games_per_iteration,
                weighted_selection=True,
                verbose=verbose,
                progress_interval=100
            )
            all_stats.append(stats)

            if verbose:
                self.trainer.print_summary()

            # Apply improvements
            improvements = self._apply_improvements()

            if verbose:
                print(f"\nApplied {improvements} improvements")

        return all_stats

    def _apply_improvements(self) -> int:
        """
        Apply automatic improvements based on training results.

        Returns:
            Number of improvements made
        """
        improvements = 0

        # Get confusion analysis
        confusion = self.trainer.get_confusion_matrix()

        # For confused entity pairs, try to add distinguishing attributes
        for entity_id, confused_with_list in confusion.items():
            if not confused_with_list:
                continue

            entity = self.kb.get_entity(entity_id)
            if not entity:
                continue

            for confused_id, count in confused_with_list[:3]:
                if count < 2:
                    continue

                confused_entity = self.kb.get_entity(confused_id)
                if not confused_entity:
                    continue

                # Find attributes that differ significantly
                distinguishing = self._find_distinguishing_attributes(
                    entity, confused_entity
                )

                # Strengthen distinguishing attributes
                for attr_id, diff in distinguishing[:3]:
                    if diff > 0:
                        # Entity has this attribute more
                        new_val = min(1.0, entity.attributes.get(attr_id, 0.5) + 0.1)
                        entity.attributes[attr_id] = new_val
                    else:
                        # Confused entity has it more, decrease ours
                        new_val = max(0.0, entity.attributes.get(attr_id, 0.5) - 0.1)
                        entity.attributes[attr_id] = new_val
                    improvements += 1

        return improvements

    def _find_distinguishing_attributes(
        self,
        entity1: Entity,
        entity2: Entity
    ) -> List[Tuple[str, float]]:
        """
        Find attributes that best distinguish two entities.

        Returns:
            List of (attr_id, difference) tuples, sorted by abs(difference)
        """
        all_attrs = set(entity1.attributes.keys()) | set(entity2.attributes.keys())

        differences = []
        for attr_id in all_attrs:
            val1 = entity1.get_attribute_probability(attr_id)
            val2 = entity2.get_attribute_probability(attr_id)
            diff = val1 - val2
            if abs(diff) > 0.3:  # Significant difference
                differences.append((attr_id, diff))

        differences.sort(key=lambda x: abs(x[1]), reverse=True)
        return differences


def run_training(
    data_dir: str = None,
    num_games: int = 1000,
    save_results: bool = True,
    verbose: bool = True
) -> TrainingStats:
    """
    Convenience function to run training.

    Args:
        data_dir: Directory containing knowledge base data
        num_games: Number of games to simulate
        save_results: Whether to save results to file
        verbose: Print progress

    Returns:
        Training statistics
    """
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')

    kb = KnowledgeBase(data_dir)
    trainer = Trainer(kb)

    stats = trainer.run_simulation(
        num_games=num_games,
        weighted_selection=True,
        verbose=verbose
    )

    if verbose:
        trainer.print_summary()

    if save_results:
        results_path = os.path.join(data_dir, 'training_results.json')
        trainer.save_results(results_path)
        if verbose:
            print(f"\nResults saved to: {results_path}")

    return stats


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Train the 20 Questions game')
    parser.add_argument('--games', type=int, default=1000, help='Number of games to simulate')
    parser.add_argument('--optimize', action='store_true', help='Run auto-optimization')
    parser.add_argument('--iterations', type=int, default=5, help='Optimization iterations')
    parser.add_argument('--quiet', action='store_true', help='Suppress output')

    args = parser.parse_args()

    if args.optimize:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        kb = KnowledgeBase(data_dir)
        trainer = Trainer(kb)
        optimizer = AutoOptimizer(kb, trainer)
        optimizer.optimize(
            iterations=args.iterations,
            games_per_iteration=args.games // args.iterations,
            verbose=not args.quiet
        )
    else:
        run_training(num_games=args.games, verbose=not args.quiet)
