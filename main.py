from Models.game import Game
from Models.player import Player
from Models.square import Square


def load_squares() -> dict[int, Square]:
    squares_list: dict[int, Square] = {}
    with open("squares.txt", "r") as squaresFile:
        squares = eval(squaresFile.read())

    count = 0

    for square in squares:
        squares_list[count] = Square(
                name=squares[square]["name"],
                square_type=squares[square]["type"],
                price=squares[square].setdefault("price", None),
                color=squares[square].setdefault("color", None),
                owner=squares[square].setdefault("owner", None),
                improvement_lvl=squares[square].setdefault("improvement_lvl", None),
                improvement_price=squares[square].setdefault("improvement_price", None),
                mortgaged=squares[square].setdefault("mortgaged", False),
                rent_levels=squares[square].setdefault("rent_levels", None)
            )
        count += 1

    return squares_list

def start():
    print("Game is initialising...")

    squares_for_game = load_squares()

    player_list: list[Player] =  []

    while True:
        try:
            player_count: int = int(input("How many players do you want? (2-8 players): "))
            if 2 <= player_count <= 8:
                break
            raise ValueError
        except ValueError:
            print("Enter a valid number")



    for count in range(0, player_count):
        player_list.append(
            Player(
                location=squares_for_game[0],
            )
        )

    new_game = Game()