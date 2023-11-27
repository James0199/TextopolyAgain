try:
    from options.debug_cheats import *
except ModuleNotFoundError:
    print("Couldn't find options/debug_cheats.py")


def load_files():
    global squares, COM_CHEST, CHANCE, PROPERTY_SETS, HELP
    try:
        with (
            open("data/squares.txt", "r+") as squares_file,
            open("data/com_chest.txt", "r+") as com_chest_file,
            open("data/chance.txt", "r+") as chance_file,
            open("data/property_sets.txt", "r+") as property_sets_file,
            open("data/help.txt", "r+") as help_file,
        ):
            squares = eval(squares_file.read())
            COM_CHEST = eval(com_chest_file.read())
            CHANCE = eval(chance_file.read())
            PROPERTY_SETS = eval(property_sets_file.read())
            HELP = help_file.read()

    except FileNotFoundError:
        if FILE_CHECK:
            print("Couldn't find a file,\nPlease download all files")
            raise SystemExit


def dict_to_obj(dto_funct):
    global squares
    squares = {index: dto_funct(square) for index, square in squares.items()}


COM_CHEST, CHANCE, PROPERTY_SETS, squares, HELP = {}, {}, {}, {}, ""
if LOAD_FILES:
    load_files()
BOARD_LENGTH = len(squares)
