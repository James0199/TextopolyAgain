def mortgage(player, files):
    print_options(player, files)
    while True:
        try:
            selected_type = input("\n[mortgage] Select property type:")
            if not selected_type:
                return
            selected_type = selected_type[0].casefold()
            for property_type in player.properties:
                if selected_type[0].casefold() == property_type[0].casefold():
                    selected_type = property_type
                    print(f"Selected {property_type} type.")
            properties: list = player.properties[selected_type]
        except (IndexError, KeyError):
            print("Invalid property type")
            continue

        option = property_select(selected_type, properties)
        if not str(option):
            return

        property_obj = files.squares[properties[option]]
        if not property_obj.mortgaged:
            mortgage_cost = property_obj.COST // 2
            property_obj.mortgaged = True
            print(f"{selected_type.capitalize()} mortgaged for ${mortgage_cost}.")
            player.balance += mortgage_cost
        elif property_obj.mortgaged:
            unmortgage_cost = round((property_obj.COST / 2) * 1.1)
            if player.balance < unmortgage_cost:
                print("Not enough balance")
                continue
            property_obj.mortgaged = False
            print(f"{selected_type.capitalize()} unmortgaged for ${unmortgage_cost}.")
            player.balance -= unmortgage_cost


def print_options(player, files):
    print("\nYou currently have these properties:")
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
            for i, owned_property in enumerate(player.properties[property_type].copy()):
                owned_property = files.squares[owned_property]
                if owned_property.SQUARE_TYPE == "street":
                    if owned_property.improvement_level > 0:
                        continue
                print(f"{i+1}. {owned_property.NAME}")


def property_select(selected_type, properties) -> int | str:
    while True:
        option = input(f"[mortgage] Select {selected_type}:")
        if not option:
            return option
        try:
            option = int(option) - 1
            if option not in range(len(properties)):
                raise IndexError
            return option
        except (ValueError, IndexError):
            if option:
                print("Invalid index")
            continue
