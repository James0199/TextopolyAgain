"""Game configuration

Don't change these constants if you want to play normally.
However, you can change them to modify how the game works.
Changing these might cause the game to be buggy as they're not often tested.
If you do find a bug, please submit an issue on this project's Github page.
"""

MODULE_GUARD = False  # True

if __name__ == "__main__" and MODULE_GUARD:
    print(
        "Please run the TextopolyAgain.py file,\n"
        "This module is meant to be imported."
    )
    exit()

# OPTION = Value  # Default value
LOCATION_LOCK = False  # False
DOUBLES_LOCK = False  # False

START_LOCATION = 0  # 0
START_BALANCE = 1500  # 1500
START_DOUBLES = 0  # 0
START_JAILED = False  # False
START_GOOJF = 0  # 0
START_PROPERTIES: dict[int, dict[str, list]] = {}  # {}
# {player.index: {"property_type": [property.index, ]}, }

WELCOME_MESSAGE = True  # True
FILE_CHECK = True  # True
LOAD_FILES = True  # True
BANKRUPTCY_CHECK = True  # True
SKIP_DICE = True  # False
SKIP_JAIL = False  # False
SINGLE_PLAYER = False  # False
PLAYER_COUNT_OVERRIDE = 0  # 0
# Negative numbers and zero equals disabling
