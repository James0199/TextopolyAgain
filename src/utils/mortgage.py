def mortgage(player, files):
    print_options(player, files)
    while True:
        try:
            selected_type = input("\nSelect type:")[0].casefold()
            if selected_type == "m":
                return
            for property_type in player.properties:
                if selected_type[0].casefold() == property_type[0].casefold():
                    selected_type = property_type
            properties: list = player.properties[selected_type]
        except (IndexError, KeyError):
            print("Invalid type")
            continue

        option = property_select(selected_type, properties)
        if option == "m":
            continue

        property_obj = files.squares[properties[option]]
        if not property_obj.mortgaged:
            property_obj.mortgaged = True
            print(f"{selected_type.capitalize()} mortgaged.")
            player.balance += property_obj.COST
            print(player.balance, property_obj.COST)
        elif property_obj.mortgaged:
            unmortgage_cost = round(property_obj.COST * 1.1)
            if player.balance < unmortgage_cost:
                print("Not enough balance")
                continue
            property_obj.mortgaged = False
            print(f"{selected_type.capitalize()} unmortgaged.")
            player.balance -= round(property_obj.COST * 1.1)


def print_options(player, files):
    print(
        '\nType "m" to return to last menu\n'
        "\nYou currently have these properties:"
    )
    for property_type in player.properties:
        if player.properties[property_type]:
            if property_type == "street" and all(
                    [
                        files.squares[street].improvement_level > 0
                        for street in player.properties["street"]
                    ]
            ):
                continue
            print(f"{property_type.capitalize()}:")
            for i, owned_property in enumerate(
                    player.properties[property_type]
            ):
                if owned_property.TYPE == "street":
                    if owned_property.improvement_level > 0:
                        continue
                print(f"{i+1}. {files.squares[owned_property].NAME}")


def property_select(selected_type, properties) -> int:
    while True:
        option = input(f"\nSelect {selected_type}:")
        try:
            if option[0].casefold() == "m":
                option = option[0].casefold()
                break
            option = int(option) - 1
            if option not in range(len(properties)):
                raise IndexError
            return option
        except (ValueError, IndexError):
            if option:
                print("Invalid INDEX")
            continue
