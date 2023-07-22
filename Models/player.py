from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner


class Player:

    def __init__(
            self,
            location: Street | Tax | Utility | Railroad | ComChest | Chance | Corner,
            balance: int,
            properties: dict[int, Street | Tax | Utility | Railroad | ComChest | Chance | Corner] | None,
            extras: dict[str, str] | None
    ):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras

    def location(self) -> Street | Tax | Utility | Railroad | ComChest | Chance | Corner:
        return self.location.name

    def balance(self):
        return self.balance

    def properties(self):
        return self.properties

    def extras(self):
        return self.extras

    def add_balance(self, value):
        self.balance += value

    def remove_balance(self, value):
        self.balance -= value
