from Models.player import Player
from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner


class Game:

    def __init__(self,
                 players: list[Player],
                 squares: dict[int, Street | Tax | Utility | Railroad, ComChest, Chance, Corner]
                 ):
        self.players = players
        self.squares = squares

    def start(self):
        print("Game is initialising....")

