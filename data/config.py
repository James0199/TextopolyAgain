"""
These constants are used for debugging, don't change them if you want to play normally
However, you can change them if you want to modify how the game works
Changing these might cause the game to be buggy as they're not often tested
"""

if __name__ == "__main__":
    print(
        "Please run the TextopolyAgain.py file,\n"
        "This module is meant to be imported."
    )
    exit()

# OPTION = Value  # Default Value
LOCATION_LOCK = False  # False
DOUBLES_LOCK = False  # False

START_LOCATION = 0  # 0
START_BALANCE = 1500  # 1500
START_DOUBLES = 0  # 0
START_JAILED = False  # False
START_GOOJF = 0  # 0
START_PROPERTIES = {}  # {}
# Structure: {player.index: [property.index, ...], ...}

BANKRUPTCY_CHECK = True  # True
FILE_CHECK = True  # True
SKIP_DICE = True  # False
SKIP_JAIL = False  # False
SINGLE_PLAYER = False  # False
PLAYER_COUNT_OVERRIDE = 0  # 0
# Negative numbers and zero equals disabling
