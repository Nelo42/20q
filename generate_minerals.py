#!/usr/bin/env python3
"""Add minerals/objects to entity database."""

import json

# Load existing entities
with open("twenty_questions/data/entities.json", "r") as f:
    data = json.load(f)

entities = data["entities"]
existing_ids = {e["id"] for e in entities}

minerals = [
    # Electronics
    ("smartphone", "a smartphone", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "has_buttons": 0.5, "is_portable": 1.0, "fits_in_pocket": 1.0, "used_for_communication": 1.0, "is_common": 1.0, "is_solid": 1.0, "is_hard": 0.8, "requires_batteries": 1.0, "is_rectangular": 0.9}),
    ("laptop", "a laptop", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "has_buttons": 1.0, "is_portable": 0.9, "used_for_communication": 0.8, "holds_information": 1.0, "is_common": 1.0, "is_solid": 1.0, "plugs_in": 0.8, "requires_batteries": 0.9, "opens_closes": 1.0}),
    ("television", "a television", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "is_large": 0.6, "plugs_in": 1.0, "used_for_entertainment": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 1.0, "is_rectangular": 0.9}),
    ("computer", "a computer", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 0.8, "has_buttons": 1.0, "plugs_in": 1.0, "holds_information": 1.0, "is_common": 1.0, "is_solid": 1.0, "found_at_home": 0.8, "found_in_office": 0.9}),
    ("tablet", "a tablet", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_screen": 1.0, "is_portable": 1.0, "is_flat": 1.0, "requires_batteries": 1.0, "is_common": 0.8, "is_solid": 1.0}),
    ("camera", "a camera", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_portable": 1.0, "has_buttons": 1.0, "requires_batteries": 1.0, "is_solid": 1.0}),
    ("headphones", "headphones", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "produces_sound": 1.0, "is_worn": 1.0, "is_portable": 1.0, "used_for_entertainment": 0.9, "is_common": 0.9}),
    ("speaker", "a speaker", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "produces_sound": 1.0, "plugs_in": 0.7, "used_for_entertainment": 0.9, "is_common": 0.8}),
    ("microwave", "a microwave", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "used_for_cooking": 1.0, "plugs_in": 1.0, "is_common": 1.0, "opens_closes": 1.0, "has_buttons": 1.0, "found_at_home": 1.0}),
    ("refrigerator", "a refrigerator", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "is_large": 1.0, "is_cold": 1.0, "plugs_in": 1.0, "is_common": 1.0, "opens_closes": 1.0, "found_at_home": 1.0, "is_container": 1.0}),
    ("washing_machine", "a washing machine", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_large": 0.8, "used_for_cleaning": 1.0, "plugs_in": 1.0, "is_common": 0.9, "found_at_home": 1.0}),
    ("toaster", "a toaster", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "used_for_cooking": 1.0, "is_hot": 0.8, "plugs_in": 1.0, "is_common": 0.9, "found_at_home": 1.0}),
    ("blender", "a blender", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "used_for_cooking": 0.9, "plugs_in": 1.0, "is_container": 0.8, "is_sharp": 0.8}),
    ("lamp", "a lamp", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "produces_light": 1.0, "plugs_in": 0.9, "is_common": 1.0, "found_at_home": 1.0, "is_decorative": 0.5}),
    ("flashlight", "a flashlight", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "produces_light": 1.0, "is_portable": 1.0, "requires_batteries": 1.0, "is_cylindrical": 0.8, "has_handle": 0.5}),
    ("clock", "a clock", {"is_mineral": 1.0, "is_manmade": 1.0, "tells_time": 1.0, "is_round": 0.7, "is_common": 1.0, "found_at_home": 1.0, "found_in_office": 0.8}),
    ("watch", "a watch", {"is_mineral": 1.0, "is_manmade": 1.0, "tells_time": 1.0, "is_worn": 1.0, "is_small": 1.0, "is_jewelry": 0.5, "is_common": 0.9, "is_portable": 1.0}),
    ("radio", "a radio", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "produces_sound": 1.0, "used_for_entertainment": 0.8, "used_for_communication": 0.5, "requires_batteries": 0.6, "plugs_in": 0.6}),
    ("remote_control", "a remote control", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 1.0, "has_buttons": 1.0, "is_small": 0.9, "is_portable": 1.0, "requires_batteries": 1.0, "found_at_home": 1.0, "is_common": 1.0}),
    ("battery", "a battery", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.8, "is_small": 0.9, "is_cylindrical": 0.7, "is_portable": 1.0, "is_common": 1.0}),
    ("light_bulb", "a light bulb", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.8, "produces_light": 1.0, "is_glass": 0.8, "is_round": 0.8, "is_common": 1.0}),

    # Vehicles
    ("car", "a car", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "has_wheels": 1.0, "is_large": 0.8, "used_for_transportation": 1.0, "is_mechanical": 1.0, "is_metal": 0.9, "is_common": 1.0, "found_outdoors": 1.0}),
    ("bicycle", "a bicycle", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "has_wheels": 1.0, "used_for_transportation": 1.0, "is_mechanical": 1.0, "is_metal": 0.9, "is_common": 1.0, "found_outdoors": 1.0, "is_sports_equipment": 0.5}),
    ("motorcycle", "a motorcycle", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "has_wheels": 1.0, "used_for_transportation": 1.0, "is_mechanical": 1.0, "is_metal": 0.9, "is_fast": 0.8, "found_outdoors": 1.0}),
    ("airplane", "an airplane", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "has_wings": 1.0, "can_fly": 1.0, "is_large": 1.0, "used_for_transportation": 1.0, "is_metal": 0.9, "is_fast": 1.0}),
    ("helicopter", "a helicopter", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "can_fly": 1.0, "is_large": 0.8, "used_for_transportation": 1.0, "is_metal": 0.9}),
    ("boat", "a boat", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "can_swim": 1.0, "lives_in_water": 0.9, "used_for_transportation": 1.0, "found_outdoors": 1.0}),
    ("ship", "a ship", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "can_swim": 1.0, "lives_in_water": 0.9, "lives_in_ocean": 0.9, "is_large": 1.0, "used_for_transportation": 1.0, "is_metal": 0.8}),
    ("train", "a train", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "has_wheels": 1.0, "is_large": 1.0, "used_for_transportation": 1.0, "is_metal": 1.0, "is_long": 0.9, "is_fast": 0.8}),
    ("bus", "a bus", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "has_wheels": 1.0, "is_large": 1.0, "used_for_transportation": 1.0, "is_metal": 0.9, "is_common": 0.9}),
    ("truck", "a truck", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 1.0, "has_wheels": 1.0, "is_large": 1.0, "used_for_transportation": 1.0, "is_metal": 0.9, "is_strong": 0.8}),
    ("skateboard", "a skateboard", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 0.7, "has_wheels": 1.0, "is_sports_equipment": 1.0, "is_small": 0.7, "is_flat": 0.9, "is_wood": 0.8}),
    ("scooter", "a scooter", {"is_mineral": 1.0, "is_manmade": 1.0, "is_vehicle": 0.8, "has_wheels": 1.0, "is_portable": 0.8, "used_for_transportation": 0.8, "is_metal": 0.8}),

    # Furniture
    ("chair", "a chair", {"is_mineral": 1.0, "is_manmade": 1.0, "is_furniture": 1.0, "is_wood": 0.6, "has_four_legs": 0.9, "is_common": 1.0, "found_at_home": 1.0, "found_in_office": 1.0}),
    ("table", "a table", {"is_mineral": 1.0, "is_manmade": 1.0, "is_furniture": 1.0, "is_wood": 0.7, "has_four_legs": 0.9, "is_flat": 0.9, "is_common": 1.0, "found_at_home": 1.0, "found_in_office": 1.0}),
    ("bed", "a bed", {"is_mineral": 1.0, "is_manmade": 1.0, "is_furniture": 1.0, "is_large": 0.8, "is_soft": 0.9, "is_common": 1.0, "found_at_home": 1.0, "is_rectangular": 0.9}),
    ("sofa", "a sofa", {"is_mineral": 1.0, "is_manmade": 1.0, "is_furniture": 1.0, "is_large": 0.8, "is_soft": 0.9, "is_common": 1.0, "found_at_home": 1.0, "is_fabric": 0.8}),
    ("desk", "a desk", {"is_mineral": 1.0, "is_manmade": 1.0, "is_furniture": 1.0, "is_wood": 0.7, "is_flat": 0.9, "is_common": 1.0, "found_in_office": 1.0, "found_at_home": 0.8}),
    ("bookshelf", "a bookshelf", {"is_mineral": 1.0, "is_manmade": 1.0, "is_furniture": 1.0, "is_wood": 0.8, "is_large": 0.7, "is_container": 0.8, "found_at_home": 1.0, "found_in_office": 0.7}),
    ("dresser", "a dresser", {"is_mineral": 1.0, "is_manmade": 1.0, "is_furniture": 1.0, "is_wood": 0.8, "is_container": 1.0, "opens_closes": 1.0, "found_at_home": 1.0}),
    ("mirror", "a mirror", {"is_mineral": 1.0, "is_manmade": 1.0, "is_glass": 1.0, "is_shiny": 1.0, "is_flat": 1.0, "is_common": 1.0, "found_at_home": 1.0, "found_in_bathroom": 0.9, "is_decorative": 0.6}),
    ("rug", "a rug", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 1.0, "is_soft": 0.9, "is_flat": 1.0, "is_decorative": 0.7, "found_at_home": 1.0, "is_common": 0.9}),
    ("curtain", "a curtain", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 1.0, "is_soft": 0.8, "is_decorative": 0.7, "found_at_home": 1.0, "is_common": 0.9}),

    # Kitchen items
    ("knife", "a knife", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_kitchen_item": 0.8, "is_metal": 0.9, "is_sharp": 1.0, "used_for_cutting": 1.0, "is_dangerous": 0.6, "is_common": 1.0, "has_handle": 1.0, "is_long": 0.6}),
    ("fork", "a fork", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_metal": 0.9, "is_small": 0.8, "is_common": 1.0, "found_at_home": 1.0, "has_handle": 0.8}),
    ("spoon", "a spoon", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_metal": 0.8, "is_small": 0.8, "is_common": 1.0, "found_at_home": 1.0, "has_handle": 0.8, "is_round": 0.6}),
    ("plate", "a plate", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_ceramic": 0.8, "is_flat": 0.9, "is_round": 0.9, "is_common": 1.0, "is_container": 0.6, "found_at_home": 1.0}),
    ("bowl", "a bowl", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_ceramic": 0.7, "is_round": 0.9, "is_container": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("cup", "a cup", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_ceramic": 0.6, "is_container": 1.0, "has_handle": 0.7, "is_common": 1.0, "found_at_home": 1.0, "is_cylindrical": 0.8}),
    ("glass_cup", "a glass", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_glass": 1.0, "is_transparent": 1.0, "is_container": 1.0, "is_common": 1.0, "found_at_home": 1.0, "is_cylindrical": 0.8}),
    ("bottle", "a bottle", {"is_mineral": 1.0, "is_manmade": 1.0, "is_container": 1.0, "is_glass": 0.5, "is_plastic": 0.4, "is_cylindrical": 0.8, "is_common": 1.0, "has_handle": 0.3}),
    ("pot", "a pot", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_metal": 0.8, "is_container": 1.0, "used_for_cooking": 1.0, "has_handle": 1.0, "is_round": 0.8, "found_at_home": 1.0}),
    ("pan", "a pan", {"is_mineral": 1.0, "is_manmade": 1.0, "is_kitchen_item": 1.0, "is_metal": 0.9, "used_for_cooking": 1.0, "has_handle": 1.0, "is_flat": 0.7, "found_at_home": 1.0}),
    ("oven", "an oven", {"is_mineral": 1.0, "is_manmade": 1.0, "is_appliance": 1.0, "is_kitchen_item": 1.0, "is_metal": 0.9, "used_for_cooking": 1.0, "is_hot": 0.9, "is_large": 0.7, "plugs_in": 0.8, "found_at_home": 1.0, "opens_closes": 1.0}),

    # Tools
    ("hammer", "a hammer", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_metal": 0.8, "has_handle": 1.0, "is_hard": 1.0, "is_heavy": 0.6, "found_outdoors": 0.5}),
    ("screwdriver", "a screwdriver", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_metal": 0.8, "has_handle": 1.0, "is_long": 0.8}),
    ("wrench", "a wrench", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_metal": 1.0, "is_hard": 1.0}),
    ("saw", "a saw", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_metal": 0.8, "is_sharp": 1.0, "used_for_cutting": 1.0, "is_dangerous": 0.6, "has_handle": 1.0}),
    ("drill", "a drill", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_electronic": 0.8, "is_mechanical": 1.0, "is_metal": 0.7, "requires_batteries": 0.6, "is_sharp": 0.7}),
    ("shovel", "a shovel", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_metal": 0.7, "has_handle": 1.0, "is_long": 0.9, "found_outdoors": 0.9, "is_outdoor_item": 1.0}),
    ("rake", "a rake", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "has_handle": 1.0, "is_long": 0.9, "found_outdoors": 1.0, "is_outdoor_item": 1.0}),
    ("axe", "an axe", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_weapon": 0.5, "is_metal": 0.8, "is_sharp": 1.0, "used_for_cutting": 1.0, "is_dangerous": 0.7, "has_handle": 1.0}),
    ("ladder", "a ladder", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_metal": 0.6, "is_wood": 0.4, "is_long": 0.9, "can_climb": 1.0, "found_outdoors": 0.7}),
    ("scissors", "scissors", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 1.0, "is_metal": 0.9, "is_sharp": 1.0, "used_for_cutting": 1.0, "is_office_item": 0.8, "is_small": 0.8, "has_handle": 1.0}),

    # Office items
    ("pen", "a pen", {"is_mineral": 1.0, "is_manmade": 1.0, "is_office_item": 1.0, "used_for_writing": 1.0, "is_small": 1.0, "is_long": 0.8, "is_plastic": 0.7, "fits_in_pocket": 1.0, "is_common": 1.0}),
    ("pencil", "a pencil", {"is_mineral": 1.0, "is_manmade": 1.0, "is_office_item": 1.0, "used_for_writing": 1.0, "is_small": 1.0, "is_long": 0.8, "is_wood": 0.9, "fits_in_pocket": 1.0, "is_common": 1.0, "is_yellow": 0.7}),
    ("eraser", "an eraser", {"is_mineral": 1.0, "is_manmade": 1.0, "is_office_item": 1.0, "is_small": 1.0, "is_rubber": 0.9, "is_soft": 0.8, "is_common": 0.9}),
    ("ruler", "a ruler", {"is_mineral": 1.0, "is_manmade": 1.0, "is_office_item": 1.0, "is_long": 0.9, "is_flat": 1.0, "is_plastic": 0.6, "is_wood": 0.3, "is_common": 0.9}),
    ("stapler", "a stapler", {"is_mineral": 1.0, "is_manmade": 1.0, "is_office_item": 1.0, "is_metal": 0.7, "is_small": 0.8, "is_common": 0.8, "found_in_office": 1.0}),
    ("paper", "paper", {"is_mineral": 1.0, "is_manmade": 1.0, "is_paper": 1.0, "is_office_item": 1.0, "is_flat": 1.0, "is_white": 0.9, "is_soft": 0.6, "is_common": 1.0, "holds_information": 0.8, "is_disposable": 0.7}),
    ("book", "a book", {"is_mineral": 1.0, "is_manmade": 1.0, "is_paper": 0.9, "holds_information": 1.0, "is_rectangular": 0.9, "opens_closes": 1.0, "is_common": 1.0, "found_at_home": 0.9, "found_in_office": 0.7}),
    ("newspaper", "a newspaper", {"is_mineral": 1.0, "is_manmade": 1.0, "is_paper": 1.0, "holds_information": 1.0, "is_flat": 0.9, "is_disposable": 0.9, "is_common": 0.8}),
    ("envelope", "an envelope", {"is_mineral": 1.0, "is_manmade": 1.0, "is_paper": 1.0, "is_office_item": 1.0, "is_flat": 0.9, "is_container": 0.8, "opens_closes": 1.0, "is_common": 0.9, "used_for_communication": 0.8}),
    ("calendar", "a calendar", {"is_mineral": 1.0, "is_manmade": 1.0, "is_paper": 0.8, "is_office_item": 1.0, "tells_time": 0.8, "holds_information": 1.0, "is_common": 0.9, "found_in_office": 0.9, "found_at_home": 0.8}),
    ("calculator", "a calculator", {"is_mineral": 1.0, "is_manmade": 1.0, "is_electronic": 0.8, "is_office_item": 1.0, "has_buttons": 1.0, "has_screen": 0.9, "is_small": 0.9, "is_common": 0.8}),
    ("folder", "a folder", {"is_mineral": 1.0, "is_manmade": 1.0, "is_paper": 0.7, "is_office_item": 1.0, "is_container": 0.8, "is_flat": 0.8, "opens_closes": 1.0, "found_in_office": 1.0}),

    # Clothing
    ("shirt", "a shirt", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_soft": 0.9, "is_common": 1.0, "found_at_home": 1.0}),
    ("pants", "pants", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("dress", "a dress", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_common": 0.8, "found_at_home": 1.0}),
    ("jacket", "a jacket", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 0.8, "is_worn": 1.0, "is_common": 0.9, "found_at_home": 1.0}),
    ("coat", "a coat", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 0.8, "is_worn": 1.0, "is_large": 0.5, "is_common": 0.9}),
    ("hat", "a hat", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_worn": 1.0, "is_fabric": 0.7, "is_common": 0.9, "is_small": 0.7}),
    ("shoes", "shoes", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_worn": 1.0, "is_leather": 0.5, "is_rubber": 0.3, "is_common": 1.0, "found_at_home": 1.0}),
    ("boots", "boots", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_worn": 1.0, "is_leather": 0.6, "is_rubber": 0.3, "found_outdoors": 0.7}),
    ("socks", "socks", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_small": 0.9, "is_soft": 0.9, "is_common": 1.0}),
    ("gloves", "gloves", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_worn": 1.0, "is_fabric": 0.7, "is_leather": 0.3, "is_small": 0.8, "is_common": 0.8}),
    ("scarf", "a scarf", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_long": 0.9, "is_soft": 0.9, "is_common": 0.8}),
    ("belt", "a belt", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_leather": 0.7, "is_worn": 1.0, "is_long": 0.9, "is_common": 0.9}),
    ("tie", "a tie", {"is_mineral": 1.0, "is_manmade": 1.0, "is_clothing": 1.0, "is_fabric": 1.0, "is_worn": 1.0, "is_long": 0.9, "is_decorative": 0.7}),
    ("glasses", "glasses", {"is_mineral": 1.0, "is_manmade": 1.0, "is_worn": 1.0, "is_glass": 0.8, "is_transparent": 0.9, "is_small": 0.8, "is_common": 0.9}),
    ("sunglasses", "sunglasses", {"is_mineral": 1.0, "is_manmade": 1.0, "is_worn": 1.0, "is_glass": 0.7, "is_black": 0.7, "found_outdoors": 0.8}),
    ("umbrella", "an umbrella", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 0.7, "has_handle": 1.0, "is_portable": 1.0, "found_outdoors": 0.8, "is_common": 0.9, "opens_closes": 1.0}),
    ("backpack", "a backpack", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 0.8, "is_container": 1.0, "is_worn": 0.8, "is_portable": 1.0, "is_common": 0.9}),
    ("purse", "a purse", {"is_mineral": 1.0, "is_manmade": 1.0, "is_leather": 0.6, "is_container": 1.0, "is_portable": 1.0, "is_common": 0.8, "opens_closes": 1.0}),
    ("wallet", "a wallet", {"is_mineral": 1.0, "is_manmade": 1.0, "is_leather": 0.7, "is_container": 1.0, "is_small": 1.0, "fits_in_pocket": 1.0, "is_common": 1.0, "opens_closes": 1.0}),

    # Sports equipment
    ("ball", "a ball", {"is_mineral": 1.0, "is_manmade": 1.0, "is_sports_equipment": 1.0, "is_round": 1.0, "is_rubber": 0.5, "is_leather": 0.3, "is_toy": 0.5, "is_common": 1.0}),
    ("basketball", "a basketball", {"is_mineral": 1.0, "is_manmade": 1.0, "is_sports_equipment": 1.0, "is_round": 1.0, "is_orange": 1.0, "is_rubber": 0.8, "is_common": 0.8}),
    ("football", "a football", {"is_mineral": 1.0, "is_manmade": 1.0, "is_sports_equipment": 1.0, "is_leather": 0.8, "is_brown": 0.8, "is_common": 0.8}),
    ("tennis_racket", "a tennis racket", {"is_mineral": 1.0, "is_manmade": 1.0, "is_sports_equipment": 1.0, "has_handle": 1.0, "is_common": 0.7}),
    ("golf_club", "a golf club", {"is_mineral": 1.0, "is_manmade": 1.0, "is_sports_equipment": 1.0, "is_metal": 0.8, "has_handle": 1.0, "is_long": 0.9}),
    ("baseball_bat", "a baseball bat", {"is_mineral": 1.0, "is_manmade": 1.0, "is_sports_equipment": 1.0, "is_wood": 0.7, "is_metal": 0.3, "has_handle": 1.0, "is_long": 0.9, "is_cylindrical": 0.8}),
    ("helmet", "a helmet", {"is_mineral": 1.0, "is_manmade": 1.0, "is_sports_equipment": 0.7, "is_worn": 1.0, "is_hard": 1.0, "is_plastic": 0.6, "is_round": 0.7}),

    # Musical instruments
    ("guitar", "a guitar", {"is_mineral": 1.0, "is_manmade": 1.0, "is_instrument": 1.0, "makes_music": 1.0, "is_wood": 0.9, "produces_sound": 1.0, "has_handle": 0.8}),
    ("piano", "a piano", {"is_mineral": 1.0, "is_manmade": 1.0, "is_instrument": 1.0, "makes_music": 1.0, "is_large": 1.0, "has_buttons": 1.0, "produces_sound": 1.0, "is_wood": 0.8}),
    ("violin", "a violin", {"is_mineral": 1.0, "is_manmade": 1.0, "is_instrument": 1.0, "makes_music": 1.0, "is_wood": 1.0, "produces_sound": 1.0, "is_small": 0.7}),
    ("drum", "a drum", {"is_mineral": 1.0, "is_manmade": 1.0, "is_instrument": 1.0, "makes_music": 1.0, "is_round": 0.9, "produces_sound": 1.0, "is_cylindrical": 0.8}),
    ("flute", "a flute", {"is_mineral": 1.0, "is_manmade": 1.0, "is_instrument": 1.0, "makes_music": 1.0, "is_metal": 0.9, "is_long": 0.9, "is_cylindrical": 0.9, "produces_sound": 1.0}),
    ("trumpet", "a trumpet", {"is_mineral": 1.0, "is_manmade": 1.0, "is_instrument": 1.0, "makes_music": 1.0, "is_metal": 1.0, "is_shiny": 0.9, "produces_sound": 1.0}),

    # Toys
    ("doll", "a doll", {"is_mineral": 1.0, "is_manmade": 1.0, "is_toy": 1.0, "is_plastic": 0.7, "is_small": 0.8, "is_common": 0.8}),
    ("teddy_bear", "a teddy bear", {"is_mineral": 1.0, "is_manmade": 1.0, "is_toy": 1.0, "is_soft": 1.0, "is_fabric": 0.9, "has_fur": 0.8, "is_brown": 0.7, "is_common": 0.8}),
    ("lego", "Lego", {"is_mineral": 1.0, "is_manmade": 1.0, "is_toy": 1.0, "is_plastic": 1.0, "is_small": 1.0, "is_colorful": 0.9, "is_hard": 1.0, "is_common": 0.8}),
    ("puzzle", "a puzzle", {"is_mineral": 1.0, "is_manmade": 1.0, "is_toy": 1.0, "is_paper": 0.7, "used_for_entertainment": 1.0, "is_common": 0.8}),
    ("kite", "a kite", {"is_mineral": 1.0, "is_manmade": 1.0, "is_toy": 1.0, "can_fly": 1.0, "is_fabric": 0.6, "is_colorful": 0.8, "found_outdoors": 1.0, "is_flat": 0.7}),
    ("yo_yo", "a yo-yo", {"is_mineral": 1.0, "is_manmade": 1.0, "is_toy": 1.0, "is_round": 1.0, "is_small": 1.0, "is_plastic": 0.8}),

    # Bathroom items
    ("toothbrush", "a toothbrush", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_plastic": 0.9, "is_small": 1.0, "used_for_cleaning": 1.0, "has_handle": 1.0, "is_common": 1.0}),
    ("toothpaste", "toothpaste", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_soft": 0.8, "used_for_cleaning": 1.0, "is_common": 1.0, "is_consumed": 0.8}),
    ("soap", "soap", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "used_for_cleaning": 1.0, "is_solid": 0.7, "is_common": 1.0, "is_consumed": 0.8}),
    ("shampoo", "shampoo", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_liquid": 1.0, "used_for_cleaning": 1.0, "is_common": 1.0, "is_consumed": 0.8}),
    ("towel", "a towel", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_fabric": 1.0, "is_soft": 0.9, "used_for_cleaning": 0.8, "is_common": 1.0, "is_rectangular": 0.8}),
    ("toilet", "a toilet", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_ceramic": 1.0, "is_white": 0.9, "is_common": 1.0, "found_in_bathroom": 1.0, "found_at_home": 1.0}),
    ("bathtub", "a bathtub", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_ceramic": 0.8, "is_large": 0.8, "is_container": 1.0, "found_in_bathroom": 1.0, "found_at_home": 1.0}),
    ("sink", "a sink", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 0.5, "is_kitchen_item": 0.5, "is_ceramic": 0.7, "is_metal": 0.3, "is_container": 0.8, "is_common": 1.0, "found_at_home": 1.0}),
    ("comb", "a comb", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_plastic": 0.8, "is_small": 1.0, "is_flat": 0.8, "is_common": 1.0}),
    ("hairdryer", "a hairdryer", {"is_mineral": 1.0, "is_manmade": 1.0, "is_bathroom_item": 1.0, "is_electronic": 1.0, "is_hot": 0.9, "plugs_in": 1.0, "has_handle": 1.0, "produces_sound": 0.8}),

    # Natural minerals
    ("diamond", "a diamond", {"is_mineral": 1.0, "is_natural": 1.0, "is_precious": 1.0, "is_hard": 1.0, "is_shiny": 1.0, "is_transparent": 0.9, "is_rare": 0.9, "is_small": 0.9, "is_jewelry": 0.8}),
    ("gold", "gold", {"is_mineral": 1.0, "is_natural": 1.0, "is_metal": 1.0, "is_precious": 1.0, "is_shiny": 1.0, "is_yellow": 1.0, "is_jewelry": 0.7, "is_rare": 0.7}),
    ("silver", "silver", {"is_mineral": 1.0, "is_natural": 1.0, "is_metal": 1.0, "is_precious": 0.8, "is_shiny": 1.0, "is_white": 0.8, "is_jewelry": 0.7}),
    ("iron", "iron", {"is_mineral": 1.0, "is_natural": 1.0, "is_metal": 1.0, "is_hard": 1.0, "is_strong": 0.9, "is_common": 0.8}),
    ("copper", "copper", {"is_mineral": 1.0, "is_natural": 1.0, "is_metal": 1.0, "is_shiny": 0.8, "is_orange": 0.7, "is_brown": 0.5}),
    ("rock", "a rock", {"is_mineral": 1.0, "is_natural": 1.0, "is_stone": 1.0, "is_hard": 1.0, "is_solid": 1.0, "found_outdoors": 1.0, "is_common": 1.0}),
    ("sand", "sand", {"is_mineral": 1.0, "is_natural": 1.0, "is_stone": 0.7, "is_tiny": 1.0, "is_brown": 0.6, "is_yellow": 0.4, "found_outdoors": 1.0, "is_common": 1.0}),
    ("coal", "coal", {"is_mineral": 1.0, "is_natural": 1.0, "is_stone": 0.7, "is_black": 1.0, "is_hard": 0.8, "is_hot": 0.5}),
    ("ice", "ice", {"is_mineral": 1.0, "is_natural": 1.0, "is_cold": 1.0, "is_solid": 1.0, "is_transparent": 0.8, "is_hard": 0.8, "is_white": 0.7}),
    ("water", "water", {"is_mineral": 1.0, "is_natural": 1.0, "is_liquid": 1.0, "is_transparent": 1.0, "is_cold": 0.5, "is_common": 1.0, "is_consumed": 1.0}),
    ("salt", "salt", {"is_mineral": 1.0, "is_natural": 1.0, "is_food": 0.8, "is_white": 1.0, "is_tiny": 1.0, "is_savory": 1.0, "is_common": 1.0, "is_consumed": 1.0}),

    # Misc objects
    ("key", "a key", {"is_mineral": 1.0, "is_manmade": 1.0, "is_metal": 1.0, "is_small": 1.0, "fits_in_pocket": 1.0, "is_common": 1.0}),
    ("lock", "a lock", {"is_mineral": 1.0, "is_manmade": 1.0, "is_metal": 0.9, "is_small": 0.8, "is_hard": 1.0, "is_common": 0.9}),
    ("door", "a door", {"is_mineral": 1.0, "is_manmade": 1.0, "is_wood": 0.7, "is_large": 0.8, "is_flat": 0.8, "opens_closes": 1.0, "is_common": 1.0, "found_at_home": 1.0}),
    ("window", "a window", {"is_mineral": 1.0, "is_manmade": 1.0, "is_glass": 1.0, "is_transparent": 1.0, "is_flat": 1.0, "opens_closes": 0.8, "is_common": 1.0, "found_at_home": 1.0}),
    ("fence", "a fence", {"is_mineral": 1.0, "is_manmade": 1.0, "is_wood": 0.6, "is_metal": 0.4, "is_large": 0.7, "found_outdoors": 1.0}),
    ("rope", "a rope", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 0.8, "is_long": 1.0, "is_flexible": 1.0, "is_strong": 0.7}),
    ("chain", "a chain", {"is_mineral": 1.0, "is_manmade": 1.0, "is_metal": 1.0, "is_long": 0.8, "is_flexible": 0.8, "is_strong": 0.9, "is_shiny": 0.7}),
    ("candle", "a candle", {"is_mineral": 1.0, "is_manmade": 1.0, "produces_light": 1.0, "is_hot": 0.8, "is_cylindrical": 0.9, "is_decorative": 0.6, "is_consumed": 1.0}),
    ("match", "a match", {"is_mineral": 1.0, "is_manmade": 1.0, "is_wood": 0.9, "is_small": 1.0, "produces_light": 0.8, "is_hot": 0.8, "is_disposable": 1.0, "is_dangerous": 0.5}),
    ("coin", "a coin", {"is_mineral": 1.0, "is_manmade": 1.0, "is_metal": 1.0, "is_small": 1.0, "is_round": 1.0, "is_flat": 0.9, "is_shiny": 0.8, "is_common": 1.0, "fits_in_pocket": 1.0}),
    ("flag", "a flag", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 1.0, "is_colorful": 0.9, "is_flat": 0.9, "found_outdoors": 0.8, "is_decorative": 0.7}),
    ("map", "a map", {"is_mineral": 1.0, "is_manmade": 1.0, "is_paper": 0.9, "is_flat": 1.0, "holds_information": 1.0, "is_colorful": 0.7}),
    ("pillow", "a pillow", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 1.0, "is_soft": 1.0, "found_at_home": 1.0, "is_common": 1.0, "is_rectangular": 0.7}),
    ("blanket", "a blanket", {"is_mineral": 1.0, "is_manmade": 1.0, "is_fabric": 1.0, "is_soft": 1.0, "is_large": 0.7, "found_at_home": 1.0, "is_common": 1.0, "is_flat": 0.8}),
    ("picture_frame", "a picture frame", {"is_mineral": 1.0, "is_manmade": 1.0, "is_wood": 0.6, "is_decorative": 1.0, "is_flat": 0.8, "found_at_home": 1.0, "is_rectangular": 0.9}),
    ("vase", "a vase", {"is_mineral": 1.0, "is_manmade": 1.0, "is_ceramic": 0.7, "is_glass": 0.3, "is_container": 1.0, "is_decorative": 1.0, "found_at_home": 1.0}),
    ("box", "a box", {"is_mineral": 1.0, "is_manmade": 1.0, "is_container": 1.0, "is_paper": 0.5, "is_wood": 0.3, "opens_closes": 1.0, "is_common": 1.0, "is_rectangular": 0.9}),
    ("bag", "a bag", {"is_mineral": 1.0, "is_manmade": 1.0, "is_container": 1.0, "is_fabric": 0.5, "is_plastic": 0.4, "is_portable": 1.0, "is_common": 1.0, "is_flexible": 0.8}),
    ("basket", "a basket", {"is_mineral": 1.0, "is_manmade": 1.0, "is_container": 1.0, "has_handle": 0.8, "is_common": 0.8}),
    ("trash_can", "a trash can", {"is_mineral": 1.0, "is_manmade": 1.0, "is_container": 1.0, "is_plastic": 0.6, "is_metal": 0.4, "is_common": 1.0, "found_at_home": 1.0, "is_cylindrical": 0.7}),
    ("broom", "a broom", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 0.8, "has_handle": 1.0, "is_long": 0.9, "used_for_cleaning": 1.0, "found_at_home": 1.0, "is_common": 0.9}),
    ("mop", "a mop", {"is_mineral": 1.0, "is_manmade": 1.0, "is_tool": 0.8, "has_handle": 1.0, "is_long": 0.9, "used_for_cleaning": 1.0, "found_at_home": 1.0}),
    ("sponge", "a sponge", {"is_mineral": 1.0, "is_manmade": 0.8, "is_soft": 1.0, "used_for_cleaning": 1.0, "is_small": 0.9, "is_kitchen_item": 0.7, "is_yellow": 0.6}),
]

count = 0
for id, name, attrs in minerals:
    if id not in existing_ids:
        entities.append({"id": id, "name": name, "attributes": attrs})
        count += 1

print(f"Added {count} mineral/object entities")
print(f"Total entities: {len(entities)}")

with open("twenty_questions/data/entities.json", "w") as f:
    json.dump({"entities": entities}, f, indent=2)
