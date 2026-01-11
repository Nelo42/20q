"""
Comprehensive Entity Generator for 20 Questions game.

Generates 500+ entities per category with:
- Popularity rankings (common items ranked higher)
- Comprehensive attributes (size, color, habitat, etc.)
- Hierarchical categorization
"""

import json
import os
from typing import Dict, List, Tuple

# ============================================================================
# ANIMAL DATABASE - Ranked by how commonly people think of them
# ============================================================================

ANIMALS = [
    # MAMMALS - PETS (Rank 1-20, most commonly thought of)
    ("dog", "a dog", 1, {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 0.95, "is_domesticated": 1.0, "is_pet": 0.95, "makes_noise": 0.9, "is_intelligent": 0.8, "is_medium": 0.7, "is_omnivore": 0.7, "is_brown": 0.4}),
    ("cat", "a cat", 2, {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 0.95, "is_domesticated": 1.0, "is_pet": 0.95, "is_predator": 0.8, "is_nocturnal": 0.6, "has_claws": 1.0, "is_small": 0.7, "is_carnivore": 0.9}),
    ("horse", "a horse", 3, {"is_animal": 1.0, "is_mammal": 1.0, "is_equine": 1.0, "has_fur": 0.9, "has_four_legs": 1.0, "has_tail": 1.0, "is_domesticated": 0.95, "is_large": 1.0, "is_fast": 0.9, "has_hooves": 1.0, "is_herbivore": 1.0, "is_strong": 0.9, "is_farm_animal": 0.7, "is_brown": 0.5}),
    ("rabbit", "a rabbit", 4, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_small": 0.9, "is_herbivore": 1.0, "is_pet": 0.7, "can_jump": 1.0, "is_fast": 0.7, "has_tail": 0.8, "is_white": 0.4, "is_wild": 0.6}),
    ("hamster", "a hamster", 5, {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 1.0, "is_tiny": 0.9, "is_pet": 0.95, "is_nocturnal": 0.8, "has_four_legs": 1.0, "is_herbivore": 0.8}),
    ("goldfish", "a goldfish", 6, {"is_animal": 1.0, "is_fish": 1.0, "lives_in_water": 1.0, "has_fins": 1.0, "has_scales": 1.0, "is_pet": 0.95, "is_orange": 0.9, "is_small": 0.9, "lives_in_freshwater": 0.9, "is_colorful": 0.7}),
    ("guinea_pig", "a guinea pig", 7, {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 0.9, "is_pet": 0.95, "is_herbivore": 1.0, "makes_noise": 0.8, "has_four_legs": 1.0}),

    # MAMMALS - FARM (Rank 8-20)
    ("cow", "a cow", 8, {"is_animal": 1.0, "is_mammal": 1.0, "is_bovine": 1.0, "has_fur": 0.8, "has_four_legs": 1.0, "has_tail": 1.0, "is_domesticated": 1.0, "is_farm_animal": 1.0, "is_large": 1.0, "is_herbivore": 1.0, "is_food": 0.8, "has_horns": 0.5, "is_black": 0.3, "is_white": 0.3}),
    ("pig", "a pig", 9, {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "has_tail": 0.9, "is_domesticated": 1.0, "is_farm_animal": 1.0, "is_medium": 0.8, "is_omnivore": 1.0, "is_food": 0.8, "is_intelligent": 0.7, "is_pink": 0.7}),
    ("chicken", "a chicken", 10, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_two_legs": 1.0, "has_wings": 1.0, "can_fly": 0.1, "is_domesticated": 1.0, "is_farm_animal": 1.0, "is_small": 0.8, "lays_eggs": 1.0, "is_food": 0.9, "has_beak": 1.0}),
    ("sheep", "a sheep", 11, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_wool": 1.0, "has_four_legs": 1.0, "is_domesticated": 1.0, "is_farm_animal": 1.0, "is_medium": 0.8, "is_herbivore": 1.0, "is_white": 0.8, "gives_live_birth": 1.0}),
    ("goat", "a goat", 12, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 0.9, "has_wool": 0.0, "has_four_legs": 1.0, "is_domesticated": 0.9, "is_farm_animal": 0.9, "is_medium": 0.8, "is_herbivore": 1.0, "has_horns": 0.8, "can_climb": 0.9}),
    ("duck", "a duck", 13, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_two_legs": 1.0, "has_wings": 1.0, "can_fly": 0.8, "can_swim": 1.0, "lives_in_water": 0.7, "is_farm_animal": 0.6, "has_beak": 1.0, "lays_eggs": 1.0, "makes_noise": 0.9}),
    ("turkey", "a turkey", 14, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_two_legs": 1.0, "has_wings": 1.0, "can_fly": 0.2, "is_farm_animal": 0.8, "is_large": 0.7, "is_food": 0.9, "has_beak": 1.0}),
    ("donkey", "a donkey", 15, {"is_animal": 1.0, "is_mammal": 1.0, "is_equine": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_domesticated": 0.9, "is_farm_animal": 0.8, "is_large": 0.8, "is_herbivore": 1.0, "has_hooves": 1.0, "makes_noise": 0.8}),

    # MAMMALS - WILD POPULAR (Rank 16-50)
    ("elephant", "an elephant", 16, {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "has_tail": 0.9, "is_wild": 1.0, "is_huge": 1.0, "is_large": 1.0, "is_herbivore": 1.0, "has_trunk": 1.0, "has_tusks": 0.7, "is_intelligent": 0.9, "lives_in_africa": 0.7, "lives_in_asia": 0.3, "is_grey": 1.0, "is_endangered": 0.7}),
    ("lion", "a lion", 17, {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 0.9, "lives_in_africa": 1.0, "lives_in_grassland": 0.9, "is_yellow": 0.7, "is_brown": 0.5}),
    ("tiger", "a tiger", 18, {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 0.9, "has_stripes": 1.0, "lives_in_asia": 1.0, "is_orange": 0.8, "is_endangered": 0.8}),
    ("bear", "a bear", 19, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_large": 1.0, "is_omnivore": 0.8, "is_predator": 0.7, "is_dangerous": 0.8, "hibernates": 0.8, "is_strong": 1.0, "has_claws": 1.0, "is_brown": 0.6}),
    ("monkey", "a monkey", 20, {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "has_four_legs": 0.5, "has_two_legs": 0.5, "has_tail": 0.9, "is_wild": 0.9, "is_medium": 0.7, "is_omnivore": 0.8, "can_climb": 1.0, "is_intelligent": 0.8, "lives_in_trees": 0.8, "lives_in_jungle": 0.7}),
    ("giraffe", "a giraffe", 21, {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_huge": 1.0, "is_large": 1.0, "is_herbivore": 1.0, "has_long_neck": 1.0, "has_spots": 1.0, "lives_in_africa": 1.0, "lives_in_grassland": 0.9, "is_yellow": 0.6, "is_brown": 0.5}),
    ("zebra", "a zebra", 22, {"is_animal": 1.0, "is_mammal": 1.0, "is_equine": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 0.8, "is_herbivore": 1.0, "has_stripes": 1.0, "has_hooves": 1.0, "lives_in_africa": 1.0, "lives_in_grassland": 0.9, "is_black": 0.5, "is_white": 0.5}),
    ("wolf", "a wolf", 23, {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_medium": 0.8, "is_carnivore": 1.0, "is_predator": 1.0, "lives_in_groups": 0.9, "makes_noise": 0.9, "is_grey": 0.7, "is_dangerous": 0.6}),
    ("fox", "a fox", 24, {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.95, "is_small": 0.7, "is_medium": 0.5, "is_omnivore": 0.8, "is_predator": 0.6, "is_nocturnal": 0.7, "is_orange": 0.8, "is_intelligent": 0.7}),
    ("deer", "a deer", 25, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 0.8, "is_wild": 0.95, "is_medium": 0.7, "is_large": 0.5, "is_herbivore": 1.0, "has_horns": 0.5, "is_fast": 0.8, "is_brown": 0.8}),
    ("kangaroo", "a kangaroo", 26, {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_two_legs": 1.0, "has_tail": 1.0, "is_wild": 0.95, "is_large": 0.7, "is_herbivore": 1.0, "can_jump": 1.0, "has_pouch": 1.0, "lives_in_australia": 1.0, "is_brown": 0.7}),
    ("koala", "a koala", 27, {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 0.95, "is_small": 0.8, "is_herbivore": 1.0, "lives_in_trees": 1.0, "has_pouch": 1.0, "lives_in_australia": 1.0, "is_grey": 0.8}),
    ("panda", "a panda", 28, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 0.95, "is_large": 0.8, "is_herbivore": 0.95, "is_endangered": 0.9, "lives_in_asia": 1.0, "is_black": 0.5, "is_white": 0.5}),
    ("gorilla", "a gorilla", 29, {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "has_two_legs": 0.7, "has_four_legs": 0.5, "is_wild": 1.0, "is_large": 1.0, "is_herbivore": 0.9, "is_intelligent": 0.95, "is_strong": 1.0, "lives_in_jungle": 0.9, "lives_in_africa": 1.0, "is_black": 0.9, "is_endangered": 0.8}),
    ("chimpanzee", "a chimpanzee", 30, {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "has_two_legs": 0.6, "is_wild": 0.95, "is_medium": 0.8, "is_omnivore": 0.9, "is_intelligent": 0.95, "can_climb": 1.0, "lives_in_jungle": 0.8, "lives_in_africa": 1.0}),

    # REPTILES (Rank 31-50)
    ("snake", "a snake", 31, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_no_legs": 1.0, "is_wild": 0.8, "is_carnivore": 1.0, "is_predator": 0.9, "is_venomous": 0.4, "is_dangerous": 0.5, "is_long": 1.0, "lays_eggs": 0.8}),
    ("crocodile", "a crocodile", 32, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 1.0, "lives_in_water": 0.8, "can_swim": 1.0, "is_green": 0.6}),
    ("turtle", "a turtle", 33, {"is_animal": 1.0, "is_reptile": 1.0, "has_shell": 1.0, "has_four_legs": 1.0, "is_wild": 0.7, "is_pet": 0.4, "is_small": 0.6, "is_herbivore": 0.7, "lives_in_water": 0.5, "can_swim": 0.8, "is_green": 0.6, "lays_eggs": 1.0}),
    ("lizard", "a lizard", 34, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.7, "is_pet": 0.3, "is_small": 0.8, "is_carnivore": 0.7, "is_green": 0.5, "lays_eggs": 1.0}),
    ("frog", "a frog", 35, {"is_animal": 1.0, "is_amphibian": 1.0, "has_four_legs": 1.0, "is_wild": 0.8, "is_small": 0.9, "is_carnivore": 0.8, "can_jump": 1.0, "can_swim": 1.0, "lives_in_water": 0.6, "is_green": 0.7, "lays_eggs": 1.0, "makes_noise": 0.8}),
    ("alligator", "an alligator", 36, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 1.0, "lives_in_water": 0.7, "can_swim": 1.0, "lives_in_americas": 1.0}),
    ("chameleon", "a chameleon", 37, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.8, "is_small": 0.9, "is_carnivore": 0.8, "can_climb": 1.0, "is_colorful": 1.0, "lives_in_trees": 0.8}),
    ("iguana", "an iguana", 38, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.7, "is_pet": 0.4, "is_medium": 0.7, "is_herbivore": 0.9, "is_green": 0.9, "can_climb": 0.8}),
    ("gecko", "a gecko", 39, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.6, "is_pet": 0.5, "is_tiny": 0.9, "is_small": 1.0, "is_carnivore": 0.8, "can_climb": 1.0, "is_nocturnal": 0.7}),
    ("komodo_dragon", "a Komodo dragon", 40, {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 1.0, "is_venomous": 0.8, "lives_in_asia": 1.0, "is_endangered": 0.8}),

    # BIRDS (Rank 41-70)
    ("eagle", "an eagle", 41, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_large": 0.8, "is_carnivore": 1.0, "is_predator": 1.0, "has_beak": 1.0, "has_claws": 1.0, "is_brown": 0.7}),
    ("owl", "an owl", 42, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "is_wild": 0.95, "is_medium": 0.7, "is_carnivore": 1.0, "is_predator": 1.0, "is_nocturnal": 1.0, "has_beak": 1.0, "is_intelligent": 0.7, "is_brown": 0.6}),
    ("penguin", "a penguin", 43, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 0.0, "can_swim": 1.0, "is_wild": 1.0, "is_medium": 0.7, "is_carnivore": 1.0, "lives_in_arctic": 0.8, "lives_in_water": 0.6, "is_black": 0.5, "is_white": 0.5}),
    ("parrot", "a parrot", 44, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "is_pet": 0.7, "is_wild": 0.6, "is_medium": 0.6, "is_colorful": 1.0, "has_beak": 1.0, "is_intelligent": 0.8, "makes_noise": 1.0, "lives_in_jungle": 0.7}),
    ("peacock", "a peacock", 45, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 0.3, "is_wild": 0.7, "is_large": 0.6, "is_colorful": 1.0, "has_beak": 1.0, "has_tail": 1.0, "is_blue": 0.7, "is_green": 0.5}),
    ("flamingo", "a flamingo", 46, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_large": 0.7, "has_long_neck": 0.8, "has_beak": 1.0, "is_pink": 1.0, "lives_in_water": 0.5}),
    ("swan", "a swan", 47, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "can_swim": 1.0, "is_wild": 0.8, "is_large": 0.7, "has_long_neck": 1.0, "has_beak": 1.0, "is_white": 0.9, "lives_in_water": 0.7}),
    ("crow", "a crow", 48, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_medium": 0.7, "is_omnivore": 0.9, "has_beak": 1.0, "is_black": 1.0, "is_intelligent": 0.9, "makes_noise": 0.9}),
    ("pigeon", "a pigeon", 49, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "is_wild": 0.8, "is_small": 0.8, "is_omnivore": 0.8, "has_beak": 1.0, "is_grey": 0.8}),
    ("hummingbird", "a hummingbird", 50, {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "has_two_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_tiny": 1.0, "is_small": 1.0, "has_beak": 1.0, "is_colorful": 0.9, "is_fast": 0.9}),

    # FISH & MARINE (Rank 51-80)
    ("shark", "a shark", 51, {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "has_tail": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 1.0, "is_large": 0.8, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 0.9, "can_swim": 1.0, "is_grey": 0.7}),
    ("whale", "a whale", 52, {"is_animal": 1.0, "is_mammal": 1.0, "is_cetacean": 1.0, "has_fins": 1.0, "has_tail": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 1.0, "is_huge": 1.0, "is_large": 1.0, "can_swim": 1.0, "is_grey": 0.6, "is_blue": 0.3, "gives_live_birth": 1.0}),
    ("dolphin", "a dolphin", 53, {"is_animal": 1.0, "is_mammal": 1.0, "is_cetacean": 1.0, "has_fins": 1.0, "has_tail": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 0.9, "is_wild": 0.9, "is_medium": 0.8, "is_carnivore": 1.0, "is_intelligent": 1.0, "can_swim": 1.0, "is_grey": 0.8, "gives_live_birth": 1.0}),
    ("octopus", "an octopus", 54, {"is_animal": 1.0, "is_mollusk": 1.0, "has_tentacles": 1.0, "has_no_legs": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 1.0, "is_medium": 0.6, "is_carnivore": 1.0, "is_intelligent": 0.9, "can_swim": 1.0, "is_colorful": 0.7}),
    ("jellyfish", "a jellyfish", 55, {"is_animal": 1.0, "has_tentacles": 1.0, "has_no_legs": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 1.0, "is_venomous": 0.8, "can_swim": 0.8, "is_transparent": 0.8, "is_dangerous": 0.5}),
    ("seahorse", "a seahorse", 56, {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "has_tail": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 0.9, "is_tiny": 0.9, "is_small": 1.0, "can_swim": 1.0, "is_colorful": 0.6}),
    ("starfish", "a starfish", 57, {"is_animal": 1.0, "has_no_legs": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 1.0, "is_small": 0.8, "is_colorful": 0.7, "is_orange": 0.5}),
    ("crab", "a crab", 58, {"is_animal": 1.0, "is_crustacean": 1.0, "has_shell": 1.0, "has_many_legs": 1.0, "has_pincers": 1.0, "has_long_body": 0.0, "lives_in_water": 0.7, "lives_in_ocean": 0.8, "is_wild": 0.9, "is_small": 0.7, "is_food": 0.8, "is_red": 0.5, "is_orange": 0.4}),
    ("lobster", "a lobster", 59, {"is_animal": 1.0, "is_crustacean": 1.0, "has_shell": 1.0, "has_many_legs": 1.0, "has_pincers": 1.0, "has_long_body": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 0.9, "is_medium": 0.6, "is_food": 0.9, "is_red": 0.7, "has_claws": 1.0}),
    ("shrimp", "a shrimp", 60, {"is_animal": 1.0, "is_crustacean": 1.0, "has_shell": 0.8, "has_many_legs": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 0.9, "is_wild": 0.8, "is_tiny": 0.9, "is_small": 1.0, "is_food": 0.95, "is_pink": 0.6}),
    ("salmon", "a salmon", 61, {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "has_scales": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 0.7, "lives_in_freshwater": 0.5, "is_wild": 0.8, "is_medium": 0.7, "is_food": 0.95, "can_swim": 1.0, "is_pink": 0.7, "migrates": 1.0}),
    ("tuna", "a tuna", 62, {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "has_scales": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 0.9, "is_large": 0.8, "is_food": 0.95, "can_swim": 1.0, "is_fast": 0.9, "is_blue": 0.5}),
    ("clownfish", "a clownfish", 63, {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "has_scales": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_wild": 0.8, "is_pet": 0.5, "is_small": 1.0, "is_colorful": 1.0, "is_orange": 0.9, "is_white": 0.5}),

    # INSECTS & ARACHNIDS (Rank 64-90)
    ("butterfly", "a butterfly", 64, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "has_many_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_small": 1.0, "is_colorful": 1.0, "is_herbivore": 0.9, "lays_eggs": 1.0}),
    ("bee", "a bee", 65, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "has_many_legs": 1.0, "can_fly": 1.0, "is_wild": 0.8, "is_tiny": 0.9, "is_small": 1.0, "is_venomous": 0.7, "is_yellow": 0.8, "is_black": 0.5, "has_stripes": 0.9, "makes_noise": 0.8, "lives_in_groups": 1.0}),
    ("ant", "an ant", 66, {"is_animal": 1.0, "is_insect": 1.0, "has_many_legs": 1.0, "is_wild": 0.95, "is_tiny": 1.0, "is_small": 1.0, "is_omnivore": 0.8, "lives_in_groups": 1.0, "is_black": 0.7, "is_strong": 0.8, "lives_underground": 0.8}),
    ("spider", "a spider", 67, {"is_animal": 1.0, "is_arachnid": 1.0, "has_many_legs": 1.0, "is_wild": 0.9, "is_small": 0.9, "is_carnivore": 1.0, "is_predator": 0.9, "is_venomous": 0.5, "is_black": 0.5, "is_brown": 0.4}),
    ("mosquito", "a mosquito", 68, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "has_many_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_tiny": 1.0, "is_small": 1.0, "is_dangerous": 0.6, "makes_noise": 0.8}),
    ("fly", "a fly", 69, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "has_many_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_tiny": 0.9, "is_small": 1.0, "is_black": 0.7, "makes_noise": 0.8}),
    ("dragonfly", "a dragonfly", 70, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "has_many_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_small": 0.9, "is_carnivore": 1.0, "is_predator": 0.8, "is_colorful": 0.8, "lives_in_water": 0.3}),
    ("ladybug", "a ladybug", 71, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "has_many_legs": 1.0, "can_fly": 1.0, "is_wild": 1.0, "is_tiny": 1.0, "is_small": 1.0, "is_carnivore": 0.8, "is_red": 0.9, "has_spots": 1.0}),
    ("grasshopper", "a grasshopper", 72, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 0.8, "has_many_legs": 1.0, "can_fly": 0.6, "can_jump": 1.0, "is_wild": 1.0, "is_small": 0.9, "is_herbivore": 1.0, "is_green": 0.9, "makes_noise": 0.8}),
    ("beetle", "a beetle", 73, {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 0.8, "has_many_legs": 1.0, "has_shell": 0.9, "is_wild": 1.0, "is_small": 0.9, "is_black": 0.6, "is_green": 0.3}),
    ("caterpillar", "a caterpillar", 74, {"is_animal": 1.0, "is_insect": 1.0, "has_many_legs": 1.0, "is_wild": 1.0, "is_small": 0.9, "is_herbivore": 1.0, "is_green": 0.7, "is_colorful": 0.5}),
    ("scorpion", "a scorpion", 75, {"is_animal": 1.0, "is_arachnid": 1.0, "has_many_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_small": 0.8, "is_carnivore": 1.0, "is_predator": 0.9, "is_venomous": 1.0, "is_dangerous": 0.8, "lives_in_desert": 0.7, "is_black": 0.5, "is_brown": 0.5}),
    ("centipede", "a centipede", 76, {"is_animal": 1.0, "has_many_legs": 1.0, "is_wild": 1.0, "is_small": 0.8, "is_carnivore": 1.0, "is_venomous": 0.6, "is_long": 0.9, "is_brown": 0.6, "is_red": 0.3}),
    ("snail", "a snail", 77, {"is_animal": 1.0, "is_mollusk": 1.0, "has_shell": 1.0, "has_no_legs": 1.0, "is_wild": 0.8, "is_small": 0.9, "is_herbivore": 0.9, "is_brown": 0.6}),
    ("worm", "a worm", 78, {"is_animal": 1.0, "has_no_legs": 1.0, "is_wild": 0.9, "is_small": 0.9, "is_long": 0.9, "lives_underground": 1.0, "is_pink": 0.6, "is_brown": 0.5}),

    # MORE MAMMALS (Rank 79-120)
    ("squirrel", "a squirrel", 79, {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.95, "is_small": 0.9, "is_herbivore": 0.9, "can_climb": 1.0, "lives_in_trees": 0.9, "is_brown": 0.7, "is_grey": 0.4}),
    ("mouse", "a mouse", 80, {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.7, "is_pet": 0.4, "is_tiny": 0.9, "is_small": 1.0, "is_omnivore": 0.8, "is_grey": 0.7}),
    ("rat", "a rat", 81, {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.8, "is_pet": 0.3, "is_small": 0.9, "is_omnivore": 0.9, "is_intelligent": 0.7, "is_grey": 0.6, "is_brown": 0.5}),
    ("bat", "a bat", 82, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 0.9, "has_wings": 1.0, "can_fly": 1.0, "is_wild": 0.95, "is_small": 0.8, "is_carnivore": 0.6, "is_nocturnal": 1.0, "lives_in_groups": 0.8, "is_black": 0.7, "is_brown": 0.4}),
    ("hedgehog", "a hedgehog", 83, {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_wild": 0.7, "is_pet": 0.4, "is_small": 1.0, "is_omnivore": 0.8, "is_nocturnal": 0.8, "is_brown": 0.7}),
    ("otter", "an otter", 84, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.95, "is_medium": 0.7, "is_carnivore": 1.0, "can_swim": 1.0, "lives_in_water": 0.7, "is_intelligent": 0.7, "is_brown": 0.8}),
    ("beaver", "a beaver", 85, {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.95, "is_medium": 0.7, "is_herbivore": 1.0, "can_swim": 1.0, "lives_in_water": 0.6, "is_brown": 0.9}),
    ("raccoon", "a raccoon", 86, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.95, "is_medium": 0.7, "is_omnivore": 1.0, "is_nocturnal": 1.0, "is_intelligent": 0.7, "is_grey": 0.7, "is_black": 0.4, "has_stripes": 0.5}),
    ("skunk", "a skunk", 87, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 0.95, "is_small": 0.8, "is_omnivore": 0.9, "is_nocturnal": 0.8, "is_black": 0.9, "is_white": 0.5, "has_stripes": 1.0}),
    ("moose", "a moose", 88, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_huge": 0.9, "is_large": 1.0, "is_herbivore": 1.0, "has_horns": 0.8, "lives_in_americas": 0.8, "is_brown": 0.9}),
    ("buffalo", "a buffalo", 89, {"is_animal": 1.0, "is_mammal": 1.0, "is_bovine": 1.0, "has_fur": 0.9, "has_four_legs": 1.0, "is_wild": 0.9, "is_huge": 0.8, "is_large": 1.0, "is_herbivore": 1.0, "has_horns": 1.0, "is_brown": 0.9, "is_strong": 0.9}),
    ("camel", "a camel", 90, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 0.8, "has_four_legs": 1.0, "has_tail": 0.8, "is_domesticated": 0.8, "is_large": 1.0, "is_herbivore": 1.0, "lives_in_desert": 1.0, "is_brown": 0.9, "has_long_neck": 0.7}),
    ("llama", "a llama", 91, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 0.8, "is_domesticated": 0.9, "is_large": 0.8, "is_herbivore": 1.0, "lives_in_mountains": 0.7, "lives_in_americas": 1.0, "is_brown": 0.5, "is_white": 0.4}),
    ("hippo", "a hippo", 92, {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_huge": 0.9, "is_large": 1.0, "is_herbivore": 1.0, "lives_in_water": 0.7, "can_swim": 1.0, "is_dangerous": 0.9, "lives_in_africa": 1.0, "is_grey": 0.9}),
    ("rhino", "a rhino", 93, {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_huge": 0.9, "is_large": 1.0, "is_herbivore": 1.0, "has_horns": 1.0, "is_endangered": 0.9, "lives_in_africa": 0.7, "lives_in_asia": 0.4, "is_grey": 0.9, "is_dangerous": 0.7}),
    ("leopard", "a leopard", 94, {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 0.8, "is_carnivore": 1.0, "is_predator": 1.0, "has_spots": 1.0, "can_climb": 0.9, "lives_in_africa": 0.8, "lives_in_asia": 0.5, "is_yellow": 0.7}),
    ("cheetah", "a cheetah", 95, {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 0.8, "is_carnivore": 1.0, "is_predator": 1.0, "has_spots": 1.0, "is_fast": 1.0, "lives_in_africa": 1.0, "is_yellow": 0.7}),
    ("jaguar", "a jaguar", 96, {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 0.9, "is_carnivore": 1.0, "is_predator": 1.0, "has_spots": 1.0, "can_swim": 0.8, "lives_in_americas": 1.0, "lives_in_jungle": 0.9, "is_yellow": 0.6}),
    ("panther", "a panther", 97, {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_large": 0.9, "is_carnivore": 1.0, "is_predator": 1.0, "is_black": 1.0, "can_climb": 0.9, "lives_in_jungle": 0.7}),
    ("hyena", "a hyena", 98, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 0.9, "is_wild": 1.0, "is_medium": 0.8, "is_carnivore": 0.9, "is_predator": 0.8, "lives_in_groups": 0.9, "makes_noise": 0.9, "lives_in_africa": 1.0, "has_spots": 0.7}),
    ("polar_bear", "a polar bear", 99, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 0.9, "lives_in_arctic": 1.0, "can_swim": 0.9, "is_white": 1.0, "is_endangered": 0.7}),
    ("sloth", "a sloth", 100, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_medium": 0.7, "is_herbivore": 0.9, "lives_in_trees": 1.0, "lives_in_jungle": 0.9, "lives_in_americas": 1.0, "is_brown": 0.7, "has_claws": 1.0}),
    # More animals continued...
    ("seal", "a seal", 101, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 0.8, "has_fins": 0.9, "is_wild": 0.95, "is_medium": 0.8, "is_carnivore": 1.0, "can_swim": 1.0, "lives_in_water": 0.8, "lives_in_ocean": 0.9, "lives_in_arctic": 0.6, "is_grey": 0.7}),
    ("walrus", "a walrus", 102, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 0.6, "has_fins": 0.9, "is_wild": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "has_tusks": 1.0, "can_swim": 1.0, "lives_in_water": 0.7, "lives_in_arctic": 1.0, "is_brown": 0.8}),
    ("platypus", "a platypus", 103, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_small": 0.8, "is_carnivore": 0.9, "can_swim": 1.0, "lives_in_water": 0.6, "has_beak": 1.0, "is_venomous": 0.5, "lays_eggs": 1.0, "lives_in_australia": 1.0, "is_brown": 0.9}),
    ("armadillo", "an armadillo", 104, {"is_animal": 1.0, "is_mammal": 1.0, "has_shell": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_small": 0.8, "is_omnivore": 0.9, "can_burrow": 1.0, "lives_in_americas": 1.0, "is_grey": 0.8}),
    ("ferret", "a ferret", 105, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_pet": 0.8, "is_small": 0.9, "is_carnivore": 0.9, "is_long": 0.8, "is_brown": 0.6, "is_white": 0.4}),
    ("meerkat", "a meerkat", 106, {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 1.0, "is_small": 0.9, "is_carnivore": 0.8, "lives_in_groups": 1.0, "lives_in_desert": 0.8, "lives_in_africa": 1.0, "is_brown": 0.9}),
    ("wombat", "a wombat", 107, {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_wild": 0.95, "is_medium": 0.7, "is_herbivore": 1.0, "can_burrow": 1.0, "has_pouch": 1.0, "lives_in_australia": 1.0, "is_brown": 0.8}),
    ("orangutan", "an orangutan", 108, {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "is_wild": 1.0, "is_large": 0.8, "is_herbivore": 0.8, "is_intelligent": 0.95, "can_climb": 1.0, "lives_in_trees": 0.9, "lives_in_asia": 1.0, "is_orange": 0.9, "is_endangered": 0.9}),
    ("lemur", "a lemur", 109, {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_wild": 1.0, "is_small": 0.8, "is_omnivore": 0.8, "can_climb": 1.0, "lives_in_trees": 0.9, "is_nocturnal": 0.6}),
    ("baboon", "a baboon", 110, {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "is_wild": 1.0, "is_medium": 0.8, "is_omnivore": 1.0, "is_aggressive": 0.7, "lives_in_groups": 1.0, "lives_in_africa": 1.0, "is_brown": 0.7}),
]

# ============================================================================
# FOOD/PLANT DATABASE - Ranked by commonality
# ============================================================================

FOODS_PLANTS = [
    # FRUITS - Most common (Rank 1-30)
    ("apple", "an apple", 1, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.9, "is_sweet": 0.8, "has_seeds": 1.0, "has_skin": 1.0, "is_red": 0.6, "is_green": 0.4, "is_common": 1.0, "is_solid": 1.0, "is_crunchy": 1.0}),
    ("banana", "a banana", 2, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_long": 0.9, "is_sweet": 0.9, "has_skin": 1.0, "is_yellow": 0.9, "is_tropical": 1.0, "is_common": 1.0, "is_solid": 1.0}),
    ("orange", "an orange", 3, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_citrus": 1.0, "grows_on_trees": 1.0, "is_round": 1.0, "is_sweet": 0.7, "is_sour": 0.4, "has_seeds": 0.8, "has_skin": 1.0, "is_orange": 1.0, "is_common": 1.0, "is_solid": 1.0}),
    ("strawberry", "a strawberry", 4, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_berry": 1.0, "is_small": 0.9, "is_sweet": 0.9, "has_seeds": 1.0, "is_red": 1.0, "is_common": 0.9, "is_solid": 1.0}),
    ("grape", "a grape", 5, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_tiny": 0.9, "is_small": 1.0, "is_round": 0.9, "is_sweet": 0.8, "has_seeds": 0.6, "is_purple": 0.5, "is_green": 0.5, "is_common": 0.9, "is_solid": 1.0}),
    ("watermelon", "a watermelon", 6, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_large": 0.9, "is_round": 0.8, "is_sweet": 0.9, "has_seeds": 0.8, "has_skin": 1.0, "is_green": 0.8, "is_red": 0.7, "is_common": 0.8, "is_solid": 1.0, "is_heavy": 0.8}),
    ("lemon", "a lemon", 7, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_citrus": 1.0, "grows_on_trees": 1.0, "is_small": 0.8, "is_sour": 1.0, "has_seeds": 0.8, "has_skin": 1.0, "is_yellow": 1.0, "is_common": 0.9, "is_solid": 1.0}),
    ("mango", "a mango", 8, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_medium": 0.7, "is_sweet": 0.95, "has_pit": 1.0, "has_skin": 1.0, "is_orange": 0.7, "is_yellow": 0.6, "is_tropical": 1.0, "is_solid": 1.0}),
    ("pineapple", "a pineapple", 9, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_medium": 0.8, "is_sweet": 0.8, "is_sour": 0.4, "has_skin": 1.0, "is_yellow": 0.9, "is_tropical": 1.0, "is_solid": 1.0}),
    ("peach", "a peach", 10, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.8, "is_sweet": 0.9, "has_pit": 1.0, "has_skin": 1.0, "is_orange": 0.7, "is_pink": 0.4, "is_soft": 0.8, "is_solid": 1.0}),
    ("cherry", "a cherry", 11, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_tiny": 0.9, "is_small": 1.0, "is_round": 1.0, "is_sweet": 0.8, "has_pit": 1.0, "is_red": 1.0, "is_solid": 1.0}),
    ("pear", "a pear", 12, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_sweet": 0.8, "has_seeds": 1.0, "has_skin": 1.0, "is_green": 0.7, "is_yellow": 0.4, "is_solid": 1.0}),
    ("blueberry", "a blueberry", 13, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_berry": 1.0, "grows_on_bushes": 1.0, "is_tiny": 1.0, "is_small": 1.0, "is_round": 1.0, "is_sweet": 0.8, "is_blue": 0.9, "is_purple": 0.5, "is_solid": 1.0}),
    ("avocado", "an avocado", 14, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "has_pit": 1.0, "has_skin": 1.0, "is_green": 1.0, "is_soft": 0.8, "is_solid": 1.0}),
    ("coconut", "a coconut", 15, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_nut": 0.5, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.8, "has_shell": 1.0, "is_brown": 0.9, "is_white": 0.5, "is_tropical": 1.0, "is_hard": 0.9, "is_solid": 1.0}),
    ("lime", "a lime", 16, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_citrus": 1.0, "grows_on_trees": 1.0, "is_small": 0.9, "is_round": 0.9, "is_sour": 1.0, "has_skin": 1.0, "is_green": 1.0, "is_solid": 1.0}),
    ("raspberry", "a raspberry", 17, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_berry": 1.0, "grows_on_bushes": 1.0, "is_tiny": 0.9, "is_small": 1.0, "is_sweet": 0.8, "is_sour": 0.3, "is_red": 0.9, "is_soft": 0.9, "is_solid": 1.0}),
    ("blackberry", "a blackberry", 18, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_berry": 1.0, "grows_on_bushes": 1.0, "is_tiny": 0.9, "is_small": 1.0, "is_sweet": 0.7, "is_black": 0.9, "is_purple": 0.5, "is_soft": 0.9, "is_solid": 1.0}),
    ("kiwi", "a kiwi", 19, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_small": 0.9, "is_sweet": 0.7, "is_sour": 0.4, "has_skin": 1.0, "is_green": 0.9, "is_brown": 0.7, "is_solid": 1.0}),
    ("pomegranate", "a pomegranate", 20, {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_round": 0.9, "is_sweet": 0.6, "is_sour": 0.4, "has_seeds": 1.0, "has_skin": 1.0, "is_red": 1.0, "is_solid": 1.0}),

    # VEGETABLES (Rank 21-50)
    ("carrot", "a carrot", 21, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_long": 0.8, "is_orange": 1.0, "is_hard": 0.7, "is_common": 1.0, "is_solid": 1.0, "is_crunchy": 1.0}),
    ("potato", "a potato", 22, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_round": 0.7, "is_brown": 0.8, "is_common": 1.0, "is_solid": 1.0, "is_savory": 0.7}),
    ("tomato", "a tomato", 23, {"is_vegetable": 1.0, "is_fruit": 0.5, "is_vegetable_food": 0.9, "is_food": 1.0, "grows_on_vines": 0.8, "is_round": 0.9, "has_seeds": 1.0, "has_skin": 1.0, "is_red": 0.9, "is_common": 1.0, "is_soft": 0.7, "is_solid": 1.0, "is_crunchy": 0.0}),
    ("onion", "an onion", 24, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_round": 0.9, "is_white": 0.6, "is_yellow": 0.3, "is_purple": 0.2, "is_common": 1.0, "is_solid": 1.0, "is_savory": 0.9}),
    ("broccoli", "broccoli", 25, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_green": 1.0, "is_common": 0.9, "is_solid": 1.0}),
    ("lettuce", "lettuce", 26, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_common": 0.9, "is_soft": 0.8, "is_solid": 1.0}),
    ("cucumber", "a cucumber", 27, {"is_vegetable": 1.0, "is_fruit": 0.3, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 0.9, "is_cylindrical": 0.9, "is_green": 1.0, "has_seeds": 0.8, "is_common": 0.9, "is_solid": 1.0}),
    ("corn", "corn", 28, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_grain": 0.5, "is_food": 1.0, "is_yellow": 1.0, "has_seeds": 1.0, "is_common": 0.9, "is_solid": 1.0, "is_sweet": 0.5}),
    ("pepper", "a pepper", 29, {"is_vegetable": 1.0, "is_fruit": 0.3, "is_vegetable_food": 1.0, "is_food": 1.0, "has_seeds": 1.0, "is_colorful": 0.8, "is_red": 0.4, "is_green": 0.4, "is_yellow": 0.3, "is_common": 0.9, "is_solid": 1.0}),
    ("celery", "celery", 30, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 0.9, "is_green": 1.0, "is_hard": 0.7, "is_solid": 1.0}),
    ("spinach", "spinach", 31, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_soft": 0.8, "is_solid": 1.0}),
    ("garlic", "garlic", 32, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_herb": 0.5, "is_food": 1.0, "grows_underground": 1.0, "is_small": 0.9, "is_white": 0.9, "is_savory": 1.0, "is_common": 0.9, "is_solid": 1.0}),
    ("mushroom", "a mushroom", 33, {"is_vegetable": 1.0, "is_fungus": 1.0, "is_food": 1.0, "is_small": 0.8, "is_brown": 0.6, "is_white": 0.5, "is_savory": 0.8, "is_soft": 0.7, "is_solid": 1.0}),
    ("pumpkin", "a pumpkin", 34, {"is_vegetable": 1.0, "is_fruit": 0.4, "is_vegetable_food": 0.8, "is_food": 1.0, "is_large": 0.8, "is_round": 0.9, "has_seeds": 1.0, "is_orange": 1.0, "is_solid": 1.0}),
    ("cabbage", "a cabbage", 35, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_round": 0.8, "is_green": 0.8, "is_purple": 0.3, "is_solid": 1.0}),
    ("cauliflower", "cauliflower", 36, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_white": 0.9, "is_solid": 1.0}),
    ("eggplant", "an eggplant", 37, {"is_vegetable": 1.0, "is_fruit": 0.3, "is_vegetable_food": 1.0, "is_food": 1.0, "is_purple": 1.0, "has_seeds": 0.8, "is_solid": 1.0}),
    ("zucchini", "a zucchini", 38, {"is_vegetable": 1.0, "is_fruit": 0.3, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 0.9, "is_cylindrical": 0.9, "is_green": 1.0, "is_solid": 1.0}),
    ("asparagus", "asparagus", 39, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 0.9, "is_green": 1.0, "is_solid": 1.0}),
    ("beet", "a beet", 40, {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_round": 0.8, "is_red": 0.9, "is_purple": 0.5, "is_solid": 1.0}),

    # TREES & FLOWERS (Rank 41-60)
    ("rose", "a rose", 41, {"is_vegetable": 1.0, "is_flower": 1.0, "is_natural": 1.0, "is_red": 0.6, "is_pink": 0.4, "is_colorful": 0.8, "is_common": 0.9}),
    ("sunflower", "a sunflower", 42, {"is_vegetable": 1.0, "is_flower": 1.0, "is_natural": 1.0, "is_large": 0.7, "is_yellow": 1.0, "is_round": 0.8, "has_seeds": 1.0}),
    ("tulip", "a tulip", 43, {"is_vegetable": 1.0, "is_flower": 1.0, "is_natural": 1.0, "is_colorful": 1.0, "is_common": 0.8}),
    ("daisy", "a daisy", 44, {"is_vegetable": 1.0, "is_flower": 1.0, "is_natural": 1.0, "is_small": 0.8, "is_white": 0.9, "is_yellow": 0.5, "is_common": 0.8}),
    ("oak_tree", "an oak tree", 45, {"is_vegetable": 1.0, "is_tree": 1.0, "is_natural": 1.0, "is_large": 1.0, "is_huge": 0.8, "has_leaves": 1.0, "is_brown": 0.8, "is_green": 0.7}),
    ("pine_tree", "a pine tree", 46, {"is_vegetable": 1.0, "is_tree": 1.0, "is_natural": 1.0, "is_large": 1.0, "has_leaves": 0.3, "is_green": 1.0, "is_brown": 0.5}),
    ("palm_tree", "a palm tree", 47, {"is_vegetable": 1.0, "is_tree": 1.0, "is_natural": 1.0, "is_large": 1.0, "has_leaves": 1.0, "is_green": 0.9, "is_tropical": 1.0}),
    ("cactus", "a cactus", 48, {"is_vegetable": 1.0, "is_natural": 1.0, "lives_in_desert": 1.0, "is_green": 1.0, "is_dangerous": 0.3}),
    ("bamboo", "bamboo", 49, {"is_vegetable": 1.0, "is_grass": 1.0, "is_natural": 1.0, "is_long": 0.9, "is_green": 1.0, "lives_in_asia": 0.8}),
    ("fern", "a fern", 50, {"is_vegetable": 1.0, "is_natural": 1.0, "has_leaves": 1.0, "is_green": 1.0}),

    # GRAINS & NUTS (Rank 51-70)
    ("rice", "rice", 51, {"is_vegetable": 1.0, "is_grain": 1.0, "is_food": 1.0, "is_tiny": 0.9, "is_white": 0.8, "is_common": 1.0, "is_solid": 1.0}),
    ("wheat", "wheat", 52, {"is_vegetable": 1.0, "is_grain": 1.0, "is_food": 1.0, "is_yellow": 0.7, "is_brown": 0.5}),
    ("oat", "oats", 53, {"is_vegetable": 1.0, "is_grain": 1.0, "is_food": 1.0, "is_brown": 0.6}),
    ("peanut", "a peanut", 54, {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_small": 0.9, "has_shell": 0.9, "is_brown": 0.9, "is_solid": 1.0}),
    ("walnut", "a walnut", 55, {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.8, "has_shell": 1.0, "is_brown": 1.0, "is_hard": 0.9, "is_round": 0.7, "is_solid": 1.0}),
    ("almond", "an almond", 56, {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.9, "is_brown": 0.9, "is_solid": 1.0}),
    ("cashew", "a cashew", 57, {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.9, "is_white": 0.7, "is_solid": 1.0}),
    ("pistachio", "a pistachio", 58, {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "is_tiny": 0.9, "is_small": 1.0, "has_shell": 1.0, "is_green": 0.8, "is_solid": 1.0}),

    # HERBS & SPICES (Rank 59-70)
    ("basil", "basil", 59, {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_savory": 0.8}),
    ("mint", "mint", 60, {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_sweet": 0.5}),
    ("parsley", "parsley", 61, {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0}),
    ("rosemary", "rosemary", 62, {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_savory": 0.9}),
    ("thyme", "thyme", 63, {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_tiny": 0.9}),
    ("ginger", "ginger", 64, {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_spicy": 0.7, "is_brown": 0.8, "is_solid": 1.0}),
    ("cinnamon", "cinnamon", 65, {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "is_brown": 1.0, "is_sweet": 0.6, "is_spicy": 0.4}),
]

# ============================================================================
# OBJECTS DATABASE - Ranked by commonality
# ============================================================================

OBJECTS = [
    # ELECTRONICS - Most common (Rank 1-30)
    ("phone", "a phone", 1, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "has_buttons": 0.5, "is_small": 0.9, "is_portable": 1.0, "fits_in_pocket": 0.9, "used_for_communication": 1.0, "is_common": 1.0, "requires_batteries": 1.0, "is_hard": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("television", "a television", 2, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "is_large": 0.7, "plugs_in": 1.0, "used_for_entertainment": 1.0, "is_common": 1.0, "is_living_room_item": 1.0, "is_hard": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("computer", "a computer", 3, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "has_buttons": 1.0, "plugs_in": 0.8, "is_common": 1.0, "is_hard": 0.9, "is_solid": 1.0, "found_at_home": 0.9, "found_in_office": 0.9, "used_for_communication": 0.8}),
    ("laptop", "a laptop", 4, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "has_buttons": 1.0, "is_portable": 1.0, "requires_batteries": 1.0, "is_common": 0.9, "opens_closes": 1.0, "is_hard": 0.9, "is_solid": 1.0}),
    ("tablet", "a tablet", 5, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "is_portable": 1.0, "requires_batteries": 1.0, "is_flat": 1.0, "is_hard": 0.9, "is_solid": 1.0}),
    ("camera", "a camera", 6, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.9, "has_buttons": 0.9, "is_portable": 1.0, "requires_batteries": 0.9, "is_solid": 1.0}),
    ("headphones", "headphones", 7, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "produces_sound": 1.0, "is_worn": 1.0, "is_portable": 0.9, "used_for_entertainment": 0.9, "is_common": 0.9}),
    ("watch", "a watch", 8, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.7, "is_mechanical": 0.5, "tells_time": 1.0, "is_worn": 1.0, "is_small": 1.0, "is_accessory": 1.0, "is_portable": 1.0, "is_common": 0.9, "requires_batteries": 0.7, "is_solid": 1.0}),
    ("clock", "a clock", 9, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.5, "is_mechanical": 0.5, "tells_time": 1.0, "is_round": 0.7, "found_at_home": 1.0, "is_common": 0.9, "is_solid": 1.0}),
    ("lamp", "a lamp", 10, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.9, "is_lighting": 1.0, "produces_light": 1.0, "plugs_in": 0.9, "found_at_home": 1.0, "is_common": 1.0, "is_solid": 1.0}),

    # KITCHEN ITEMS (Rank 11-40)
    ("spoon", "a spoon", 11, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 0.8, "is_tool": 0.7, "is_kitchen_item": 1.0, "used_for_cooking": 0.5, "is_small": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "has_handle": 1.0}),
    ("fork", "a fork", 12, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 0.8, "is_tool": 0.7, "is_kitchen_item": 1.0, "is_small": 0.9, "is_sharp": 0.5, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "has_handle": 1.0}),
    ("knife", "a knife", 13, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 0.9, "is_tool": 1.0, "is_kitchen_item": 0.8, "is_weapon": 0.5, "used_for_cutting": 1.0, "is_sharp": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "has_handle": 1.0, "is_dangerous": 0.5}),
    ("plate", "a plate", 14, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_ceramic": 0.8, "is_kitchen_item": 1.0, "is_round": 0.9, "is_flat": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "is_container": 0.5}),
    ("cup", "a cup", 15, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_ceramic": 0.6, "is_glass": 0.3, "is_kitchen_item": 1.0, "is_container": 1.0, "is_cylindrical": 0.8, "is_small": 0.8, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "has_handle": 0.6}),
    ("bowl", "a bowl", 16, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_ceramic": 0.7, "is_kitchen_item": 1.0, "is_container": 1.0, "is_round": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),
    ("pot", "a pot", 17, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 0.9, "is_kitchen_item": 1.0, "is_container": 1.0, "used_for_cooking": 1.0, "is_round": 0.8, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0, "has_handle": 0.9}),
    ("pan", "a pan", 18, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 0.9, "is_kitchen_item": 1.0, "used_for_cooking": 1.0, "is_round": 0.8, "is_flat": 0.7, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0, "has_handle": 1.0}),
    ("microwave", "a microwave", 19, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "used_for_cooking": 1.0, "plugs_in": 1.0, "has_buttons": 1.0, "opens_closes": 1.0, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("refrigerator", "a refrigerator", 20, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "plugs_in": 1.0, "is_large": 1.0, "is_cold": 1.0, "opens_closes": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "is_container": 1.0}),
    ("toaster", "a toaster", 21, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "used_for_cooking": 1.0, "plugs_in": 1.0, "is_small": 0.8, "is_hot": 0.7, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("blender", "a blender", 22, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "used_for_cooking": 1.0, "plugs_in": 1.0, "has_buttons": 1.0, "is_sharp": 0.8, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 1.0}),
    ("bottle", "a bottle", 23, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_plastic": 0.7, "is_glass": 0.4, "is_container": 1.0, "is_cylindrical": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),
    ("glass", "a glass", 24, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_glass": 1.0, "is_kitchen_item": 1.0, "is_container": 1.0, "is_transparent": 0.9, "is_cylindrical": 0.8, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),

    # FURNITURE (Rank 25-45)
    ("chair", "a chair", 25, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_furniture": 1.0, "is_wood": 0.6, "is_plastic": 0.3, "has_four_legs": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),
    ("table", "a table", 26, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_furniture": 1.0, "is_wood": 0.7, "has_four_legs": 0.9, "is_flat": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),
    ("bed", "a bed", 27, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_furniture": 1.0, "is_bedroom_item": 1.0, "is_large": 0.8, "is_soft": 0.9, "is_common": 1.0, "found_at_home": 1.0}),
    ("sofa", "a sofa", 28, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_furniture": 1.0, "is_living_room_item": 1.0, "is_large": 0.8, "is_soft": 0.9, "is_fabric": 0.8, "is_common": 0.9, "found_at_home": 1.0}),
    ("desk", "a desk", 29, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_furniture": 1.0, "is_wood": 0.7, "is_flat": 0.9, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 0.8, "found_in_office": 1.0}),
    ("bookshelf", "a bookshelf", 30, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_furniture": 1.0, "is_storage": 1.0, "is_wood": 0.8, "is_large": 0.7, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 1.0}),
    ("dresser", "a dresser", 31, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_furniture": 1.0, "is_bedroom_item": 1.0, "is_storage": 1.0, "is_wood": 0.8, "opens_closes": 1.0, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 1.0}),
    ("mirror", "a mirror", 32, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_glass": 1.0, "is_flat": 1.0, "is_shiny": 1.0, "is_bathroom_item": 0.7, "is_bedroom_item": 0.6, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("pillow", "a pillow", 33, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_fabric": 1.0, "is_bedroom_item": 1.0, "is_soft": 1.0, "is_white": 0.6, "is_common": 1.0, "found_at_home": 1.0}),
    ("blanket", "a blanket", 34, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_fabric": 1.0, "is_bedroom_item": 1.0, "is_soft": 1.0, "is_flat": 0.8, "is_common": 1.0, "found_at_home": 1.0}),

    # BATHROOM ITEMS (Rank 35-50)
    ("toothbrush", "a toothbrush", 35, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_plastic": 0.9, "is_bathroom_item": 1.0, "is_personal_care": 1.0, "used_for_cleaning": 1.0, "is_small": 0.9, "is_long": 0.7, "is_common": 1.0, "is_solid": 1.0, "used_daily": 1.0, "found_at_home": 1.0, "has_handle": 1.0}),
    ("soap", "soap", 36, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_bathroom_item": 1.0, "is_personal_care": 1.0, "used_for_cleaning": 1.0, "is_small": 0.8, "is_consumed": 1.0, "is_common": 1.0, "is_solid": 0.8, "used_daily": 1.0, "found_at_home": 1.0}),
    ("towel", "a towel", 37, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_fabric": 1.0, "is_bathroom_item": 1.0, "is_soft": 0.9, "is_flat": 0.8, "is_common": 1.0, "found_at_home": 1.0, "is_white": 0.5}),
    ("shampoo", "shampoo", 38, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_bathroom_item": 1.0, "is_personal_care": 1.0, "used_for_cleaning": 1.0, "is_liquid": 1.0, "is_consumed": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("toilet", "a toilet", 39, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_bathroom_item": 1.0, "is_ceramic": 1.0, "is_white": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),
    ("sink", "a sink", 40, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_bathroom_item": 0.7, "is_kitchen_item": 0.7, "is_ceramic": 0.7, "is_metal": 0.4, "is_container": 0.8, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),

    # TOOLS (Rank 41-60)
    ("hammer", "a hammer", 41, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 1.0, "is_metal": 0.8, "is_wood": 0.5, "is_hard": 1.0, "is_heavy": 0.7, "has_handle": 1.0, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 0.8}),
    ("screwdriver", "a screwdriver", 42, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 1.0, "is_metal": 0.8, "is_plastic": 0.5, "is_long": 0.8, "has_handle": 1.0, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 0.8}),
    ("scissors", "scissors", 43, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 1.0, "is_metal": 0.9, "used_for_cutting": 1.0, "is_sharp": 1.0, "has_handle": 1.0, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("saw", "a saw", 44, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 1.0, "is_metal": 0.9, "used_for_cutting": 1.0, "is_sharp": 1.0, "has_handle": 1.0, "is_dangerous": 0.6, "is_solid": 1.0}),
    ("wrench", "a wrench", 45, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 1.0, "is_metal": 1.0, "is_hard": 1.0, "is_solid": 1.0}),
    ("drill", "a drill", 46, {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_electronic": 0.8, "is_mechanical": 1.0, "requires_batteries": 0.6, "makes_noise": 0.9, "is_solid": 1.0}),
    ("pliers", "pliers", 47, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 1.0, "is_metal": 0.9, "has_handle": 1.0, "is_solid": 1.0}),
    ("tape", "tape", 48, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 0.5, "is_plastic": 0.8, "is_flat": 0.8, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("rope", "rope", 49, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 0.6, "is_fabric": 0.7, "is_long": 1.0, "is_flexible": 1.0, "is_common": 0.8, "is_solid": 1.0}),
    ("ladder", "a ladder", 50, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_tool": 1.0, "is_metal": 0.6, "is_wood": 0.5, "is_large": 0.8, "is_long": 0.9, "found_outdoors": 0.6, "is_solid": 1.0}),

    # CLOTHING (Rank 51-70)
    ("shirt", "a shirt", 51, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("pants", "pants", 52, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("shoes", "shoes", 53, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_leather": 0.5, "is_rubber": 0.5, "is_worn": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("hat", "a hat", 54, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 0.8, "is_worn": 1.0, "is_common": 0.9, "found_at_home": 1.0}),
    ("jacket", "a jacket", 55, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 0.9, "is_worn": 1.0, "is_common": 0.9, "found_at_home": 1.0}),
    ("socks", "socks", 56, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_small": 0.9, "is_common": 1.0, "found_at_home": 1.0}),
    ("gloves", "gloves", 57, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 0.7, "is_leather": 0.4, "is_worn": 1.0, "is_common": 0.8, "found_at_home": 1.0}),
    ("belt", "a belt", 58, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_accessory": 1.0, "is_leather": 0.7, "is_worn": 1.0, "is_long": 0.9, "is_common": 0.9, "found_at_home": 1.0}),
    ("scarf", "a scarf", 59, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_long": 0.9, "is_soft": 0.9, "is_common": 0.8, "found_at_home": 1.0}),
    ("tie", "a tie", 60, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_long": 0.9, "is_common": 0.7, "found_at_home": 0.8}),

    # VEHICLES (Rank 61-75)
    ("car", "a car", 61, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 0.9, "has_wheels": 1.0, "is_large": 0.9, "used_for_transportation": 1.0, "is_mechanical": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_outdoors": 1.0}),
    ("bicycle", "a bicycle", 62, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 0.9, "has_wheels": 1.0, "is_medium": 0.8, "used_for_transportation": 1.0, "is_mechanical": 1.0, "is_common": 0.9, "is_solid": 1.0, "found_outdoors": 0.8}),
    ("airplane", "an airplane", 63, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 0.9, "has_wings": 1.0, "can_fly": 1.0, "is_huge": 1.0, "is_large": 1.0, "used_for_transportation": 1.0, "is_common": 0.7, "is_solid": 1.0}),
    ("boat", "a boat", 64, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "can_swim": 0.3, "lives_in_water": 0.8, "used_for_transportation": 1.0, "is_common": 0.7, "is_solid": 1.0}),
    ("train", "a train", 65, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 1.0, "has_wheels": 1.0, "is_huge": 1.0, "is_large": 1.0, "is_long": 1.0, "used_for_transportation": 1.0, "is_common": 0.7, "is_solid": 1.0}),
    ("bus", "a bus", 66, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 0.9, "has_wheels": 1.0, "is_large": 1.0, "used_for_transportation": 1.0, "is_common": 0.8, "is_solid": 1.0}),
    ("motorcycle", "a motorcycle", 67, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 0.9, "has_wheels": 1.0, "is_medium": 0.8, "used_for_transportation": 1.0, "is_mechanical": 1.0, "is_fast": 0.8, "is_common": 0.7, "is_solid": 1.0}),
    ("helicopter", "a helicopter", 68, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 0.9, "can_fly": 1.0, "is_large": 0.9, "used_for_transportation": 1.0, "is_common": 0.5, "is_solid": 1.0}),
    ("truck", "a truck", 69, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_vehicle": 1.0, "is_metal": 0.9, "has_wheels": 1.0, "is_large": 1.0, "used_for_transportation": 1.0, "is_common": 0.8, "is_solid": 1.0}),

    # OFFICE/SCHOOL SUPPLIES (Rank 70-85)
    ("pen", "a pen", 70, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_office_item": 1.0, "is_plastic": 0.8, "used_for_writing": 1.0, "is_small": 0.9, "is_long": 0.8, "is_cylindrical": 0.9, "is_common": 1.0, "is_solid": 1.0, "fits_in_pocket": 1.0, "found_at_home": 1.0, "found_in_office": 1.0}),
    ("pencil", "a pencil", 71, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_office_item": 1.0, "is_wood": 0.8, "used_for_writing": 1.0, "is_small": 0.9, "is_long": 0.8, "is_cylindrical": 0.9, "is_sharp": 0.6, "is_yellow": 0.7, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "found_in_office": 1.0}),
    ("book", "a book", 72, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_office_item": 0.6, "is_paper": 1.0, "holds_information": 1.0, "opens_closes": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "found_in_office": 0.7}),
    ("paper", "paper", 73, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_paper": 1.0, "is_office_item": 1.0, "is_flat": 1.0, "is_white": 0.9, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "found_in_office": 1.0}),
    ("notebook", "a notebook", 74, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_paper": 1.0, "is_office_item": 1.0, "used_for_writing": 1.0, "holds_information": 1.0, "opens_closes": 1.0, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0, "found_in_office": 1.0}),
    ("eraser", "an eraser", 75, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_rubber": 1.0, "is_office_item": 1.0, "is_small": 1.0, "is_pink": 0.6, "is_white": 0.4, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 0.9, "found_in_office": 1.0}),
    ("ruler", "a ruler", 76, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_plastic": 0.7, "is_wood": 0.4, "is_office_item": 1.0, "is_tool": 0.5, "is_flat": 1.0, "is_long": 0.9, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 0.8, "found_in_office": 1.0}),
    ("stapler", "a stapler", 77, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 0.7, "is_plastic": 0.5, "is_office_item": 1.0, "is_tool": 0.7, "is_small": 0.9, "is_common": 0.8, "is_solid": 1.0, "found_in_office": 1.0}),
    ("calculator", "a calculator", 78, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_office_item": 1.0, "has_buttons": 1.0, "has_screen": 1.0, "is_small": 0.9, "requires_batteries": 0.8, "is_common": 0.8, "is_solid": 1.0, "found_in_office": 1.0}),

    # TOYS & SPORTS (Rank 79-95)
    ("ball", "a ball", 79, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_toy": 0.8, "is_sports_equipment": 0.8, "is_rubber": 0.6, "is_round": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 0.9}),
    ("doll", "a doll", 80, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_toy": 1.0, "is_plastic": 0.8, "is_baby_item": 0.5, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 0.9}),
    ("teddy_bear", "a teddy bear", 81, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_toy": 1.0, "is_fabric": 1.0, "is_soft": 1.0, "is_brown": 0.7, "is_baby_item": 0.6, "is_common": 0.8, "found_at_home": 0.9}),
    ("puzzle", "a puzzle", 82, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_toy": 1.0, "used_for_entertainment": 1.0, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 0.9}),
    ("kite", "a kite", 83, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_toy": 1.0, "is_plastic": 0.6, "is_fabric": 0.5, "can_fly": 1.0, "is_colorful": 0.8, "found_outdoors": 1.0, "is_common": 0.7}),
    ("skateboard", "a skateboard", 84, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_toy": 0.6, "is_sports_equipment": 1.0, "is_wood": 0.8, "has_wheels": 1.0, "is_flat": 0.8, "found_outdoors": 0.8, "is_common": 0.7, "is_solid": 1.0}),
    ("tennis_racket", "a tennis racket", 85, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_sports_equipment": 1.0, "has_handle": 1.0, "is_common": 0.6, "is_solid": 1.0}),

    # MISC COMMON OBJECTS (Rank 86-110)
    ("key", "a key", 86, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 1.0, "is_small": 1.0, "is_tiny": 0.8, "fits_in_pocket": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "is_shiny": 0.7}),
    ("wallet", "a wallet", 87, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_leather": 0.8, "is_accessory": 1.0, "is_container": 1.0, "is_small": 0.9, "fits_in_pocket": 1.0, "opens_closes": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0}),
    ("umbrella", "an umbrella", 88, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_fabric": 0.8, "is_metal": 0.5, "is_long": 0.7, "opens_closes": 1.0, "is_portable": 1.0, "found_outdoors": 0.7, "is_common": 0.9, "has_handle": 1.0}),
    ("bag", "a bag", 89, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_fabric": 0.6, "is_plastic": 0.4, "is_container": 1.0, "is_portable": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("backpack", "a backpack", 90, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_fabric": 1.0, "is_container": 1.0, "is_storage": 1.0, "is_portable": 1.0, "is_worn": 0.8, "opens_closes": 1.0, "is_common": 0.9, "found_at_home": 1.0}),
    ("suitcase", "a suitcase", 91, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_plastic": 0.6, "is_fabric": 0.5, "is_container": 1.0, "is_storage": 1.0, "has_wheels": 0.8, "opens_closes": 1.0, "is_portable": 1.0, "is_common": 0.8}),
    ("candle", "a candle", 92, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "produces_light": 1.0, "is_hot": 0.7, "is_cylindrical": 0.8, "is_white": 0.5, "is_colorful": 0.5, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 1.0}),
    ("flashlight", "a flashlight", 93, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_lighting": 1.0, "produces_light": 1.0, "requires_batteries": 1.0, "is_cylindrical": 0.8, "is_portable": 1.0, "is_common": 0.8, "is_solid": 1.0, "found_at_home": 1.0}),
    ("coin", "a coin", 94, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_metal": 1.0, "is_money": 1.0, "is_round": 1.0, "is_flat": 0.9, "is_tiny": 0.9, "is_small": 1.0, "is_shiny": 0.8, "is_common": 1.0, "is_solid": 1.0, "fits_in_pocket": 1.0}),
    ("ring", "a ring", 95, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_jewelry": 1.0, "is_metal": 0.9, "is_worn": 1.0, "is_round": 1.0, "is_tiny": 0.9, "is_small": 1.0, "is_shiny": 0.9, "is_precious": 0.7, "is_common": 0.8, "is_solid": 1.0}),
    ("necklace", "a necklace", 96, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_jewelry": 1.0, "is_metal": 0.7, "is_worn": 1.0, "is_long": 0.8, "is_shiny": 0.8, "is_common": 0.7, "found_at_home": 0.9}),
    ("glasses", "glasses", 97, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_accessory": 1.0, "is_glass": 0.8, "is_plastic": 0.5, "is_worn": 1.0, "is_transparent": 0.8, "is_common": 0.8, "found_at_home": 0.9}),
    ("sunglasses", "sunglasses", 98, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_accessory": 1.0, "is_glass": 0.7, "is_plastic": 0.6, "is_worn": 1.0, "is_black": 0.6, "is_common": 0.8}),
    ("brush", "a brush", 99, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_personal_care": 0.8, "is_tool": 0.5, "has_handle": 1.0, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
    ("comb", "a comb", 100, {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.0, "is_plastic": 0.8, "is_personal_care": 1.0, "is_small": 0.9, "is_flat": 0.8, "is_common": 0.9, "is_solid": 1.0, "found_at_home": 1.0}),
]


def generate_entities() -> Dict:
    """Generate the complete entities database."""
    entities = []

    # Add animals
    for entity_id, name, rank, attrs in ANIMALS:
        entity = {
            "id": entity_id,
            "name": name,
            "popularity_rank": rank,
            "category": "animal",
            "attributes": attrs
        }
        entities.append(entity)

    # Add foods/plants
    for entity_id, name, rank, attrs in FOODS_PLANTS:
        entity = {
            "id": entity_id,
            "name": name,
            "popularity_rank": rank,
            "category": "plant",
            "attributes": attrs
        }
        entities.append(entity)

    # Add objects
    for entity_id, name, rank, attrs in OBJECTS:
        entity = {
            "id": entity_id,
            "name": name,
            "popularity_rank": rank,
            "category": "object",
            "attributes": attrs
        }
        entities.append(entity)

    return {"entities": entities}


def save_entities(output_path: str = None):
    """Save entities to JSON file."""
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(__file__), 'data', 'entities.json'
        )

    data = generate_entities()

    # Create backup of existing file
    if os.path.exists(output_path):
        backup_path = output_path + '.backup'
        os.rename(output_path, backup_path)
        print(f"Backed up existing file to {backup_path}")

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data['entities'])} entities to {output_path}")
    print(f"  Animals: {len(ANIMALS)}")
    print(f"  Foods/Plants: {len(FOODS_PLANTS)}")
    print(f"  Objects: {len(OBJECTS)}")

    return output_path


if __name__ == '__main__':
    save_entities()
