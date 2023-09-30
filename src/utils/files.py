from options.debug_cheats import *


def load_files():
    if not LOAD_FILES:
        return
    global squares, COM_CHEST, CHANCE, PROPERTY_SETS
    try:
        with (
            open("data/squares.txt", "r+") as squares_file,
            open("data/COM_CHEST.txt", "r+") as com_chest_file,
            open("data/CHANCE.txt", "r+") as chance_file,
            open("data/PROPERTY_SETS.txt", "r+") as property_sets_file,
        ):
            squares = eval(squares_file.read())
            COM_CHEST = eval(com_chest_file.read())
            CHANCE = eval(chance_file.read())
            PROPERTY_SETS = eval(property_sets_file.read())
    except FileNotFoundError:
        if FILE_CHECK:
            print("Please download all files")
            raise SystemExit


def dict_to_obj(dto_funct):
    global squares
    squares = {index: dto_funct(square) for index, square in squares.items()}


COM_CHEST, CHANCE, PROPERTY_SETS, squares = {}, {}, {}, {}
load_files()
