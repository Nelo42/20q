"""
Question Selector for the 20 Questions game.

Implements entropy-based question selection to maximize information gain.
Uses hierarchical question ordering and implication-aware filtering.
"""

import numpy as np
from typing import Set, Optional, List, Tuple, Dict
from .models import BeliefState
from .knowledge_base import KnowledgeBase
from .belief_tracker import BeliefTracker
from .implications import ImplicationEngine


# Hierarchical question ordering - questions in earlier tiers are prioritized
# Tier 0: Opening category questions (Animal/Vegetable/Mineral)
# Tier 1: Context-aware broad classification (FIXED ORDER within category)
# Tier 2: Specific families/subtypes (info gain within tier)
# Tier 3: All other questions (selected by info gain)

# Category-specific question lists for context-aware Tier 1
TIER1_ANIMAL_QUESTIONS = [
    # Major biological classes - ordered by commonality
    'is_mammal',      # 46% of animals - ask first!
    'is_bird',        # 16% of animals
    'is_fish',        # 8% of animals
    'is_reptile',     # 7% of animals
    'is_insect',      # 10% of animals
    'is_amphibian',   # Less common
    'is_crustacean',
    'is_mollusk',
    'is_arachnid',
    # Key habitat/lifestyle questions - very discriminating
    'is_domesticated',
    'is_pet',
    'is_farm_animal',
    'is_wild',
]

TIER1_PLANT_QUESTIONS = [
    # Broad types - ordered by commonality
    'is_fruit',
    'is_vegetable_food',
    'is_tree',
    'is_flower',
    'is_fungus',
    'is_grain',
    'is_nut',
    'is_herb',
]

TIER1_OBJECT_QUESTIONS = [
    # Broad object types - ordered by commonality
    'is_electronic',
    'is_tool',
    'is_vehicle',
    'is_furniture',
    'is_clothing',
    'is_appliance',
    'is_accessory',
    'is_money',
    'is_personal_care',
    'is_kitchen_item',
    'is_bathroom_item',
    'is_cleaning_supply',
    'is_lighting',
]

QUESTION_HIERARCHY: Dict[int, Optional[List[str]]] = {
    # Tier 0: Opening questions - establish main category
    0: ['is_animal', 'is_vegetable', 'is_mineral'],

    # Tier 1: Now handled dynamically based on category (see _get_tier1_questions)
    1: None,  # Special handling - context-aware

    # Tier 2: Specific families/subtypes (info-gain based)
    2: [
        # Mammal families
        'is_primate', 'is_feline', 'is_canine', 'is_rodent',
        'is_cetacean', 'is_marsupial', 'is_equine', 'is_bovine', 'is_ape',
        # Habitat/lifestyle
        'lives_in_water', 'lives_in_ocean', 'can_fly',
        # Distinguishing animal features
        'hops', 'has_beard', 'has_mane', 'has_blowhole', 'echolocates',
        'has_wool', 'has_long_body', 'has_pincers', 'is_slimy',
        # Object subtypes
        'is_instrument', 'is_toy', 'is_weapon', 'is_jewelry', 'is_container',
        'is_cookware', 'is_utensil', 'is_dinnerware', 'is_cleaning_supply',
        # Clothing/wearing
        'worn_on_finger', 'worn_on_neck', 'worn_on_hands', 'worn_on_feet', 'worn_on_waist',
        # Plant growth & types
        'grows_on_trees', 'grows_underground', 'grows_on_vines', 'grows_on_bushes',
        'is_citrus', 'is_berry', 'is_tropical',
        'is_bulb', 'is_root_vegetable', 'is_cruciferous', 'is_legume', 'is_stone_fruit',
        'is_pungent', 'has_layers',
        # Size/color/shape for disambiguation
        'is_tiny', 'is_round', 'is_long', 'is_crunchy',
        # Functions
        'used_for_eating', 'used_for_drinking', 'holds_liquid', 'provides_security',
        'takes_photos', 'tells_time',
    ],

    # Tier 3: All remaining questions - pure info gain selection
    3: None,  # None means use all attributes
}

# Questions in Tier 0 should be asked in FIXED ORDER (not by info gain)
# Tier 1 is now context-aware but still fixed order within category
FIXED_ORDER_TIERS = {0, 1}


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
        self.implication_engine = ImplicationEngine()

    def _get_tier1_questions(self, known_answers: Dict[str, float]) -> List[str]:
        """
        Get context-aware Tier 1 questions based on determined category.

        Returns only relevant questions for the established category,
        avoiding irrelevant questions like 'is_electronic' for animals.

        Args:
            known_answers: Dict of {attr_id: answer_value} from previous questions

        Returns:
            List of relevant Tier 1 question IDs
        """
        # Check which category has been established
        is_animal = known_answers.get('is_animal', 0.5)
        is_vegetable = known_answers.get('is_vegetable', 0.5)
        is_mineral = known_answers.get('is_mineral', 0.5)

        # If animal confirmed (>0.7) or others denied (<0.3)
        if is_animal > 0.7 or (is_vegetable < 0.3 and is_mineral < 0.3):
            return TIER1_ANIMAL_QUESTIONS

        # If plant/vegetable confirmed or others denied
        if is_vegetable > 0.7 or (is_animal < 0.3 and is_mineral < 0.3):
            return TIER1_PLANT_QUESTIONS

        # If mineral/object confirmed or others denied
        if is_mineral > 0.7 or (is_animal < 0.3 and is_vegetable < 0.3):
            return TIER1_OBJECT_QUESTIONS

        # Category not yet determined - return all Tier 1 questions
        return TIER1_ANIMAL_QUESTIONS + TIER1_PLANT_QUESTIONS + TIER1_OBJECT_QUESTIONS

    def select_best_question(
        self,
        beliefs: BeliefState,
        asked_questions: Set[str],
        known_answers: Optional[Dict[str, float]] = None
    ) -> Optional[str]:
        """
        Select the question that maximizes expected information gain.

        Uses hierarchical question ordering:
        1. Tier 0: Category questions (Animal/Vegetable/Mineral)
        2. Tier 1: Subcategory questions (mammal/bird/electronic, etc.)
        3. Tier 2: All other questions (pure info gain)

        Skips questions whose answers are already logically determined
        from previous answers via the implication system.

        Args:
            beliefs: Current belief state
            asked_questions: Set of attribute IDs already asked
            known_answers: Dict of {attr_id: answer_value} for implication filtering

        Returns:
            Attribute ID of the best question, or None if no good questions remain
        """
        if known_answers is None:
            known_answers = {}

        current_entropy = self.bt.get_entropy(beliefs)

        # Search through tiers in order
        for tier in sorted(QUESTION_HIERARCHY.keys()):
            tier_attrs = QUESTION_HIERARCHY[tier]

            # Tier 1 is special: context-aware based on category
            if tier == 1:
                tier_attrs = self._get_tier1_questions(known_answers)
            elif tier_attrs is None:
                # Last tier (Tier 3): Use all attributes not in previous tiers
                all_tier_attrs = set(TIER1_ANIMAL_QUESTIONS + TIER1_PLANT_QUESTIONS + TIER1_OBJECT_QUESTIONS)
                all_tier_attrs.update(QUESTION_HIERARCHY.get(0, []) or [])
                all_tier_attrs.update(QUESTION_HIERARCHY.get(2, []) or [])
                tier_attrs = [
                    a.id for a in self.kb.get_all_attributes()
                    if a.id not in all_tier_attrs
                ]

            # Check if this tier uses fixed order (for natural flow)
            use_fixed_order = tier in FIXED_ORDER_TIERS

            if use_fixed_order:
                # Fixed order: Return first available question in the list order
                for attr_id in tier_attrs:
                    if attr_id in asked_questions:
                        continue
                    is_determined, _ = self.implication_engine.is_already_determined(
                        attr_id, known_answers
                    )
                    if is_determined:
                        continue
                    if self.kb.get_attribute(attr_id) is None:
                        continue
                    # Check minimum info gain threshold
                    info_gain = self._calculate_info_gain(beliefs, attr_id, current_entropy)
                    if info_gain >= self.min_info_gain:
                        return attr_id
                # No valid questions in this fixed-order tier, move to next tier
                continue

            # Info-gain based selection: Find best question within this tier
            best_question = None
            best_gain = -float('inf')

            for attr_id in tier_attrs:
                # Skip already asked questions
                if attr_id in asked_questions:
                    continue

                # Skip questions whose answers are already determined via implications
                is_determined, _ = self.implication_engine.is_already_determined(
                    attr_id, known_answers
                )
                if is_determined:
                    continue

                # Skip if attribute doesn't exist in knowledge base
                if self.kb.get_attribute(attr_id) is None:
                    continue

                info_gain = self._calculate_info_gain(
                    beliefs, attr_id, current_entropy
                )

                if info_gain > best_gain and info_gain >= self.min_info_gain:
                    best_gain = info_gain
                    best_question = attr_id

            # If we found a good question in this tier, return it
            if best_question is not None:
                return best_question

        return None

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
        min_margin: float = 0.15,
        questions_asked: int = 0,
        max_questions: int = 20
    ) -> bool:
        """
        Determine if we should make a guess instead of asking another question.

        Uses multiple criteria for smarter guessing:
        1. Traditional threshold + margin check
        2. Low entropy check (high certainty)
        3. Strong dominance (top >> 2nd place)
        4. Progressive threshold (more aggressive as questions increase)

        Args:
            beliefs: Current belief state
            threshold: Minimum probability for top entity to trigger guess
            min_margin: Minimum margin over second-best entity
            questions_asked: Number of questions asked so far
            max_questions: Maximum questions allowed

        Returns:
            True if we should guess, False if we should ask another question
        """
        top_entities = beliefs.get_top_entities(3)

        if len(top_entities) == 0:
            return False

        if len(top_entities) == 1:
            return top_entities[0][1] >= threshold * 0.5  # Lower threshold for single entity

        top_prob = top_entities[0][1]
        second_prob = top_entities[1][1]
        third_prob = top_entities[2][1] if len(top_entities) > 2 else 0.0

        # Calculate entropy to check certainty
        entropy = self.bt.get_entropy(beliefs)
        num_entities = len(beliefs.probabilities)
        max_entropy = np.log2(num_entities) if num_entities > 0 else 1.0

        # Normalized entropy (0 = certain, 1 = completely uncertain)
        norm_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        # Progressive threshold - lower as we ask more questions
        progress = questions_asked / max_questions
        adjusted_threshold = threshold * (1.0 - progress * 0.5)  # Threshold drops to 50% of original at max questions
        adjusted_margin = min_margin * (1.0 - progress * 0.5)

        # Criterion 1: Traditional threshold + margin (with progressive adjustment)
        if top_prob >= adjusted_threshold and (top_prob - second_prob) >= adjusted_margin:
            return True

        # Criterion 2: Very low entropy (very certain)
        if norm_entropy < 0.15:  # Less than 15% of max entropy
            return True

        # Criterion 3: Strong dominance - top is at least 3x the second place
        if top_prob > 0.1 and second_prob > 0 and top_prob / second_prob >= 3.0:
            return True

        # Criterion 4: Top entity is significantly ahead of both 2nd and 3rd
        if top_prob > 0.15 and (top_prob - second_prob) >= 0.08 and (top_prob - third_prob) >= 0.12:
            return True

        return False

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
