#!/usr/bin/env python3
"""Generate expanded entity database for 20 Questions game."""

import json

entities = []

# ============== ANIMALS (150+) ==============
animals = [
    # Mammals - Pets & Domestic
    ("dog", "a dog", {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 0.95, "has_four_legs": 1.0, "has_tail": 0.95, "is_domesticated": 0.95, "is_pet": 0.9, "makes_noise": 0.9, "is_intelligent": 0.7}),
    ("cat", "a cat", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 0.95, "has_four_legs": 1.0, "has_tail": 0.95, "is_domesticated": 0.9, "is_pet": 0.9, "is_predator": 0.7, "is_nocturnal": 0.6, "has_claws": 1.0}),
    ("hamster", "a hamster", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 1.0, "is_tiny": 0.9, "is_pet": 0.9, "is_nocturnal": 0.8}),
    ("guinea_pig", "a guinea pig", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 0.9, "is_pet": 0.9, "is_herbivore": 1.0, "makes_noise": 0.7}),
    ("rabbit", "a rabbit", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_small": 0.8, "is_herbivore": 1.0, "is_pet": 0.6, "can_jump": 1.0}),
    ("ferret", "a ferret", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "is_small": 0.8, "is_pet": 0.7, "is_carnivore": 0.9, "is_long": 0.8}),
    ("gerbil", "a gerbil", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_tiny": 1.0, "is_pet": 0.8, "has_tail": 1.0}),

    # Mammals - Farm
    ("horse", "a horse", {"is_animal": 1.0, "is_mammal": 1.0, "is_equine": 1.0, "has_fur": 0.9, "has_four_legs": 1.0, "has_tail": 1.0, "is_large": 0.9, "is_domesticated": 0.9, "is_farm_animal": 0.8, "has_hooves": 1.0, "is_fast": 0.9, "is_strong": 0.8, "is_herbivore": 1.0}),
    ("cow", "a cow", {"is_animal": 1.0, "is_mammal": 1.0, "is_bovine": 1.0, "has_four_legs": 1.0, "is_large": 0.8, "is_domesticated": 1.0, "is_farm_animal": 1.0, "is_herbivore": 1.0, "has_hooves": 1.0, "has_horns": 0.6, "is_food": 0.8}),
    ("pig", "a pig", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_domesticated": 0.9, "is_farm_animal": 1.0, "is_omnivore": 1.0, "is_intelligent": 0.7, "is_food": 0.7}),
    ("sheep", "a sheep", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_domesticated": 1.0, "is_farm_animal": 1.0, "is_herbivore": 1.0, "has_hooves": 1.0, "lives_in_groups": 0.9}),
    ("goat", "a goat", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_domesticated": 0.9, "is_farm_animal": 0.9, "is_herbivore": 1.0, "has_hooves": 1.0, "has_horns": 0.8, "can_climb": 0.8}),
    ("donkey", "a donkey", {"is_animal": 1.0, "is_mammal": 1.0, "is_equine": 1.0, "has_four_legs": 1.0, "is_domesticated": 0.9, "is_farm_animal": 0.8, "has_hooves": 1.0, "is_herbivore": 1.0, "makes_noise": 0.8}),
    ("llama", "a llama", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 0.7, "is_domesticated": 0.8, "is_herbivore": 1.0, "has_long_neck": 0.7, "lives_in_americas": 0.9}),
    ("alpaca", "an alpaca", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_domesticated": 0.9, "is_herbivore": 1.0, "lives_in_americas": 0.9}),

    # Mammals - Big Cats
    ("lion", "a lion", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 0.9, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 0.9, "lives_in_africa": 0.9, "lives_in_groups": 0.8, "makes_noise": 1.0, "has_claws": 1.0}),
    ("tiger", "a tiger", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 0.9, "is_carnivore": 1.0, "is_predator": 1.0, "has_stripes": 1.0, "is_dangerous": 0.9, "lives_in_asia": 0.9, "is_solitary": 0.8, "is_endangered": 0.8, "has_claws": 1.0}),
    ("leopard", "a leopard", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "has_spots": 1.0, "can_climb": 1.0, "is_solitary": 0.9, "has_claws": 1.0}),
    ("cheetah", "a cheetah", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "has_spots": 1.0, "is_fast": 1.0, "lives_in_africa": 0.9, "is_endangered": 0.7, "has_claws": 1.0}),
    ("jaguar", "a jaguar", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "has_spots": 1.0, "can_swim": 0.8, "lives_in_americas": 0.9, "lives_in_jungle": 0.9, "has_claws": 1.0}),
    ("cougar", "a cougar", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "lives_in_americas": 1.0, "is_solitary": 0.9, "has_claws": 1.0}),
    ("lynx", "a lynx", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_solitary": 0.9, "lives_in_arctic": 0.5, "has_claws": 1.0}),
    ("snow_leopard", "a snow leopard", {"is_animal": 1.0, "is_mammal": 1.0, "is_feline": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "has_spots": 1.0, "lives_in_mountains": 1.0, "lives_in_asia": 1.0, "is_endangered": 0.9, "has_claws": 1.0}),

    # Mammals - Canines
    ("wolf", "a wolf", {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "lives_in_groups": 1.0, "makes_noise": 0.9, "is_wild": 1.0, "has_claws": 0.8}),
    ("fox", "a fox", {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 0.8, "is_predator": 0.7, "is_solitary": 0.7, "is_nocturnal": 0.6, "is_wild": 1.0}),
    ("coyote", "a coyote", {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 0.8, "is_predator": 0.8, "lives_in_americas": 1.0, "makes_noise": 0.9, "is_wild": 1.0}),
    ("hyena", "a hyena", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 1.0, "is_predator": 0.9, "lives_in_africa": 0.9, "lives_in_groups": 0.9, "makes_noise": 0.9, "is_nocturnal": 0.6}),
    ("dingo", "a dingo", {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 0.9, "is_predator": 0.8, "lives_in_australia": 1.0, "is_wild": 1.0}),
    ("jackal", "a jackal", {"is_animal": 1.0, "is_mammal": 1.0, "is_canine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_carnivore": 0.8, "lives_in_africa": 0.8, "is_wild": 1.0}),

    # Mammals - Bears
    ("bear", "a bear", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 0.9, "is_omnivore": 0.8, "is_strong": 1.0, "is_dangerous": 0.9, "has_claws": 1.0, "hibernates": 0.8}),
    ("polar_bear", "a polar bear", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "lives_in_arctic": 1.0, "is_white": 1.0, "can_swim": 0.9, "is_dangerous": 0.9, "has_claws": 1.0}),
    ("grizzly_bear", "a grizzly bear", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "is_omnivore": 1.0, "is_strong": 1.0, "is_dangerous": 0.9, "lives_in_americas": 0.9, "hibernates": 0.9, "has_claws": 1.0}),
    ("panda", "a panda", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 0.8, "is_herbivore": 0.95, "is_endangered": 0.9, "lives_in_asia": 1.0, "is_black": 0.5, "is_white": 0.5}),
    ("koala", "a koala", {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_pouch": 1.0, "lives_in_australia": 1.0, "lives_in_trees": 1.0, "is_herbivore": 1.0, "is_small": 0.7}),

    # Mammals - Primates
    ("monkey", "a monkey", {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "has_tail": 0.9, "lives_in_trees": 0.9, "is_intelligent": 0.8, "lives_in_groups": 0.9, "is_omnivore": 0.8}),
    ("gorilla", "a gorilla", {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "is_large": 0.9, "is_strong": 1.0, "lives_in_jungle": 0.9, "lives_in_africa": 1.0, "is_endangered": 0.8, "is_intelligent": 0.9, "is_herbivore": 0.9}),
    ("chimpanzee", "a chimpanzee", {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "lives_in_africa": 1.0, "is_intelligent": 0.95, "lives_in_groups": 0.9, "is_omnivore": 0.9}),
    ("orangutan", "an orangutan", {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "is_large": 0.8, "lives_in_trees": 1.0, "lives_in_asia": 1.0, "is_intelligent": 0.9, "is_endangered": 0.9, "is_orange": 0.9}),
    ("baboon", "a baboon", {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "lives_in_africa": 1.0, "lives_in_groups": 1.0, "is_omnivore": 0.9, "is_aggressive": 0.7}),
    ("lemur", "a lemur", {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "has_tail": 1.0, "lives_in_trees": 0.9, "is_endangered": 0.7}),
    ("gibbon", "a gibbon", {"is_animal": 1.0, "is_mammal": 1.0, "is_primate": 1.0, "has_fur": 1.0, "lives_in_trees": 1.0, "lives_in_asia": 1.0, "makes_noise": 0.9, "can_climb": 1.0}),

    # Mammals - Large herbivores
    ("elephant", "an elephant", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "is_huge": 1.0, "has_trunk": 1.0, "has_tusks": 0.8, "is_herbivore": 1.0, "is_strong": 1.0, "is_intelligent": 0.9, "lives_in_africa": 0.7, "lives_in_asia": 0.3, "lives_in_groups": 0.9}),
    ("giraffe", "a giraffe", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "has_long_neck": 1.0, "has_spots": 1.0, "is_herbivore": 1.0, "lives_in_africa": 1.0, "has_hooves": 1.0}),
    ("zebra", "a zebra", {"is_animal": 1.0, "is_mammal": 1.0, "is_equine": 1.0, "has_four_legs": 1.0, "has_stripes": 1.0, "is_herbivore": 1.0, "lives_in_africa": 1.0, "has_hooves": 1.0, "lives_in_groups": 0.9}),
    ("hippo", "a hippopotamus", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "lives_in_water": 0.8, "is_herbivore": 1.0, "is_dangerous": 0.9, "lives_in_africa": 1.0, "is_aggressive": 0.8}),
    ("rhino", "a rhinoceros", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "has_horns": 1.0, "is_herbivore": 1.0, "is_dangerous": 0.8, "is_endangered": 0.9, "is_strong": 0.9}),
    ("buffalo", "a buffalo", {"is_animal": 1.0, "is_mammal": 1.0, "is_bovine": 1.0, "has_four_legs": 1.0, "is_large": 0.9, "has_horns": 1.0, "is_herbivore": 1.0, "is_dangerous": 0.7, "lives_in_groups": 0.9, "has_hooves": 1.0}),
    ("bison", "a bison", {"is_animal": 1.0, "is_mammal": 1.0, "is_bovine": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "has_horns": 1.0, "is_herbivore": 1.0, "lives_in_americas": 0.9, "has_hooves": 1.0}),
    ("moose", "a moose", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 1.0, "has_horns": 0.8, "is_herbivore": 1.0, "lives_in_arctic": 0.5, "has_hooves": 1.0, "is_solitary": 0.7}),
    ("deer", "a deer", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_horns": 0.6, "is_herbivore": 1.0, "is_fast": 0.9, "has_hooves": 1.0}),
    ("elk", "an elk", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "is_large": 0.8, "has_horns": 0.8, "is_herbivore": 1.0, "has_hooves": 1.0, "lives_in_americas": 0.8}),
    ("reindeer", "a reindeer", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_horns": 0.9, "is_herbivore": 1.0, "lives_in_arctic": 1.0, "has_hooves": 1.0, "is_domesticated": 0.5}),
    ("antelope", "an antelope", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_horns": 0.9, "is_herbivore": 1.0, "is_fast": 0.9, "lives_in_africa": 0.8, "has_hooves": 1.0}),
    ("gazelle", "a gazelle", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "has_horns": 0.8, "is_herbivore": 1.0, "is_fast": 1.0, "lives_in_africa": 0.9, "has_hooves": 1.0}),
    ("camel", "a camel", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "is_large": 0.9, "is_domesticated": 0.8, "lives_in_desert": 1.0, "is_herbivore": 1.0, "has_hooves": 1.0}),

    # Mammals - Marine
    ("whale", "a whale", {"is_animal": 1.0, "is_mammal": 1.0, "is_cetacean": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_large": 1.0, "is_huge": 1.0, "can_swim": 1.0, "has_no_legs": 1.0, "has_fins": 1.0}),
    ("dolphin", "a dolphin", {"is_animal": 1.0, "is_mammal": 1.0, "is_cetacean": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 0.9, "can_swim": 1.0, "is_intelligent": 0.95, "lives_in_groups": 0.9, "has_no_legs": 1.0, "has_fins": 1.0, "makes_noise": 0.9}),
    ("orca", "an orca", {"is_animal": 1.0, "is_mammal": 1.0, "is_cetacean": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_large": 0.9, "is_predator": 1.0, "is_carnivore": 1.0, "is_intelligent": 0.9, "is_black": 0.5, "is_white": 0.5, "has_fins": 1.0}),
    ("seal", "a seal", {"is_animal": 1.0, "is_mammal": 1.0, "lives_in_water": 0.9, "lives_in_ocean": 0.9, "can_swim": 1.0, "is_carnivore": 1.0, "eats_fish": 1.0, "has_fins": 0.8}),
    ("sea_lion", "a sea lion", {"is_animal": 1.0, "is_mammal": 1.0, "lives_in_water": 0.8, "lives_in_ocean": 0.9, "can_swim": 1.0, "is_carnivore": 1.0, "eats_fish": 1.0, "makes_noise": 0.8}),
    ("walrus", "a walrus", {"is_animal": 1.0, "is_mammal": 1.0, "lives_in_water": 0.7, "lives_in_ocean": 0.9, "is_large": 0.9, "has_tusks": 1.0, "lives_in_arctic": 1.0, "can_swim": 1.0}),
    ("manatee", "a manatee", {"is_animal": 1.0, "is_mammal": 1.0, "lives_in_water": 1.0, "is_large": 0.8, "is_herbivore": 1.0, "can_swim": 1.0, "has_fins": 0.8}),
    ("otter", "an otter", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "lives_in_water": 0.8, "can_swim": 1.0, "is_carnivore": 0.9, "eats_fish": 0.9, "is_small": 0.6}),

    # Mammals - Small/Medium
    ("mouse", "a mouse", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 1.0, "is_tiny": 1.0, "has_tail": 1.0, "is_nocturnal": 0.7}),
    ("rat", "a rat", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 0.9, "has_tail": 1.0, "is_nocturnal": 0.7, "is_intelligent": 0.6}),
    ("squirrel", "a squirrel", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 0.9, "has_tail": 1.0, "lives_in_trees": 0.9, "is_herbivore": 0.8, "can_climb": 1.0}),
    ("chipmunk", "a chipmunk", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "is_small": 1.0, "has_stripes": 1.0, "lives_in_americas": 0.9, "can_climb": 0.8}),
    ("beaver", "a beaver", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "has_fur": 1.0, "has_tail": 1.0, "lives_in_water": 0.7, "lives_in_freshwater": 0.9, "can_swim": 1.0, "is_herbivore": 1.0}),
    ("porcupine", "a porcupine", {"is_animal": 1.0, "is_mammal": 1.0, "is_rodent": 1.0, "is_small": 0.7, "is_dangerous": 0.5, "is_nocturnal": 0.7, "is_herbivore": 1.0}),
    ("hedgehog", "a hedgehog", {"is_animal": 1.0, "is_mammal": 1.0, "is_small": 1.0, "is_nocturnal": 0.8, "eats_insects": 0.8, "is_pet": 0.4}),
    ("mole", "a mole", {"is_animal": 1.0, "is_mammal": 1.0, "is_small": 1.0, "lives_underground": 1.0, "can_burrow": 1.0, "eats_insects": 0.9}),
    ("badger", "a badger", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "lives_underground": 0.8, "can_burrow": 1.0, "is_omnivore": 0.9, "is_nocturnal": 0.7, "has_stripes": 0.7}),
    ("skunk", "a skunk", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "is_small": 0.8, "has_stripes": 1.0, "is_nocturnal": 0.8, "is_omnivore": 0.9, "lives_in_americas": 1.0}),
    ("raccoon", "a raccoon", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "is_small": 0.7, "is_nocturnal": 1.0, "is_omnivore": 1.0, "is_intelligent": 0.7, "lives_in_americas": 1.0, "can_climb": 0.8}),
    ("opossum", "an opossum", {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_pouch": 1.0, "is_nocturnal": 1.0, "is_omnivore": 1.0, "lives_in_americas": 1.0, "has_tail": 1.0}),
    ("weasel", "a weasel", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "is_small": 1.0, "is_carnivore": 1.0, "is_predator": 0.9, "is_long": 0.8}),
    ("mongoose", "a mongoose", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "is_small": 0.8, "is_carnivore": 0.9, "is_predator": 0.8, "is_fast": 0.8}),

    # Mammals - Marsupials
    ("kangaroo", "a kangaroo", {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_pouch": 1.0, "has_two_legs": 0.8, "has_tail": 1.0, "is_large": 0.7, "lives_in_australia": 1.0, "is_herbivore": 1.0, "can_jump": 1.0}),
    ("wallaby", "a wallaby", {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_pouch": 1.0, "has_tail": 1.0, "lives_in_australia": 1.0, "is_herbivore": 1.0, "can_jump": 1.0, "is_small": 0.6}),
    ("wombat", "a wombat", {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_pouch": 1.0, "lives_in_australia": 1.0, "lives_underground": 0.8, "can_burrow": 1.0, "is_herbivore": 1.0, "is_nocturnal": 0.7}),
    ("tasmanian_devil", "a Tasmanian devil", {"is_animal": 1.0, "is_mammal": 1.0, "is_marsupial": 1.0, "has_fur": 1.0, "has_pouch": 1.0, "lives_in_australia": 1.0, "is_carnivore": 1.0, "is_aggressive": 0.8, "makes_noise": 0.9, "is_endangered": 0.8}),

    # Mammals - Other
    ("bat", "a bat", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 0.9, "is_nocturnal": 1.0, "eats_insects": 0.7, "lives_in_groups": 0.8}),
    ("sloth", "a sloth", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "lives_in_trees": 1.0, "lives_in_jungle": 1.0, "lives_in_americas": 1.0, "is_herbivore": 0.9, "is_solitary": 0.8, "has_claws": 1.0}),
    ("armadillo", "an armadillo", {"is_animal": 1.0, "is_mammal": 1.0, "has_shell": 0.9, "has_four_legs": 1.0, "lives_underground": 0.6, "can_burrow": 0.9, "eats_insects": 0.8, "lives_in_americas": 1.0}),
    ("anteater", "an anteater", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "eats_insects": 1.0, "has_long_neck": 0.3, "lives_in_americas": 1.0, "has_claws": 1.0}),
    ("platypus", "a platypus", {"is_animal": 1.0, "is_mammal": 1.0, "has_fur": 1.0, "has_four_legs": 1.0, "lives_in_australia": 1.0, "lives_in_water": 0.7, "can_swim": 1.0, "lays_eggs": 1.0, "is_venomous": 0.8, "has_beak": 0.9}),
    ("aardvark", "an aardvark", {"is_animal": 1.0, "is_mammal": 1.0, "has_four_legs": 1.0, "eats_insects": 1.0, "lives_in_africa": 1.0, "is_nocturnal": 1.0, "can_burrow": 1.0}),

    # Birds
    ("eagle", "an eagle", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "has_two_legs": 1.0, "is_predator": 1.0, "is_carnivore": 1.0, "has_claws": 1.0, "lays_eggs": 1.0}),
    ("hawk", "a hawk", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_predator": 1.0, "is_carnivore": 1.0, "has_claws": 1.0, "lays_eggs": 1.0}),
    ("falcon", "a falcon", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_predator": 1.0, "is_carnivore": 1.0, "is_fast": 1.0, "has_claws": 1.0, "lays_eggs": 1.0}),
    ("owl", "an owl", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_predator": 1.0, "is_carnivore": 1.0, "is_nocturnal": 1.0, "has_claws": 1.0, "lays_eggs": 1.0, "makes_noise": 0.8}),
    ("vulture", "a vulture", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_carnivore": 1.0, "is_large": 0.6, "lays_eggs": 1.0}),
    ("penguin", "a penguin", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.0, "has_beak": 1.0, "can_swim": 1.0, "lives_in_arctic": 0.7, "lives_in_groups": 0.9, "lays_eggs": 1.0, "is_black": 0.5, "is_white": 0.5}),
    ("ostrich", "an ostrich", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.0, "has_beak": 1.0, "has_two_legs": 1.0, "is_large": 1.0, "is_fast": 1.0, "lives_in_africa": 0.9, "lays_eggs": 1.0, "has_long_neck": 0.8}),
    ("emu", "an emu", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.0, "has_beak": 1.0, "is_large": 0.9, "lives_in_australia": 1.0, "lays_eggs": 1.0}),
    ("parrot", "a parrot", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_pet": 0.7, "is_colorful": 1.0, "makes_noise": 1.0, "is_intelligent": 0.8, "lives_in_jungle": 0.6, "lays_eggs": 1.0}),
    ("cockatoo", "a cockatoo", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_pet": 0.6, "is_white": 0.7, "makes_noise": 1.0, "lives_in_australia": 0.8, "lays_eggs": 1.0}),
    ("toucan", "a toucan", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_colorful": 1.0, "lives_in_jungle": 1.0, "lives_in_americas": 1.0, "lays_eggs": 1.0}),
    ("peacock", "a peacock", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.4, "has_beak": 1.0, "has_tail": 1.0, "is_colorful": 1.0, "makes_noise": 0.8, "lays_eggs": 1.0}),
    ("flamingo", "a flamingo", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.9, "has_beak": 1.0, "has_long_neck": 0.8, "lives_in_water": 0.6, "lives_in_groups": 0.9, "is_pink": 0.9, "lays_eggs": 1.0}),
    ("swan", "a swan", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.9, "has_beak": 1.0, "can_swim": 1.0, "has_long_neck": 0.9, "is_white": 0.8, "lays_eggs": 1.0}),
    ("duck", "a duck", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.8, "has_beak": 1.0, "can_swim": 1.0, "is_farm_animal": 0.6, "makes_noise": 0.8, "lays_eggs": 1.0}),
    ("goose", "a goose", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.9, "has_beak": 1.0, "can_swim": 0.9, "is_farm_animal": 0.5, "is_aggressive": 0.6, "makes_noise": 0.9, "lays_eggs": 1.0}),
    ("chicken", "a chicken", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.2, "has_beak": 1.0, "is_domesticated": 1.0, "is_farm_animal": 1.0, "makes_noise": 0.8, "lays_eggs": 1.0, "is_food": 0.9}),
    ("turkey", "a turkey", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 0.3, "has_beak": 1.0, "is_farm_animal": 0.8, "is_food": 0.8, "makes_noise": 0.8, "lays_eggs": 1.0}),
    ("crow", "a crow", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_intelligent": 0.9, "is_black": 1.0, "makes_noise": 0.9, "lays_eggs": 1.0}),
    ("raven", "a raven", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_intelligent": 0.9, "is_black": 1.0, "is_large": 0.4, "makes_noise": 0.9, "lays_eggs": 1.0}),
    ("pigeon", "a pigeon", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "lives_in_groups": 0.8, "makes_noise": 0.7, "lays_eggs": 1.0}),
    ("sparrow", "a sparrow", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_small": 1.0, "is_tiny": 0.8, "makes_noise": 0.8, "lays_eggs": 1.0}),
    ("robin", "a robin", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_small": 1.0, "is_red": 0.5, "makes_noise": 0.9, "lays_eggs": 1.0}),
    ("hummingbird", "a hummingbird", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_small": 1.0, "is_tiny": 1.0, "is_colorful": 0.8, "is_fast": 0.9, "lays_eggs": 1.0}),
    ("woodpecker", "a woodpecker", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "lives_in_trees": 0.9, "makes_noise": 1.0, "lays_eggs": 1.0}),
    ("pelican", "a pelican", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "can_swim": 0.8, "eats_fish": 1.0, "is_large": 0.6, "lives_in_ocean": 0.7, "lays_eggs": 1.0}),
    ("seagull", "a seagull", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "lives_in_ocean": 0.8, "is_white": 0.8, "makes_noise": 0.9, "lays_eggs": 1.0}),
    ("stork", "a stork", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "has_long_neck": 0.7, "is_large": 0.6, "migrates": 0.9, "lays_eggs": 1.0}),
    ("heron", "a heron", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "has_long_neck": 0.8, "lives_in_water": 0.6, "eats_fish": 0.9, "lays_eggs": 1.0}),
    ("kingfisher", "a kingfisher", {"is_animal": 1.0, "is_bird": 1.0, "has_feathers": 1.0, "has_wings": 1.0, "can_fly": 1.0, "has_beak": 1.0, "is_colorful": 1.0, "eats_fish": 1.0, "is_small": 0.8, "lays_eggs": 1.0}),

    # Reptiles
    ("snake", "a snake", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_no_legs": 1.0, "is_carnivore": 1.0, "is_predator": 0.9, "lays_eggs": 0.8, "is_venomous": 0.4, "is_long": 1.0}),
    ("python", "a python", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_no_legs": 1.0, "is_carnivore": 1.0, "is_predator": 1.0, "is_large": 0.8, "is_strong": 0.9, "is_long": 1.0, "lays_eggs": 1.0}),
    ("cobra", "a cobra", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_no_legs": 1.0, "is_carnivore": 1.0, "is_venomous": 1.0, "is_dangerous": 0.9, "lives_in_asia": 0.7, "lays_eggs": 1.0}),
    ("rattlesnake", "a rattlesnake", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_no_legs": 1.0, "is_carnivore": 1.0, "is_venomous": 1.0, "is_dangerous": 0.9, "lives_in_americas": 1.0, "makes_noise": 0.9, "lays_eggs": 1.0}),
    ("crocodile", "a crocodile", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_large": 0.9, "lives_in_water": 0.8, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 1.0, "lays_eggs": 1.0}),
    ("alligator", "an alligator", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_large": 0.9, "lives_in_water": 0.8, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 1.0, "lives_in_americas": 0.9, "lays_eggs": 1.0}),
    ("turtle", "a turtle", {"is_animal": 1.0, "is_reptile": 1.0, "has_shell": 1.0, "has_four_legs": 1.0, "lives_in_water": 0.7, "can_swim": 0.8, "lays_eggs": 1.0, "is_herbivore": 0.6}),
    ("tortoise", "a tortoise", {"is_animal": 1.0, "is_reptile": 1.0, "has_shell": 1.0, "has_four_legs": 1.0, "is_herbivore": 1.0, "lays_eggs": 1.0}),
    ("lizard", "a lizard", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_small": 0.7, "lays_eggs": 1.0}),
    ("iguana", "an iguana", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_herbivore": 0.9, "lives_in_americas": 0.9, "is_pet": 0.4, "lays_eggs": 1.0}),
    ("gecko", "a gecko", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "is_small": 1.0, "is_nocturnal": 0.7, "can_climb": 1.0, "eats_insects": 0.9, "lays_eggs": 1.0}),
    ("chameleon", "a chameleon", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_small": 0.8, "is_colorful": 0.9, "lives_in_trees": 0.8, "eats_insects": 1.0, "lays_eggs": 1.0}),
    ("komodo_dragon", "a Komodo dragon", {"is_animal": 1.0, "is_reptile": 1.0, "has_scales": 1.0, "has_four_legs": 1.0, "is_large": 0.9, "is_carnivore": 1.0, "is_predator": 1.0, "is_dangerous": 0.9, "is_venomous": 0.8, "lives_in_asia": 1.0, "lays_eggs": 1.0}),

    # Amphibians
    ("frog", "a frog", {"is_animal": 1.0, "is_amphibian": 1.0, "has_four_legs": 1.0, "is_small": 0.9, "lives_in_water": 0.6, "can_swim": 0.9, "can_jump": 1.0, "lays_eggs": 1.0, "eats_insects": 1.0, "makes_noise": 0.8}),
    ("toad", "a toad", {"is_animal": 1.0, "is_amphibian": 1.0, "has_four_legs": 1.0, "is_small": 0.9, "can_jump": 0.8, "lays_eggs": 1.0, "eats_insects": 1.0, "is_venomous": 0.3}),
    ("salamander", "a salamander", {"is_animal": 1.0, "is_amphibian": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_small": 0.9, "lives_in_water": 0.5, "lays_eggs": 1.0}),
    ("newt", "a newt", {"is_animal": 1.0, "is_amphibian": 1.0, "has_four_legs": 1.0, "has_tail": 1.0, "is_small": 1.0, "lives_in_water": 0.6, "lays_eggs": 1.0}),

    # Fish
    ("shark", "a shark", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 0.7, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "is_predator": 1.0, "is_carnivore": 1.0, "is_dangerous": 0.8, "is_large": 0.7, "has_no_legs": 1.0}),
    ("goldfish", "a goldfish", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_freshwater": 1.0, "can_swim": 1.0, "is_small": 1.0, "is_pet": 0.9, "is_orange": 0.9, "has_no_legs": 1.0}),
    ("salmon", "a salmon", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "can_swim": 1.0, "is_food": 0.9, "migrates": 0.9, "has_no_legs": 1.0}),
    ("tuna", "a tuna", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "is_food": 0.9, "is_large": 0.6, "has_no_legs": 1.0}),
    ("cod", "a cod", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "is_food": 0.9, "has_no_legs": 1.0}),
    ("trout", "a trout", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_freshwater": 1.0, "can_swim": 1.0, "is_food": 0.8, "has_no_legs": 1.0}),
    ("bass", "a bass", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "can_swim": 1.0, "is_food": 0.7, "has_no_legs": 1.0}),
    ("catfish", "a catfish", {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_freshwater": 1.0, "can_swim": 1.0, "is_food": 0.7, "has_no_legs": 1.0}),
    ("swordfish", "a swordfish", {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "is_large": 0.8, "is_fast": 0.9, "has_no_legs": 1.0}),
    ("manta_ray", "a manta ray", {"is_animal": 1.0, "is_fish": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "is_large": 0.9, "is_flat": 0.9, "has_no_legs": 1.0}),
    ("eel", "an eel", {"is_animal": 1.0, "is_fish": 1.0, "lives_in_water": 1.0, "can_swim": 1.0, "is_long": 1.0, "has_no_legs": 1.0}),
    ("piranha", "a piranha", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_freshwater": 1.0, "can_swim": 1.0, "is_predator": 1.0, "is_carnivore": 1.0, "is_dangerous": 0.8, "lives_in_americas": 1.0, "has_no_legs": 1.0}),
    ("clownfish", "a clownfish", {"is_animal": 1.0, "is_fish": 1.0, "has_scales": 1.0, "has_fins": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "is_small": 1.0, "is_colorful": 1.0, "is_orange": 0.8, "has_no_legs": 1.0}),
    ("seahorse", "a seahorse", {"is_animal": 1.0, "is_fish": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 0.7, "is_small": 1.0, "has_no_legs": 1.0}),
    ("pufferfish", "a pufferfish", {"is_animal": 1.0, "is_fish": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "is_venomous": 0.9, "is_round": 0.7, "has_no_legs": 1.0}),

    # Insects
    ("butterfly", "a butterfly", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 1.0, "is_colorful": 1.0, "has_many_legs": 1.0}),
    ("moth", "a moth", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 1.0, "is_nocturnal": 1.0, "has_many_legs": 1.0}),
    ("bee", "a bee", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 1.0, "is_tiny": 1.0, "is_venomous": 0.8, "makes_noise": 0.8, "lives_in_groups": 1.0, "is_yellow": 0.7, "has_many_legs": 1.0}),
    ("wasp", "a wasp", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 1.0, "is_venomous": 0.9, "is_dangerous": 0.5, "is_yellow": 0.7, "has_many_legs": 1.0}),
    ("hornet", "a hornet", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 0.8, "is_venomous": 1.0, "is_dangerous": 0.7, "is_aggressive": 0.8, "has_many_legs": 1.0}),
    ("ant", "an ant", {"is_animal": 1.0, "is_insect": 1.0, "is_small": 1.0, "is_tiny": 1.0, "lives_underground": 0.8, "lives_in_groups": 1.0, "is_strong": 0.7, "has_many_legs": 1.0}),
    ("termite", "a termite", {"is_animal": 1.0, "is_insect": 1.0, "is_tiny": 1.0, "lives_underground": 0.7, "lives_in_groups": 1.0, "has_many_legs": 1.0}),
    ("beetle", "a beetle", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 0.8, "is_small": 1.0, "has_shell": 0.8, "has_many_legs": 1.0}),
    ("ladybug", "a ladybug", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 1.0, "is_tiny": 1.0, "is_red": 0.9, "has_spots": 1.0, "has_many_legs": 1.0}),
    ("dragonfly", "a dragonfly", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 0.9, "is_predator": 0.9, "is_colorful": 0.7, "lives_in_water": 0.3, "has_many_legs": 1.0}),
    ("grasshopper", "a grasshopper", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 0.8, "is_small": 1.0, "can_jump": 1.0, "is_green": 0.8, "makes_noise": 0.8, "has_many_legs": 1.0}),
    ("cricket", "a cricket", {"is_animal": 1.0, "is_insect": 1.0, "is_small": 1.0, "can_jump": 1.0, "makes_noise": 1.0, "is_nocturnal": 0.8, "has_many_legs": 1.0}),
    ("cockroach", "a cockroach", {"is_animal": 1.0, "is_insect": 1.0, "is_small": 1.0, "is_nocturnal": 1.0, "is_fast": 0.8, "has_many_legs": 1.0}),
    ("fly", "a fly", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 1.0, "is_tiny": 1.0, "has_many_legs": 1.0}),
    ("mosquito", "a mosquito", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_tiny": 1.0, "is_dangerous": 0.6, "makes_noise": 0.7, "has_many_legs": 1.0}),
    ("firefly", "a firefly", {"is_animal": 1.0, "is_insect": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_small": 1.0, "is_nocturnal": 1.0, "produces_light": 1.0, "has_many_legs": 1.0}),
    ("caterpillar", "a caterpillar", {"is_animal": 1.0, "is_insect": 1.0, "is_small": 1.0, "is_long": 0.7, "is_herbivore": 1.0, "is_colorful": 0.6, "has_many_legs": 1.0}),
    ("praying_mantis", "a praying mantis", {"is_animal": 1.0, "is_insect": 1.0, "is_small": 0.8, "is_predator": 1.0, "is_carnivore": 1.0, "is_green": 0.8, "has_many_legs": 1.0}),

    # Arachnids
    ("spider", "a spider", {"is_animal": 1.0, "is_arachnid": 1.0, "is_small": 0.9, "is_predator": 1.0, "is_carnivore": 1.0, "is_venomous": 0.5, "eats_insects": 1.0, "has_many_legs": 1.0}),
    ("tarantula", "a tarantula", {"is_animal": 1.0, "is_arachnid": 1.0, "is_small": 0.6, "is_predator": 1.0, "is_venomous": 0.6, "has_fur": 0.8, "is_pet": 0.3, "has_many_legs": 1.0}),
    ("scorpion", "a scorpion", {"is_animal": 1.0, "is_arachnid": 1.0, "is_small": 0.8, "has_tail": 1.0, "is_predator": 1.0, "is_venomous": 1.0, "is_dangerous": 0.7, "lives_in_desert": 0.7, "is_nocturnal": 0.8, "has_many_legs": 1.0}),
    ("tick", "a tick", {"is_animal": 1.0, "is_arachnid": 1.0, "is_tiny": 1.0, "is_dangerous": 0.6, "has_many_legs": 1.0}),

    # Crustaceans
    ("crab", "a crab", {"is_animal": 1.0, "is_crustacean": 1.0, "has_shell": 1.0, "lives_in_water": 0.8, "lives_in_ocean": 0.7, "can_swim": 0.6, "is_small": 0.7, "is_food": 0.7, "has_claws": 1.0, "has_many_legs": 1.0}),
    ("lobster", "a lobster", {"is_animal": 1.0, "is_crustacean": 1.0, "has_shell": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_food": 0.9, "has_claws": 1.0, "is_red": 0.7, "has_many_legs": 1.0}),
    ("shrimp", "a shrimp", {"is_animal": 1.0, "is_crustacean": 1.0, "has_shell": 0.8, "lives_in_water": 1.0, "lives_in_ocean": 0.8, "is_small": 1.0, "is_food": 0.9, "has_many_legs": 1.0}),
    ("crayfish", "a crayfish", {"is_animal": 1.0, "is_crustacean": 1.0, "has_shell": 1.0, "lives_in_water": 1.0, "lives_in_freshwater": 1.0, "is_small": 0.9, "has_claws": 1.0, "is_food": 0.6, "has_many_legs": 1.0}),

    # Mollusks
    ("octopus", "an octopus", {"is_animal": 1.0, "is_mollusk": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "has_tentacles": 1.0, "is_intelligent": 0.9, "is_predator": 0.8, "has_no_legs": 0.2}),
    ("squid", "a squid", {"is_animal": 1.0, "is_mollusk": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 1.0, "has_tentacles": 1.0, "is_predator": 0.8, "is_food": 0.7}),
    ("snail", "a snail", {"is_animal": 1.0, "is_mollusk": 1.0, "has_shell": 1.0, "is_small": 1.0, "is_herbivore": 0.8, "has_no_legs": 1.0}),
    ("slug", "a slug", {"is_animal": 1.0, "is_mollusk": 1.0, "is_small": 1.0, "is_herbivore": 0.8, "has_no_legs": 1.0}),
    ("clam", "a clam", {"is_animal": 1.0, "is_mollusk": 1.0, "has_shell": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 0.8, "is_food": 0.7}),
    ("oyster", "an oyster", {"is_animal": 1.0, "is_mollusk": 1.0, "has_shell": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_food": 0.8}),
    ("mussel", "a mussel", {"is_animal": 1.0, "is_mollusk": 1.0, "has_shell": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 0.8, "is_food": 0.7}),
    ("scallop", "a scallop", {"is_animal": 1.0, "is_mollusk": 1.0, "has_shell": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_food": 0.8, "can_swim": 0.6}),

    # Other sea creatures
    ("jellyfish", "a jellyfish", {"is_animal": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "can_swim": 0.7, "has_tentacles": 1.0, "is_venomous": 0.7, "is_transparent": 0.8, "has_no_legs": 1.0}),
    ("starfish", "a starfish", {"is_animal": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_colorful": 0.6, "has_many_legs": 1.0}),
    ("sea_urchin", "a sea urchin", {"is_animal": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "has_shell": 0.7, "is_round": 0.9, "is_venomous": 0.5}),
    ("coral", "coral", {"is_animal": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_colorful": 0.8}),
]

for id, name, attrs in animals:
    entities.append({"id": id, "name": name, "attributes": attrs})

# Save entities
print(f"Generated {len(entities)} animal entities")

with open("twenty_questions/data/entities.json", "w") as f:
    json.dump({"entities": entities}, f, indent=2)

print(f"Saved {len(entities)} entities to entities.json")
