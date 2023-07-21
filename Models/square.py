from typing import Optional


class Square:

    def __init__(
            self,
            name: str,
            square_type: str,
            price: int = None,
            color: str = None,
            owner: str = None,
            improvement_lvl: str = None,
            improvement_price: str = None,
            mortgaged: bool = False,
            rent_levels: Optional[dict[int, int]] = None,
    ):
        self._name = name
        self._square_type = square_type
        self._price = price
        self._color = color
        self._owner = owner
        self._improvement_lvl = improvement_lvl
        self._improvement_price = improvement_price
        self._mortgaged = mortgaged
        self._rent_levels = rent_levels

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def square_type(self):
        return self._square_type

    @square_type.setter
    def square_type(self, value):
        self._square_type = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value

    @property
    def improvement_lvl(self):
        return self._improvement_lvl

    @improvement_lvl.setter
    def improvement_lvl(self, value):
        self._improvement_lvl = value

    @property
    def improvement_price(self):
        return self._improvement_price

    @improvement_price.setter
    def improvement_price(self, value):
        self._improvement_price = value

    @property
    def mortgaged(self):
        return self._mortgaged

    @mortgaged.setter
    def mortgaged(self, value):
        self._mortgaged = value

    @property
    def rent_levels(self):
        return self._rent_levels

    @rent_levels.setter
    def rent_levels(self, value):
        self._rent_levels = value
