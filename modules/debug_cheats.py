"""Debugging cheats

These cheats are meant for debugging,
don't change these if you want to play the game normally.
Changing them might cause the game to be buggy as they're not often tested.
"""

MODULE_GUARD = True  # True

if __name__ == "__main__" and MODULE_GUARD:
    print("Please run the main.py file,\nThis module is meant to be imported.")
    raise SystemExit

# OPTION = Value  # Default value
DOUBLES_LOCK = False  # False
WELCOME_MESSAGE = False  # True
FILE_CHECK = True  # True
LOAD_FILES = True  # True
BANKRUPTCY_CHECK = True  # True
SKIP_DICE = False  # False
SKIP_JAIL = False  # False
SINGLE_PLAYER = False  # False
PLAYER_COUNT_OVERRIDE = 2  # 0
# Numbers <=0 is disabling

# Structure for START_OPTIONS:
# {player.index: Value, }  # {}
START_LOCATION: dict[int, int] = {}
# Square (property) indexes can be found in the squares.txt file
START_BALANCE: dict[int, int] = {}
START_DOUBLES: dict[int, int] = {}
START_JAILED: dict[int, bool] = {}
START_GOOJF: dict[int, int] = {}
START_PROPERTIES: dict[int, dict[str, list[int]]] = {1: {"street": []}}
# {player.index: {"property_type": [property.index, ]}, }
START_COLOR_SETS: dict[int, list[str]] = {}
# {player.index: ["color_set", ], }
# Mismatched color sets with properties may cause unexpected behavior
