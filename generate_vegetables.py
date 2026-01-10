#!/usr/bin/env python3
"""Add vegetables/plants to entity database."""

import json

# Load existing entities
with open("twenty_questions/data/entities.json", "r") as f:
    data = json.load(f)

entities = data["entities"]
existing_ids = {e["id"] for e in entities}

vegetables = [
    # Fruits
    ("apple", "an apple", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.9, "has_seeds": 1.0, "has_skin": 1.0, "is_sweet": 0.8, "is_red": 0.6, "is_green": 0.3, "is_natural": 1.0, "is_solid": 1.0, "is_common": 1.0}),
    ("orange", "an orange", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 1.0, "has_seeds": 0.9, "has_skin": 1.0, "is_sweet": 0.8, "is_sour": 0.4, "is_orange": 1.0, "is_tropical": 0.6, "is_natural": 1.0, "is_solid": 1.0}),
    ("banana", "a banana", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 0.9, "is_long": 0.8, "has_skin": 1.0, "is_sweet": 0.9, "is_yellow": 1.0, "is_tropical": 1.0, "is_natural": 1.0, "is_solid": 1.0, "is_common": 1.0}),
    ("grape", "a grape", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_round": 1.0, "is_small": 1.0, "has_seeds": 0.7, "has_skin": 1.0, "is_sweet": 0.9, "is_purple": 0.6, "is_green": 0.4, "is_natural": 1.0}),
    ("strawberry", "a strawberry", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_small": 1.0, "has_seeds": 1.0, "is_sweet": 0.9, "is_red": 1.0, "is_natural": 1.0, "is_solid": 1.0}),
    ("blueberry", "a blueberry", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_small": 1.0, "is_tiny": 0.9, "is_round": 1.0, "is_sweet": 0.8, "is_blue": 1.0, "is_natural": 1.0}),
    ("raspberry", "a raspberry", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_small": 1.0, "is_sweet": 0.8, "is_red": 1.0, "is_natural": 1.0}),
    ("blackberry", "a blackberry", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "is_small": 1.0, "is_sweet": 0.7, "is_black": 1.0, "grows_on_vines": 0.8, "is_natural": 1.0}),
    ("cherry", "a cherry", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 1.0, "is_round": 1.0, "has_pit": 1.0, "is_sweet": 0.8, "is_red": 1.0, "is_natural": 1.0}),
    ("peach", "a peach", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.8, "has_pit": 1.0, "has_skin": 1.0, "is_sweet": 0.9, "is_orange": 0.8, "is_natural": 1.0}),
    ("plum", "a plum", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.9, "has_pit": 1.0, "has_skin": 1.0, "is_sweet": 0.8, "is_purple": 0.8, "is_natural": 1.0}),
    ("apricot", "an apricot", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.8, "has_pit": 1.0, "is_sweet": 0.8, "is_orange": 0.9, "is_natural": 1.0, "is_small": 0.8}),
    ("pear", "a pear", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "has_seeds": 1.0, "has_skin": 1.0, "is_sweet": 0.8, "is_green": 0.7, "is_natural": 1.0}),
    ("mango", "a mango", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "has_pit": 1.0, "has_skin": 1.0, "is_sweet": 1.0, "is_orange": 0.7, "is_yellow": 0.5, "is_tropical": 1.0, "is_natural": 1.0}),
    ("pineapple", "a pineapple", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "has_skin": 1.0, "is_sweet": 0.9, "is_sour": 0.4, "is_yellow": 0.9, "is_tropical": 1.0, "is_natural": 1.0}),
    ("coconut", "a coconut", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_nut": 0.5, "is_food": 1.0, "grows_on_trees": 1.0, "has_shell": 1.0, "is_round": 0.9, "is_brown": 0.9, "is_tropical": 1.0, "is_natural": 1.0, "is_hard": 1.0}),
    ("papaya", "a papaya", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "has_seeds": 1.0, "is_sweet": 0.9, "is_orange": 0.8, "is_tropical": 1.0, "is_natural": 1.0}),
    ("kiwi", "a kiwi fruit", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_small": 0.9, "has_skin": 1.0, "has_seeds": 1.0, "is_sweet": 0.7, "is_sour": 0.4, "is_green": 0.9, "is_brown": 0.5, "is_natural": 1.0}),
    ("watermelon", "a watermelon", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_large": 0.8, "is_round": 0.8, "has_seeds": 0.9, "has_skin": 1.0, "is_sweet": 0.9, "is_red": 0.8, "is_green": 0.5, "is_natural": 1.0}),
    ("cantaloupe", "a cantaloupe", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_round": 0.9, "has_seeds": 1.0, "has_skin": 1.0, "is_sweet": 0.9, "is_orange": 0.9, "is_natural": 1.0}),
    ("honeydew", "a honeydew melon", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_round": 0.9, "has_seeds": 1.0, "is_sweet": 0.9, "is_green": 0.9, "is_natural": 1.0}),
    ("lemon", "a lemon", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "has_seeds": 0.8, "has_skin": 1.0, "is_sour": 1.0, "is_yellow": 1.0, "is_natural": 1.0}),
    ("lime", "a lime", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "has_seeds": 0.8, "has_skin": 1.0, "is_sour": 1.0, "is_green": 1.0, "is_natural": 1.0, "is_small": 0.8}),
    ("grapefruit", "a grapefruit", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 1.0, "has_seeds": 0.8, "has_skin": 1.0, "is_sour": 0.7, "is_bitter": 0.5, "is_yellow": 0.6, "is_pink": 0.4, "is_natural": 1.0}),
    ("pomegranate", "a pomegranate", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_round": 0.9, "has_seeds": 1.0, "has_skin": 1.0, "is_sweet": 0.7, "is_red": 1.0, "is_natural": 1.0}),
    ("fig", "a fig", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.9, "has_seeds": 1.0, "is_sweet": 0.9, "is_purple": 0.7, "is_natural": 1.0}),
    ("date", "a date", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.9, "has_pit": 1.0, "is_sweet": 1.0, "is_brown": 1.0, "lives_in_desert": 0.8, "is_natural": 1.0}),
    ("avocado", "an avocado", {"is_vegetable": 1.0, "is_fruit": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "has_pit": 1.0, "has_skin": 1.0, "is_green": 1.0, "is_savory": 0.6, "is_natural": 1.0}),
    ("tomato", "a tomato", {"is_vegetable": 1.0, "is_fruit": 0.8, "is_vegetable_food": 0.8, "is_food": 1.0, "grows_on_vines": 1.0, "is_round": 0.9, "has_seeds": 1.0, "has_skin": 1.0, "is_red": 0.9, "is_natural": 1.0, "is_common": 1.0}),

    # Vegetables
    ("carrot", "a carrot", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_long": 0.8, "is_orange": 1.0, "is_sweet": 0.4, "is_natural": 1.0, "is_hard": 0.7, "is_common": 1.0}),
    ("potato", "a potato", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_round": 0.7, "is_brown": 0.8, "is_savory": 0.6, "is_natural": 1.0, "is_common": 1.0}),
    ("sweet_potato", "a sweet potato", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_sweet": 0.7, "is_orange": 0.9, "is_natural": 1.0}),
    ("onion", "an onion", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_round": 0.9, "has_skin": 1.0, "is_savory": 0.8, "is_white": 0.5, "is_natural": 1.0, "is_common": 1.0}),
    ("garlic", "garlic", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_herb": 0.5, "is_food": 1.0, "grows_underground": 1.0, "is_small": 0.9, "is_white": 0.9, "is_savory": 0.9, "is_natural": 1.0, "is_common": 1.0}),
    ("celery", "celery", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 0.9, "is_green": 1.0, "is_savory": 0.5, "has_leaves": 0.8, "is_natural": 1.0}),
    ("broccoli", "broccoli", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_green": 1.0, "has_leaves": 0.7, "is_natural": 1.0, "is_common": 1.0}),
    ("cauliflower", "cauliflower", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_white": 1.0, "has_leaves": 0.7, "is_natural": 1.0}),
    ("cabbage", "a cabbage", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_round": 0.8, "is_green": 0.8, "has_leaves": 1.0, "is_natural": 1.0}),
    ("lettuce", "lettuce", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_green": 1.0, "has_leaves": 1.0, "is_natural": 1.0, "is_common": 1.0}),
    ("spinach", "spinach", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_green": 1.0, "has_leaves": 1.0, "is_natural": 1.0}),
    ("kale", "kale", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_green": 1.0, "has_leaves": 1.0, "is_natural": 1.0}),
    ("cucumber", "a cucumber", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_long": 0.8, "is_cylindrical": 0.9, "is_green": 1.0, "has_seeds": 1.0, "is_natural": 1.0, "is_common": 1.0}),
    ("zucchini", "a zucchini", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_long": 0.8, "is_green": 1.0, "is_natural": 1.0}),
    ("squash", "a squash", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "has_seeds": 1.0, "is_yellow": 0.6, "is_orange": 0.4, "is_natural": 1.0}),
    ("pumpkin", "a pumpkin", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_on_vines": 1.0, "is_large": 0.7, "is_round": 0.9, "has_seeds": 1.0, "is_orange": 1.0, "is_natural": 1.0}),
    ("eggplant", "an eggplant", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_on_vines": 0.8, "is_purple": 1.0, "has_skin": 1.0, "is_natural": 1.0}),
    ("pepper", "a bell pepper", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "has_seeds": 1.0, "is_colorful": 0.9, "is_red": 0.4, "is_green": 0.3, "is_yellow": 0.3, "is_natural": 1.0}),
    ("chili", "a chili pepper", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_herb": 0.5, "is_food": 1.0, "is_small": 0.8, "is_spicy": 1.0, "is_red": 0.7, "is_green": 0.3, "is_natural": 1.0}),
    ("corn", "corn", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_grain": 0.5, "is_food": 1.0, "has_seeds": 1.0, "is_yellow": 1.0, "is_sweet": 0.6, "is_natural": 1.0, "is_common": 1.0}),
    ("peas", "peas", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_small": 1.0, "is_round": 1.0, "is_green": 1.0, "is_sweet": 0.5, "is_natural": 1.0}),
    ("green_beans", "green beans", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 0.9, "is_green": 1.0, "has_seeds": 0.8, "is_natural": 1.0}),
    ("asparagus", "asparagus", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("artichoke", "an artichoke", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_green": 0.9, "has_leaves": 1.0, "is_natural": 1.0}),
    ("beet", "a beet", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_round": 0.8, "is_red": 0.9, "is_purple": 0.5, "is_natural": 1.0}),
    ("radish", "a radish", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_small": 0.9, "is_round": 0.8, "is_red": 0.8, "is_spicy": 0.5, "is_natural": 1.0}),
    ("turnip", "a turnip", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_round": 0.8, "is_white": 0.7, "is_natural": 1.0}),
    ("parsnip", "a parsnip", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_long": 0.8, "is_white": 0.9, "is_natural": 1.0}),
    ("leek", "a leek", {"is_vegetable": 1.0, "is_vegetable_food": 1.0, "is_food": 1.0, "is_long": 0.9, "is_green": 0.7, "is_white": 0.5, "is_natural": 1.0}),
    ("mushroom", "a mushroom", {"is_vegetable": 1.0, "is_fungus": 1.0, "is_food": 1.0, "grows_underground": 0.3, "is_small": 0.8, "is_brown": 0.6, "is_white": 0.4, "is_natural": 1.0, "is_common": 1.0}),

    # Nuts & Seeds
    ("peanut", "a peanut", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_small": 1.0, "has_shell": 0.9, "is_brown": 0.9, "is_natural": 1.0, "is_common": 1.0}),
    ("walnut", "a walnut", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.9, "has_shell": 1.0, "is_brown": 1.0, "is_round": 0.7, "is_natural": 1.0, "is_hard": 1.0}),
    ("almond", "an almond", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 1.0, "has_shell": 0.8, "is_brown": 0.9, "is_natural": 1.0}),
    ("cashew", "a cashew", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 1.0, "is_tropical": 1.0, "is_natural": 1.0}),
    ("pistachio", "a pistachio", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 1.0, "has_shell": 1.0, "is_green": 0.8, "is_natural": 1.0}),
    ("hazelnut", "a hazelnut", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 1.0, "has_shell": 1.0, "is_round": 0.8, "is_brown": 1.0, "is_natural": 1.0}),
    ("pecan", "a pecan", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.9, "has_shell": 1.0, "is_brown": 1.0, "is_natural": 1.0}),
    ("chestnut", "a chestnut", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "grows_on_trees": 1.0, "is_small": 0.8, "has_shell": 1.0, "is_brown": 1.0, "is_round": 0.8, "is_natural": 1.0}),
    ("sunflower_seed", "a sunflower seed", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "is_tiny": 1.0, "has_shell": 0.8, "is_natural": 1.0}),
    ("sesame_seed", "a sesame seed", {"is_vegetable": 1.0, "is_nut": 1.0, "is_food": 1.0, "is_tiny": 1.0, "is_white": 0.6, "is_natural": 1.0}),

    # Grains
    ("wheat", "wheat", {"is_vegetable": 1.0, "is_grain": 1.0, "is_food": 1.0, "is_grass": 1.0, "is_brown": 0.7, "is_natural": 1.0, "is_common": 1.0}),
    ("rice", "rice", {"is_vegetable": 1.0, "is_grain": 1.0, "is_food": 1.0, "is_tiny": 1.0, "is_white": 0.8, "grows_in_water": 0.7, "is_natural": 1.0, "is_common": 1.0}),
    ("oats", "oats", {"is_vegetable": 1.0, "is_grain": 1.0, "is_food": 1.0, "is_grass": 1.0, "is_brown": 0.7, "is_natural": 1.0}),
    ("barley", "barley", {"is_vegetable": 1.0, "is_grain": 1.0, "is_food": 1.0, "is_grass": 1.0, "is_natural": 1.0}),

    # Herbs & Spices
    ("basil", "basil", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("mint", "mint", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("parsley", "parsley", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("cilantro", "cilantro", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("rosemary", "rosemary", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("thyme", "thyme", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_small": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("oregano", "oregano", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("sage", "sage", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "has_leaves": 1.0, "is_green": 0.8, "is_natural": 1.0}),
    ("ginger", "ginger", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "grows_underground": 1.0, "is_spicy": 0.7, "is_brown": 0.8, "is_natural": 1.0}),
    ("cinnamon", "cinnamon", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "is_brown": 1.0, "is_sweet": 0.5, "is_spicy": 0.4, "is_natural": 1.0}),
    ("vanilla", "vanilla", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "is_sweet": 0.8, "is_brown": 0.7, "is_tropical": 1.0, "is_natural": 1.0}),
    ("pepper_spice", "black pepper", {"is_vegetable": 1.0, "is_herb": 1.0, "is_food": 1.0, "is_tiny": 1.0, "is_spicy": 0.8, "is_black": 1.0, "is_natural": 1.0, "is_common": 1.0}),

    # Trees & Plants
    ("oak_tree", "an oak tree", {"is_vegetable": 1.0, "is_tree": 1.0, "is_large": 1.0, "has_leaves": 1.0, "is_brown": 0.5, "is_green": 0.5, "is_natural": 1.0, "is_wood": 1.0}),
    ("pine_tree", "a pine tree", {"is_vegetable": 1.0, "is_tree": 1.0, "is_large": 1.0, "has_leaves": 1.0, "is_green": 1.0, "lives_in_arctic": 0.4, "is_natural": 1.0}),
    ("palm_tree", "a palm tree", {"is_vegetable": 1.0, "is_tree": 1.0, "is_large": 1.0, "has_leaves": 1.0, "is_tropical": 1.0, "is_green": 0.8, "is_natural": 1.0}),
    ("maple_tree", "a maple tree", {"is_vegetable": 1.0, "is_tree": 1.0, "is_large": 1.0, "has_leaves": 1.0, "is_colorful": 0.7, "is_natural": 1.0}),
    ("bamboo", "bamboo", {"is_vegetable": 1.0, "is_grass": 1.0, "is_large": 0.7, "is_long": 0.9, "is_green": 1.0, "lives_in_asia": 0.8, "is_natural": 1.0}),
    ("cactus", "a cactus", {"is_vegetable": 1.0, "lives_in_desert": 1.0, "is_green": 1.0, "is_dangerous": 0.4, "is_natural": 1.0}),
    ("seaweed", "seaweed", {"is_vegetable": 1.0, "is_aquatic_plant": 1.0, "lives_in_water": 1.0, "lives_in_ocean": 1.0, "is_green": 0.8, "is_food": 0.6, "is_natural": 1.0}),
    ("moss", "moss", {"is_vegetable": 1.0, "is_small": 1.0, "is_green": 1.0, "lives_in_water": 0.3, "is_natural": 1.0}),
    ("fern", "a fern", {"is_vegetable": 1.0, "has_leaves": 1.0, "is_green": 1.0, "is_natural": 1.0}),
    ("ivy", "ivy", {"is_vegetable": 1.0, "grows_on_vines": 1.0, "has_leaves": 1.0, "is_green": 1.0, "can_climb": 1.0, "is_natural": 1.0}),

    # Flowers
    ("rose", "a rose", {"is_vegetable": 1.0, "is_flower": 1.0, "is_red": 0.6, "is_colorful": 0.9, "is_dangerous": 0.3, "is_natural": 1.0, "is_decorative": 1.0}),
    ("sunflower", "a sunflower", {"is_vegetable": 1.0, "is_flower": 1.0, "is_large": 0.6, "is_yellow": 1.0, "is_round": 0.8, "is_natural": 1.0}),
    ("tulip", "a tulip", {"is_vegetable": 1.0, "is_flower": 1.0, "is_colorful": 1.0, "is_natural": 1.0, "is_decorative": 1.0}),
    ("daisy", "a daisy", {"is_vegetable": 1.0, "is_flower": 1.0, "is_small": 0.8, "is_white": 0.8, "is_yellow": 0.5, "is_natural": 1.0}),
    ("lily", "a lily", {"is_vegetable": 1.0, "is_flower": 1.0, "is_white": 0.6, "is_colorful": 0.7, "is_natural": 1.0, "is_decorative": 1.0}),
    ("orchid", "an orchid", {"is_vegetable": 1.0, "is_flower": 1.0, "is_colorful": 1.0, "is_tropical": 0.7, "is_rare": 0.5, "is_natural": 1.0, "is_decorative": 1.0}),
    ("dandelion", "a dandelion", {"is_vegetable": 1.0, "is_flower": 1.0, "is_small": 0.9, "is_yellow": 0.8, "is_white": 0.5, "is_natural": 1.0, "is_common": 1.0}),
    ("lavender", "lavender", {"is_vegetable": 1.0, "is_flower": 1.0, "is_herb": 0.5, "is_purple": 1.0, "is_natural": 1.0}),
    ("lotus", "a lotus", {"is_vegetable": 1.0, "is_flower": 1.0, "is_aquatic_plant": 1.0, "grows_in_water": 1.0, "is_colorful": 0.8, "is_natural": 1.0}),
]

count = 0
for id, name, attrs in vegetables:
    if id not in existing_ids:
        entities.append({"id": id, "name": name, "attributes": attrs})
        count += 1

print(f"Added {count} vegetable/plant entities")
print(f"Total entities: {len(entities)}")

with open("twenty_questions/data/entities.json", "w") as f:
    json.dump({"entities": entities}, f, indent=2)
