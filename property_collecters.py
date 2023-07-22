from Models.Property import Street, Tax, Utility, Railroad, ComChest, Chance, Corner


def load_squares() -> dict[int, Street | Tax | Utility | Railroad | ComChest | Chance | Corner]:
    with open("squares.txt", "r") as squaresFile:
        squares = eval(squaresFile.read())

    all_squares: dict[int, Street | Tax | Utility | Railroad | ComChest | Chance | Corner] = {}
    count = 0
    for square in squares:
        all_squares[count] = get_type(squares[square])
        count += 1

    return all_squares



def get_type(property_getter: dict[str, str | int | dict | bool]) -> Street | Tax | Utility | Railroad | ComChest | Chance | Corner | str:
    if property_getter["type"] == "street":
        return Street(
            name=property_getter["name"],
            price=property_getter["price"],
            property_type=property_getter["type"],
            color=property_getter["color"],
            improvement_lvl=property_getter["improvement_lvl"],
            improvement_price=property_getter["improvement_price"],
            mortgaged=property_getter["mortgaged"],
            rent_levels=property_getter["rent_levels"],
            owner=property_getter["owner"]
        )
    elif property_getter["type"] == "tax":
        return Tax(
            tax=property_getter["price"],
            name=property_getter["name"],
            property_type=property_getter["type"]
        )
    elif property_getter["type"] == "utility":
        return Utility(
            name=property_getter["name"],
            price=property_getter["price"],
            property_type=property_getter["type"],
            improvement_lvl=property_getter["improvement_lvl"],
            mortgaged=property_getter["mortgaged"],
            owner=property_getter["owner"]
        )
    elif property_getter["type"] == "railroad":
        return Railroad(
            name=property_getter["name"],
            price=property_getter["price"],
            property_type=property_getter["type"],
            improvement_lvl=property_getter["improvement_lvl"],
            mortgaged=property_getter["mortgaged"],
            rent_levels=property_getter["rent_levels"],
            owner=property_getter["owner"]
        )
    elif property_getter["type"] == "comChest":
        return ComChest(
            name=property_getter["name"],
            property_type=property_getter["type"]
        )
    elif property_getter["type"] == "chance":
        return Chance(
            name=property_getter["name"],
            property_type=property_getter["type"]
        )
    elif property_getter["type"] == "corner":
        return Corner(
            name=property_getter["name"],
            property_type=property_getter["type"]
        )
    else:
        return "Error"
