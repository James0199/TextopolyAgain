class Property:

    def __init__(self, name: str, property_type: str):
        self._name = name
        self._property_type = property_type

    @property
    def name(self):
        return self._name

    @property
    def property_type(self):
        return self.__class__.__name__


class Street(Property):

    def __init__(self, name: str, price: int, property_type: str, color: str, improvement_lvl: int = 0,
                 improvement_price: int = 0, mortgaged: bool = False, rent_levels: dict[int, int] = None,
                 owner=None):
        super().__init__(name, property_type)
        self._price = price
        self._color = color
        self.improvement_lvl = improvement_lvl
        self._improvement_price = improvement_price
        self.mortgaged = mortgaged
        self._rent_levels = rent_levels
        self.owner = owner

    @property
    def price(self):
        return self._price

    @property
    def color(self):
        return self._color

    @property
    def improvement_price(self):
        return self._improvement_price

    @property
    def rent_levels(self):
        return self._rent_levels


class Tax(Property):

    def __init__(self, tax, name: str, property_type: str):
        super().__init__(name, property_type)
        self._tax = tax

    def pay_tax(self, player):
        player.remove_balance(self._tax)


class Railroad(Property):

    def __init__(self, name: str, property_type: str, price: int, improvement_lvl: int = 0, mortgaged: bool = False,
                 rent_levels: dict[int, int] = None, owner=None):
        super().__init__(name, property_type)
        self._price = price
        self._rent_levels = rent_levels
        self.improvement_lvl = improvement_lvl
        self.mortgaged = mortgaged
        self.owner = owner

    @property
    def price(self):
        return self._price

    @property
    def rent_levels(self):
        return self._rent_levels


class Utility(Property):

    def __init__(self, name: str, property_type: str, price: int, improvement_lvl: int = 0, mortgaged: bool = False,
                 owner=None):
        super().__init__(name, property_type)
        self._price = price
        self.improvement_lvl = improvement_lvl
        self.mortgaged = mortgaged
        self.owner = owner

    @property
    def price(self):
        return self._price


class ComChest(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)


class Chance(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)


class Corner(Property):

    def __init__(self, name: str, property_type: str):
        super().__init__(name, property_type)
