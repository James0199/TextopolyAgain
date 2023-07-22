from Models.game import Game
from Models.player import Player
from property_collecters import load_squares


def start() -> Game:
    print("Game is initialising...")

    all_squares = load_squares()

    player_list: list[Player] = []

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
                location=all_squares[0],
                balance=0,
                properties=None,
                extras=None
            )
        )

    return Game(
        players=player_list,
        squares=all_squares
    )


game = start()
players = game.players
squares = game.squares
count = 1

for player in players:
    print(f"Player {count} is at: {player.location.name} with balance {player.balance}")
    count += 1
