"""
Belief Tracker for the 20 Questions game.

Implements Bayesian belief updates based on user answers.
"""

import numpy as np
from typing import Optional, List, Tuple
from .models import BeliefState
from .knowledge_base import KnowledgeBase
from .implications import ImplicationEngine


class BeliefTracker:
    """
    Tracks and updates belief state using Bayesian inference.

    After each answer, updates the probability distribution over entities
    using Bayes' theorem: P(entity|answer) ∝ P(answer|entity) * P(entity)
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        unknown_likelihood: float = 0.5,
        smoothing: float = 0.01
    ):
        """
        Initialize the belief tracker.

        Args:
            knowledge_base: The knowledge base to use
            unknown_likelihood: Likelihood to use for "don't know" answers
            smoothing: Small value to prevent zero probabilities
        """
        self.kb = knowledge_base
        self.unknown_likelihood = unknown_likelihood
        self.smoothing = smoothing
        self.implication_engine = ImplicationEngine()

    def initialize_beliefs(self) -> BeliefState:
        """Create uniform prior distribution over all entities."""
        entity_ids = self.kb.get_all_entity_ids()
        return BeliefState.uniform(entity_ids)

    def update_beliefs(
        self,
        beliefs: BeliefState,
        attribute_id: str,
        answer: float
    ) -> BeliefState:
        """
        Update beliefs based on an answer to a question.

        Uses Bayes' theorem with implication propagation:
        1. Apply direct update for the answered attribute
        2. Propagate logical implications to update beliefs for implied attributes

        Args:
            beliefs: Current belief state
            attribute_id: The attribute/question that was asked
            answer: User's answer (1.0=yes, 0.0=no, 0.5=unknown)

        Returns:
            Updated belief state
        """
        # First, apply the direct update for the answered attribute
        result = self._apply_single_update(beliefs, attribute_id, answer)

        # Then, propagate logical implications
        implications = self.implication_engine.get_implications(attribute_id, answer)
        for implied_attr, implied_val in implications:
            result = self._apply_single_update(result, implied_attr, implied_val)

        return result

    def _apply_single_update(
        self,
        beliefs: BeliefState,
        attribute_id: str,
        answer: float
    ) -> BeliefState:
        """
        Apply a single Bayesian update for one attribute.

        Uses Bayes' theorem:
        P(entity|answer) ∝ P(answer|entity) * P(entity)

        Args:
            beliefs: Current belief state
            attribute_id: The attribute to update
            answer: The answer value (1.0=yes, 0.0=no, 0.5=unknown)

        Returns:
            Updated belief state
        """
        new_probs = {}

        for entity_id, prior_prob in beliefs.probabilities.items():
            entity = self.kb.get_entity(entity_id)
            if entity is None:
                continue

            # Get P(yes|entity) for this attribute
            p_yes = entity.get_attribute_probability(attribute_id)

            # Calculate likelihood based on answer
            likelihood = self._calculate_likelihood(p_yes, answer)

            # Apply Bayes: posterior ∝ likelihood * prior
            # Add smoothing to prevent zero probabilities
            new_probs[entity_id] = (likelihood + self.smoothing) * prior_prob

        # Create new belief state and normalize
        result = BeliefState(probabilities=new_probs)
        result.normalize()

        return result

    def _calculate_likelihood(self, p_yes: float, answer: float) -> float:
        """
        Calculate likelihood P(answer|entity).

        Args:
            p_yes: P(yes|entity) - probability entity has this attribute
            answer: User's answer (1.0=yes, 0.0=no, 0.5=unknown)

        Returns:
            Likelihood value
        """
        if answer > 0.7:  # Yes
            return p_yes
        elif answer < 0.3:  # No
            return 1.0 - p_yes
        else:  # Unknown/Maybe
            # For uncertain answers, use a neutral likelihood
            # that slightly favors entities closer to 0.5
            return self.unknown_likelihood

    def get_entropy(self, beliefs: BeliefState) -> float:
        """
        Calculate Shannon entropy of the belief distribution.

        H = -Σ p(x) * log2(p(x))

        Lower entropy means more certainty about the answer.

        Args:
            beliefs: Current belief state

        Returns:
            Entropy value (0 = completely certain, log2(n) = completely uncertain)
        """
        entropy = 0.0
        for prob in beliefs.probabilities.values():
            if prob > 0:
                entropy -= prob * np.log2(prob)
        return entropy

    def get_confidence(self, beliefs: BeliefState) -> float:
        """
        Calculate confidence as the probability of the top entity.

        Args:
            beliefs: Current belief state

        Returns:
            Confidence value (0.0 to 1.0)
        """
        _, max_prob = beliefs.get_max_probability()
        return max_prob

    def get_top_entity(self, beliefs: BeliefState) -> Optional[str]:
        """
        Get the most likely entity.

        Args:
            beliefs: Current belief state

        Returns:
            Entity ID of the most likely entity, or None if empty
        """
        entity_id, _ = beliefs.get_max_probability()
        return entity_id

    def simulate_answer(
        self,
        beliefs: BeliefState,
        attribute_id: str,
        answer: float
    ) -> BeliefState:
        """
        Simulate what beliefs would look like after an answer.

        Creates a copy of beliefs and applies the update without
        modifying the original.

        Args:
            beliefs: Current belief state
            attribute_id: The attribute/question
            answer: Hypothetical answer

        Returns:
            Simulated belief state
        """
        return self.update_beliefs(beliefs.copy(), attribute_id, answer)

    def get_answer_probability(
        self,
        beliefs: BeliefState,
        attribute_id: str
    ) -> float:
        """
        Estimate P(yes) for an attribute given current beliefs.

        P(yes) = Σ P(yes|entity) * P(entity)

        Args:
            beliefs: Current belief state
            attribute_id: The attribute to query

        Returns:
            Estimated probability of "yes" answer
        """
        p_yes = 0.0
        for entity_id, prob in beliefs.probabilities.items():
            entity = self.kb.get_entity(entity_id)
            if entity:
                p_yes += entity.get_attribute_probability(attribute_id) * prob
        return p_yes
