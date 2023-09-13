"""Game configuration

Don't change these constants if you want to play normally.
However, you can change them to modify how the game works.
Changing these might cause the game to be buggy as they're not often tested.
If you do find a bug, please submit an issue on this project's Github page.
"""

MODULE_GUARD = True  # True

if __name__ == "__main__" and MODULE_GUARD:
    print(
        "Please run the TextopolyAgain.py file,\n"
        "This module is meant to be imported."
    )
    exit()

# OPTION = Value  # Default value
LOCATION_LOCK = False  # False
DOUBLES_LOCK = False  # False

# Structure for START_OPTIONS:
# {player.index: Value, }  # {}
START_LOCATION: dict[int, int] = {}
START_BALANCE: dict[int, int] = {}
START_DOUBLES: dict[int, int] = {}
START_JAILED: dict[int, bool] = {}
START_GOOJF: dict[int, int] = {}
START_PROPERTIES: dict[int, dict[str, list[int]]] = {}
# {player.index: {"property_type": [property.index, ]}, }
START_COLOR_SETS: dict[int, list[str]] = {}
# {player.index: ["color_set", ], }
# Mismatched color sets with properties may cause unexpected behavior

WELCOME_MESSAGE = False  # True
FILE_CHECK = True  # True
LOAD_FILES = True  # True
BANKRUPTCY_CHECK = True  # True
SKIP_DICE = False  # False
SKIP_JAIL = False  # False
SINGLE_PLAYER = True  # False
PLAYER_COUNT_OVERRIDE = 0  # 0
# Numbers <=0 is disabling
