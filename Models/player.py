from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner


class Player:

    def __init__(
            self,
            location: dict[int, Street | Tax | Utility | Railroad, ComChest, Chance, Corner],
            balance: int,
            properties: dict[int, Street | Tax | Utility | Railroad, ComChest, Chance, Corner],
            extras: dict[str, str]
    ):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras

    def add_balance(self, value):
        self.balance += value

    def remove_balance(self, value):
        self.balance -= value
