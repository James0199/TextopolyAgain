def exchange(player, files):
    applicable_streets, options = get_options(player, files)
    print('Type "m" to return to last menu')
    while True:
        if applicable_streets["buy"]:
            print("(b) _B_uy")
        if applicable_streets["sell"]:
            print("(s) _S_ell")
        option = input("[houses] Enter option:")
        if option:
            option = option[0].casefold()
        if option not in options:
            print("Invalid option")
            continue
        match option:
            case "b":
                house_action(applicable_streets, "buy", player)
                get_options(player, files, True)
            case "s":
                house_action(applicable_streets, "sell", player)
                get_options(player, files, True)
            case "m":
                return
            case _:
                print("Invalid option")
                continue


def get_options(player, files, no_print=False) -> tuple[dict, list] | dict:
    applicable_streets = {"buy": [], "sell": []}
    color_sets = {
        color: [
            files.squares[street] for street in files.PROPERTY_SETS["street"][color]
        ]
        for color in player.color_sets
    }
    for color in color_sets:
        house_cap = max([street_.improvement_level for street_ in color_sets[color]])
        for street in color_sets[color]:
            if (
                street.improvement_level <= 0
                or street.improvement_level + 1 <= house_cap
            ):
                applicable_streets["buy"].append(street)
                continue
            elif (
                street.improvement_level >= 5
                or street.improvement_level > house_cap - 1
            ):
                applicable_streets["sell"].append(street)
                continue
    if no_print:
        return applicable_streets

    options = []
    if applicable_streets["buy"]:
        options.append("b")
        print("You can buy houses on these streets:")
        for street in applicable_streets["buy"]:
            print(f"- {street.NAME}")
    if applicable_streets["sell"]:
        options.append("s")
        print("You can sell houses on these streets:")
        for street in applicable_streets["sell"]:
            print(f"- {street.NAME}")
    return applicable_streets, options


def house_action(applicable_streets, action, player):
    for i, street in enumerate(applicable_streets[action]):
        print(f"{i+1}. {street.NAME}")
    while True:
        street_index = input("[houses] Select street:")
        if street_index == "m":
            break
        try:
            street_index = int(street_index) - 1
            if street_index not in range(len(applicable_streets[action])):
                raise ValueError
        except ValueError:
            print("Invalid INDEX")
            continue
    if street_index == "m":
        return
    selected_street = applicable_streets[action][street_index]
    if action == "buy":
        selected_street.improvement_level += 1
        player.balance -= selected_street.IMPROVEMENT_COST
        print(
            f"House bought on {selected_street.NAME} for "
            f"${selected_street.IMPROVEMENT_COST}"
        )
    else:
        selected_street.improvement_level -= 1
        player.balance += selected_street.IMPROVEMENT_COST // 2
        print(
            f"House sold on {selected_street.NAME} for "
            f"${selected_street.IMPROVEMENT_COST // 2}"
        )
