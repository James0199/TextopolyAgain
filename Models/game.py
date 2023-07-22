from Models.player import Player
from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner


class Game:

    def __init__(self,
                 players: list[Player],
                 squares: dict[int, Street | Tax | Utility | Railroad | ComChest | Chance | Corner]
                 ):
        self._players = players
        self._squares = squares

    @property
    def players(self):
        return self._players

    @property
    def squares(self):
        return self._squares

