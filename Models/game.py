from player import Player
from square import Square


class Game:

    def __init__(self,
                 players: list[Player],
                 squares: dict[int, Square]
                 ):
        self.players = players
        self.squares = squares

    def start(self):
        print("Game is initialising....")

