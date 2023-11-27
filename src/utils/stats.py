def main_stats(player, square):
    print(
        f"\nPlayer {player.INDEX + 1}'s turn"
        f"\nBalance: ${player.balance}"
        f"\nSquare: {square.INDEX} - {square.NAME}"
    )


def stat_options(player, player_list: dict, squares: dict):
    print(
        "\n(p) View _p_layer stats\n"
        "(s) View _s_quare (properties) stats\n"
        "(b) View all squares' indexes (_b_oard)"
    )
    while True:
        option = input("[stats] Enter option:")
        if not option:
            return
        option = option[0].casefold()
        match option:
            case "p":
                print(f"\nYour player index: {player.INDEX+1}")

                while True:
                    try:
                        player_select = input("[stats] Enter player (index):")
                        if not option:
                            break

                        player_select = player_list[int(player_select) - 1]
                        player_stats(vars(player_select).items(), squares)
                    except (ValueError, IndexError, KeyError):
                        print("Invalid player")
            case "s":
                player_properties = player.properties.values()
                if any(player_properties):
                    property_list = [
                        i for properties in player_properties for i in properties
                    ]
                    print("Your properties' indexes:", ", ".join(property_list))

                while True:
                    try:
                        square_select = input(
                            "\n[stats] Enter square (property) index:"
                        )
                        if not square_select:
                            break

                        square_select = squares[int(square_select)]
                        square_stats(vars(square_select))
                    except (ValueError, IndexError, KeyError):
                        print("Invalid square (property)")
            case "b":
                print()
                for i, square in squares.items():
                    print(f"{i}: {square.NAME}")
                    if i != 0 and i % 5 == 0:
                        input("\n(More)")
            case "":
                break
            case _:
                print("Invalid option")
                continue


def player_stats(stats, squares):
    print()
    for attr, value in stats:
        match attr:
            case "INDEX":
                print(f"Player index: {value+1}")
            case "balance":
                print(f"{attr.capitalize()}: ${value}")
            case "doubles":
                print(f"Consecutive doubles: {value}")
            case "color_sets":
                if value:
                    print(f"Owned color sets: {', '.join(value)}")
            case "properties":
                if any(value.values()):
                    input("(More)")
                for property_type, properties in value.items():
                    if not properties:
                        continue
                    print(property_type.capitalize())
                    for property_ in properties:
                        print(squares[property_].NAME)
    print()


def square_stats(stats):
    print(f"\nIndex (location): {stats['INDEX']}\nName: {stats['NAME']}")
    if stats["SQUARE_TYPE"] == "com_chest":
        print("Square type: Community chest")
    else:
        print(f"Square type: {stats['SQUARE_TYPE'].capitalize()}")
    if stats["SQUARE_TYPE"] == "tax":
        print(f"Tax: ${stats['COST']}")
    elif stats["SQUARE_TYPE"] in ("street", "railroad", "utility"):
        ownable_stats(stats)


def ownable_stats(stats):
    print(f"Purchase price: ${stats['COST']}")

    if stats["owner"] is None:
        print("Owner: No one")
    else:
        print(f"Owner: player {stats['owner'] + 1}")
    if stats["owner"] is not None:
        if stats["mortgaged"]:
            print(f"Mortgaged: Yes")
        else:
            print("Mortgaged: No")

    if stats["SQUARE_TYPE"] == "street":
        print(f"Color: {stats['COLOR']}")

    title_deed(stats)


def title_deed(stats):
    input("\n(More)")
    try:
        rent_levels = stats["RENT_LEVELS"]
    except KeyError:
        rent_levels = {}

    print("Title deed:")
    if stats["SQUARE_TYPE"] == "street":
        print(
            f"Rent: ${rent_levels[0]}\n"
            f"With color set: ${rent_levels[0]*2}\n"
            f"With 1 house: ${rent_levels[1]}"
        )
        for i in range(2, 5 + 1):
            print(f"Rent with {i} houses: ${rent_levels[i]}")
    elif stats["SQUARE_TYPE"] == "railroad":
        print(f"Rent: ${rent_levels[0]}")
        for i in range(1, 3 + 1):
            print(f"{i} Railroads owned: {rent_levels[i]}")
    else:
        print(
            "Rent if 1 utility owned: 4x amount shown on dice\n"
            "2 utilities owned: 10x amount shown on dice"
        )
    print(f"\nMortgage value: ${stats['COST'] // 2}")
