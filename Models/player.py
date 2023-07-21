from square import Square


class Player:

    def __init__(
            self,
            location: dict[int, Square],
            balance: int,
            properties: dict[int, Square],
            extras: dict[str, str]
    ):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras
