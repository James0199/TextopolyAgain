# These constants are for debugging, don't change them if you want to play normally
# However, you can change them if you want to (cheat)
# Changing these might cause the game to be buggy as they're not often tested

if __name__ == "__main__":
    print(
        "Please run the TextopolyAgain.py file,\n"
        "This module is meant to be imported."
    )
    exit()

LOCATION_LOCK = False  # False
DOUBLES_LOCK = False  # False

START_LOCATION = 0  # 0
START_BALANCE = 1500  # 1500
START_DOUBLES = 0  # 0
START_JAILED = False  # False
START_GOOJF = False  # False
START_PROPERTIES = {}  # {}
# Structure: {player.index: [property.index, ...], ...}

BANKRUPTCY_CHECK = True  # True
SKIP_DICE = False  # False
SINGLE_PLAYER = False  # False
