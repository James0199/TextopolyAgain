from Models.game import Game
from Models.player import Player
from property_collecters import load_squares


def start():
    print("Game is initialising...")

    player_list: list[Player] = []

    while True:
        try:
            player_count: int = int(input("How many players do you want? (2-8 players): "))
            if 2 <= player_count <= 8:
                break
            raise ValueError
        except ValueError:
            print("Enter a valid number")


all_squares = load_squares()

for square in all_squares:
    print(square.name)
