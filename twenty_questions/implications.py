"""
Attribute Implication System for the 20 Questions game.

Defines logical implications between attributes to enable
constraint propagation and redundant question elimination.

When a user answers a question, this system propagates logical
implications to infer answers to related questions.
"""

from typing import Dict, List, Tuple, Optional


# Implication rules: (attribute_id, answer_value) -> [(implied_attr, implied_value), ...]
# answer_value: 1.0 = if user answers yes, 0.0 = if user answers no
ATTRIBUTE_IMPLICATIONS: Dict[Tuple[str, float], List[Tuple[str, float]]] = {
    # ========================================
    # CATEGORY IMPLICATIONS (Animal/Vegetable/Mineral)
    # ========================================
    ('is_animal', 1.0): [
        ('is_vegetable', 0.0),
        ('is_mineral', 0.0),
        ('is_living', 1.0),
        ('is_natural', 0.9),
    ],
    ('is_animal', 0.0): [
        # If not an animal, exclude all animal-specific attributes
        ('is_mammal', 0.0),
        ('is_bird', 0.0),
        ('is_fish', 0.0),
        ('is_reptile', 0.0),
        ('is_amphibian', 0.0),
        ('is_insect', 0.0),
        ('is_arachnid', 0.0),
        ('is_crustacean', 0.0),
        ('is_mollusk', 0.0),
        ('is_primate', 0.0),
        ('is_rodent', 0.0),
        ('is_feline', 0.0),
        ('is_canine', 0.0),
        ('is_bovine', 0.0),
        ('is_equine', 0.0),
        ('is_cetacean', 0.0),
        ('is_marsupial', 0.0),
        ('is_carnivore', 0.0),
        ('is_herbivore', 0.0),
        ('is_omnivore', 0.0),
        ('is_predator', 0.0),
        ('is_domesticated', 0.0),
        ('is_pet', 0.0),
        ('is_farm_animal', 0.0),
        ('is_wild', 0.0),
    ],
    ('is_vegetable', 1.0): [
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
        ('is_living', 1.0),
        ('is_natural', 1.0),
    ],
    ('is_vegetable', 0.0): [
        # If not a vegetable/plant, exclude plant-specific attributes
        ('is_fruit', 0.0),
        ('is_vegetable_food', 0.0),
        ('is_grain', 0.0),
        ('is_nut', 0.0),
        ('is_herb', 0.0),
        ('is_flower', 0.0),
        ('is_tree', 0.0),
        ('is_grass', 0.0),
        ('is_fungus', 0.0),
        ('is_aquatic_plant', 0.0),
        ('grows_on_trees', 0.0),
        ('grows_underground', 0.0),
        ('grows_on_vines', 0.0),
        ('has_leaves', 0.0),
        ('has_seeds', 0.0),
    ],
    ('is_mineral', 1.0): [
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
        ('is_living', 0.0),
    ],
    ('is_mineral', 0.0): [
        # If not a mineral/object, exclude object-specific attributes
        ('is_electronic', 0.0),
        ('is_mechanical', 0.0),
        ('is_vehicle', 0.0),
        ('is_furniture', 0.0),
        ('is_clothing', 0.0),
        ('is_jewelry', 0.0),
        ('is_appliance', 0.0),
        ('is_instrument', 0.0),
        ('requires_batteries', 0.0),
        ('plugs_in', 0.0),
        ('has_screen', 0.0),
    ],

    # ========================================
    # ANIMAL BIOLOGY IMPLICATIONS
    # ========================================
    ('is_mammal', 1.0): [
        ('is_animal', 1.0),
        ('is_bird', 0.0),
        ('is_fish', 0.0),
        ('is_reptile', 0.0),
        ('is_amphibian', 0.0),
        ('is_insect', 0.0),
        ('is_arachnid', 0.0),
        ('is_crustacean', 0.0),
        ('is_mollusk', 0.0),
        ('has_fur', 0.9),
        ('gives_live_birth', 0.9),
        ('lays_eggs', 0.1),
        ('has_feathers', 0.0),
        ('has_scales', 0.1),
    ],
    ('is_mammal', 0.0): [
        # If not a mammal, exclude all mammal-specific families
        ('is_primate', 0.0),
        ('is_rodent', 0.0),
        ('is_feline', 0.0),
        ('is_canine', 0.0),
        ('is_bovine', 0.0),
        ('is_equine', 0.0),
        ('is_cetacean', 0.0),
        ('is_marsupial', 0.0),
    ],
    ('is_bird', 1.0): [
        ('is_animal', 1.0),
        ('is_mammal', 0.0),
        ('is_fish', 0.0),
        ('is_reptile', 0.0),
        ('is_insect', 0.0),
        ('has_feathers', 1.0),
        ('has_wings', 1.0),
        ('has_beak', 1.0),
        ('lays_eggs', 1.0),
        ('has_two_legs', 1.0),
        ('has_fur', 0.0),
        ('has_four_legs', 0.0),
        ('gives_live_birth', 0.0),
    ],
    ('is_fish', 1.0): [
        ('is_animal', 1.0),
        ('is_mammal', 0.0),
        ('is_bird', 0.0),
        ('is_reptile', 0.0),
        ('is_insect', 0.0),
        ('lives_in_water', 1.0),
        ('can_swim', 1.0),
        ('has_fins', 1.0),
        ('has_scales', 0.9),
        ('has_fur', 0.0),
        ('has_feathers', 0.0),
        ('has_four_legs', 0.0),
        ('can_fly', 0.0),
    ],
    ('is_reptile', 1.0): [
        ('is_animal', 1.0),
        ('is_mammal', 0.0),
        ('is_bird', 0.0),
        ('is_fish', 0.0),
        ('is_insect', 0.0),
        ('has_scales', 0.95),
        ('lays_eggs', 0.9),
        ('has_fur', 0.0),
        ('has_feathers', 0.0),
        ('gives_live_birth', 0.1),
    ],
    ('is_amphibian', 1.0): [
        ('is_animal', 1.0),
        ('is_mammal', 0.0),
        ('is_bird', 0.0),
        ('is_fish', 0.0),
        ('is_reptile', 0.0),
        ('is_insect', 0.0),
        ('can_swim', 0.95),
        ('lays_eggs', 1.0),
        ('has_fur', 0.0),
        ('has_feathers', 0.0),
        ('lives_in_water', 0.7),
    ],
    ('is_insect', 1.0): [
        ('is_animal', 1.0),
        ('is_mammal', 0.0),
        ('is_bird', 0.0),
        ('is_fish', 0.0),
        ('is_reptile', 0.0),
        ('has_many_legs', 1.0),
        ('is_small', 1.0),
        ('is_tiny', 0.9),
        ('has_fur', 0.0),
        ('has_feathers', 0.0),
        ('is_large', 0.0),
        ('gives_live_birth', 0.0),
        ('lays_eggs', 1.0),
    ],
    ('is_arachnid', 1.0): [
        ('is_animal', 1.0),
        ('is_insect', 0.0),
        ('is_mammal', 0.0),
        ('has_many_legs', 1.0),
        ('is_small', 1.0),
        ('has_fur', 0.0),
    ],
    ('is_crustacean', 1.0): [
        ('is_animal', 1.0),
        ('has_shell', 0.95),
        ('lives_in_water', 0.9),
        ('has_many_legs', 1.0),
        ('has_pincers', 0.9),
        ('is_mammal', 0.0),
        ('is_bird', 0.0),
        ('is_fish', 0.0),
        ('is_reptile', 0.0),
        ('is_insect', 0.0),
    ],
    ('is_mollusk', 1.0): [
        ('is_animal', 1.0),
        ('is_mammal', 0.0),
        ('is_bird', 0.0),
        ('has_shell', 0.7),
        ('has_fur', 0.0),
    ],

    # Specific animal families
    ('is_primate', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('is_intelligent', 0.9),
        ('can_climb', 0.9),
    ],
    ('is_feline', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('is_predator', 0.95),
        ('is_carnivore', 0.95),
        ('has_claws', 1.0),
    ],
    ('is_canine', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('has_fur', 1.0),
    ],
    ('is_cetacean', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('lives_in_water', 1.0),
        ('lives_in_ocean', 0.95),
        ('can_swim', 1.0),
        ('is_large', 0.9),
        ('has_fins', 1.0),
        ('has_fur', 0.0),
    ],
    ('is_marsupial', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('has_pouch', 1.0),
        ('lives_in_australia', 0.6),  # Reduced: opossums are American marsupials
    ],
    ('is_equine', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('has_hooves', 1.0),
        ('has_four_legs', 1.0),
        ('is_herbivore', 1.0),
    ],
    ('is_bovine', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('has_hooves', 1.0),
        ('has_four_legs', 1.0),
        ('is_herbivore', 1.0),
    ],
    ('is_rodent', 1.0): [
        ('is_mammal', 1.0),
        ('is_animal', 1.0),
        ('is_small', 0.9),
    ],

    # ========================================
    # PHYSICAL FEATURE IMPLICATIONS
    # ========================================
    ('has_feathers', 1.0): [
        ('is_bird', 0.95),
        ('has_fur', 0.0),
        ('has_scales', 0.0),
    ],
    ('has_trunk', 1.0): [
        ('is_mammal', 1.0),
        ('is_large', 1.0),
        ('is_huge', 0.9),
    ],
    ('has_hooves', 1.0): [
        ('is_mammal', 1.0),
        ('has_claws', 0.0),
    ],
    ('has_fins', 1.0): [
        ('can_swim', 1.0),
        ('has_four_legs', 0.0),
    ],
    ('has_pouch', 1.0): [
        ('is_marsupial', 1.0),
        ('is_mammal', 1.0),
    ],
    ('has_shell', 1.0): [
        ('is_soft', 0.0),
    ],
    ('has_wool', 1.0): [
        ('is_mammal', 1.0),
        ('is_farm_animal', 0.9),
        ('has_fur', 1.0),  # Wool is a type of fur
    ],
    ('has_long_body', 1.0): [
        ('is_round', 0.0),
    ],
    ('has_tentacles', 1.0): [
        ('is_mollusk', 0.8),
        ('lives_in_water', 0.9),
    ],

    # Size implications
    ('is_huge', 1.0): [
        ('is_large', 1.0),
        ('is_small', 0.0),
        ('is_tiny', 0.0),
        ('is_microscopic', 0.0),
    ],
    ('is_large', 1.0): [
        ('is_small', 0.0),
        ('is_tiny', 0.0),
        ('is_microscopic', 0.0),
    ],
    ('is_tiny', 1.0): [
        ('is_small', 1.0),
        ('is_large', 0.0),
        ('is_huge', 0.0),
    ],
    ('is_microscopic', 1.0): [
        ('is_tiny', 1.0),
        ('is_small', 1.0),
        ('is_large', 0.0),
        ('is_huge', 0.0),
    ],

    # ========================================
    # DOMESTICATION/HABITAT IMPLICATIONS
    # ========================================
    ('is_pet', 1.0): [
        ('is_domesticated', 1.0),
        ('is_animal', 1.0),
        ('is_wild', 0.1),  # Pets are rarely wild
    ],
    ('is_farm_animal', 1.0): [
        ('is_domesticated', 1.0),
        ('is_animal', 1.0),
        ('is_wild', 0.1),  # Farm animals are rarely wild
    ],
    ('is_domesticated', 1.0): [
        ('is_animal', 1.0),
        ('is_wild', 0.2),  # Domesticated animals can occasionally be wild (feral)
    ],
    ('is_wild', 1.0): [
        ('is_animal', 1.0),
        ('is_pet', 0.1),  # Wild animals are rarely pets
        ('is_domesticated', 0.2),  # Wild animals are rarely domesticated
    ],

    # ========================================
    # DIET IMPLICATIONS
    # ========================================
    ('is_carnivore', 1.0): [
        ('is_animal', 1.0),
        ('is_herbivore', 0.0),
        ('is_predator', 0.9),
    ],
    ('is_herbivore', 1.0): [
        ('is_animal', 1.0),
        ('is_carnivore', 0.0),
        ('is_predator', 0.0),
    ],
    ('is_predator', 1.0): [
        ('is_animal', 1.0),
        ('is_herbivore', 0.0),
    ],

    # ========================================
    # HABITAT IMPLICATIONS
    # ========================================
    ('lives_in_water', 1.0): [
        ('can_swim', 1.0),
        ('can_fly', 0.1),
    ],
    ('lives_in_ocean', 1.0): [
        ('lives_in_water', 1.0),
        ('can_swim', 1.0),
    ],
    ('lives_in_freshwater', 1.0): [
        ('lives_in_water', 1.0),
        ('can_swim', 1.0),
    ],
    ('can_fly', 1.0): [
        ('has_wings', 1.0),
    ],

    # ========================================
    # PLANT/VEGETABLE IMPLICATIONS
    # ========================================
    ('is_fruit', 1.0): [
        ('is_vegetable', 1.0),
        ('has_seeds', 0.95),
        ('is_food', 1.0),
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
        ('is_vegetable_food', 0.1),  # Fruits aren't typically culinary vegetables
        # Note: Removed has_leaves implication - fruits grow on plants that have leaves
    ],
    ('is_vegetable_food', 1.0): [
        ('is_vegetable', 1.0),
        ('is_food', 1.0),
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
        ('is_fruit', 0.2),  # Culinary vegetables aren't typically fruits
    ],
    ('has_leaves', 1.0): [
        ('is_vegetable', 1.0),
        # Note: Removed is_fruit=0 - many fruits grow on plants with leaves (apples, oranges, etc.)
    ],
    ('is_berry', 1.0): [
        ('is_vegetable', 1.0),
        ('is_fruit', 1.0),
        ('is_small', 1.0),
        ('is_food', 1.0),
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
    ],
    ('is_citrus', 1.0): [
        ('is_vegetable', 1.0),
        ('is_fruit', 1.0),
        ('has_skin', 1.0),
        ('is_food', 1.0),
        ('is_sour', 0.8),
        ('is_berry', 0.0),  # Citrus are not berries
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
    ],
    ('grows_on_bushes', 1.0): [
        ('is_vegetable', 1.0),
        ('grows_on_trees', 0.0),
        ('grows_underground', 0.0),
    ],
    ('is_tree', 1.0): [
        ('is_vegetable', 1.0),
        ('has_leaves', 0.95),
        ('is_large', 0.8),
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
    ],
    ('is_flower', 1.0): [
        ('is_vegetable', 1.0),
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
    ],
    ('is_fungus', 1.0): [
        ('is_vegetable', 1.0),
        ('is_animal', 0.0),
        ('is_mineral', 0.0),
    ],
    ('grows_on_trees', 1.0): [
        ('is_vegetable', 1.0),
    ],
    ('grows_underground', 1.0): [
        ('is_vegetable', 1.0),
    ],

    # ========================================
    # OBJECT/MINERAL IMPLICATIONS
    # ========================================
    ('is_electronic', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
        ('is_living', 0.0),
    ],
    ('is_vehicle', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('has_wheels', 0.8),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
    ('is_furniture', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
        ('found_at_home', 0.9),
    ],
    ('is_clothing', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('is_worn', 1.0),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
    ('is_appliance', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('is_electronic', 0.9),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
    ('is_tool', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
    ('is_instrument', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('makes_music', 1.0),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
    ('has_screen', 1.0): [
        ('is_electronic', 1.0),
        ('is_mineral', 1.0),
    ],
    ('requires_batteries', 1.0): [
        ('is_electronic', 1.0),
        ('is_mineral', 1.0),
    ],
    ('plugs_in', 1.0): [
        ('is_electronic', 1.0),
        ('is_mineral', 1.0),
    ],

    # Material implications
    ('is_metal', 1.0): [
        ('is_mineral', 1.0),
        ('is_hard', 0.95),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
    ('is_plastic', 1.0): [
        ('is_mineral', 1.0),
        ('is_manmade', 1.0),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
    ('is_glass', 1.0): [
        ('is_mineral', 1.0),
        ('is_transparent', 0.9),
        ('is_hard', 1.0),
        ('is_animal', 0.0),
        ('is_vegetable', 0.0),
    ],
}


class ImplicationEngine:
    """
    Applies logical implications to attribute answers.

    When a user answers a question, this engine determines what other
    attributes are logically implied by that answer.
    """

    def __init__(self, implications: Optional[Dict] = None):
        """
        Initialize the implication engine.

        Args:
            implications: Custom implication rules (uses defaults if None)
        """
        self.implications = implications or ATTRIBUTE_IMPLICATIONS
        self._build_reverse_index()

    def _build_reverse_index(self):
        """Build an index of which attributes can be implied by others."""
        self.implied_by: Dict[str, List[Tuple[str, float, float]]] = {}
        for (cond_attr, cond_val), implications in self.implications.items():
            for implied_attr, implied_val in implications:
                if implied_attr not in self.implied_by:
                    self.implied_by[implied_attr] = []
                self.implied_by[implied_attr].append((cond_attr, cond_val, implied_val))

    def get_implications(self, attribute_id: str, answer: float) -> List[Tuple[str, float]]:
        """
        Get all attributes implied by an answer.

        Args:
            attribute_id: The attribute that was answered
            answer: The answer value (1.0=yes, 0.0=no, 0.5=maybe)

        Returns:
            List of (attr_id, implied_value) tuples
        """
        # Only trigger implications for definitive answers
        if answer > 0.7:
            answer_key = 1.0
        elif answer < 0.3:
            answer_key = 0.0
        else:
            return []  # "Maybe" doesn't trigger implications

        key = (attribute_id, answer_key)
        return self.implications.get(key, [])

    def is_already_determined(
        self,
        attribute_id: str,
        known_answers: Dict[str, float]
    ) -> Tuple[bool, Optional[float]]:
        """
        Check if an attribute's answer is already logically determined.

        Args:
            attribute_id: The attribute to check
            known_answers: Dict of {attr_id: answer_value} from previous questions

        Returns:
            (is_determined, implied_value) or (False, None)
        """
        if attribute_id not in self.implied_by:
            return (False, None)

        for cond_attr, cond_val, implied_val in self.implied_by[attribute_id]:
            if cond_attr in known_answers:
                known_val = known_answers[cond_attr]
                # Check if the condition is met
                if cond_val == 1.0 and known_val > 0.7:
                    return (True, implied_val)
                elif cond_val == 0.0 and known_val < 0.3:
                    return (True, implied_val)

        return (False, None)

    def get_all_determined_attributes(
        self,
        known_answers: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Get all attributes that are logically determined from known answers.

        Uses iterative propagation to handle transitive implications:
        e.g., is_bird=1 -> is_mammal=0 -> is_cetacean=0

        Args:
            known_answers: Dict of {attr_id: answer_value}

        Returns:
            Dict of {attr_id: implied_value} for all determined attributes
        """
        # Create a working copy that includes both known and determined
        all_known = dict(known_answers)
        determined = {}

        # Iterate until no new determinations
        max_iterations = 10  # Prevent infinite loops
        for _ in range(max_iterations):
            new_determinations = {}

            for attr_id in self.implied_by:
                if attr_id in all_known:
                    continue  # Already known or determined

                is_det, implied_val = self.is_already_determined(attr_id, all_known)
                if is_det:
                    new_determinations[attr_id] = implied_val

            if not new_determinations:
                break  # Converged, no new determinations

            # Add new determinations to working set
            all_known.update(new_determinations)
            determined.update(new_determinations)

        return determined
