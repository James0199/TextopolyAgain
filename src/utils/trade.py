try:
    from options.debug_cheats import *
except ModuleNotFoundError:
    print("Can't find options/debug_cheats.py")
    raise SystemExit


class PlayerType:
    def __init__(self):
        self.INDEX: int = 0
        self.location: int = 0
        self.balance: int = 0
        self.doubles: int = 0
        self.properties: dict[str, list[int]] = {}
        self.color_sets: list[str] = []


sender_offer, receiver_offer, status, accepted = {}, {}, None, []
player_list, jailed_list, squares = {}, {}, {}
sender: None | PlayerType = None
receiver: None | PlayerType = None


def set_globals(sender_, player_list_, jailed_list_, squares_):
    global sender_offer, receiver_offer, status, accepted, sender, receiver
    global player_list, jailed_list, squares

    player_list, jailed_list, squares = player_list_, jailed_list_, squares_
    sender = sender_
    receiver = None
    status = None
    sender_offer = {
        "property": {"street": [], "railroad": [], "utility": []},
        "money": 0,
        "goojf": 0,
    }
    receiver_offer = receiver_offer = {
        "property": {"street": [], "railroad": [], "utility": []},
        "money": 0,
        "goojf": 0,
    }
    accepted = [False, False]


def set_side(sender_side, type_="player") -> PlayerType | dict | str:
    match type_:
        case "player":
            if sender_side:
                return sender
            return receiver
        case "offer":
            if sender_side:
                return sender_offer
            return receiver_offer
        case "input":
            if sender_side:
                return input("\n[trade] Add to sender offer:")
            return input("\n[trade] Add to receiver offer:")


def start_trade(sender_, *databases):
    set_globals(sender_, *databases)

    trade()
    if not status:
        print("Trade canceled.")
        return
    elif status:
        apply_trade(sender, receiver, receiver_offer)
        apply_trade(receiver, sender, sender_offer)
        print("Trade successful")


def trade():
    global accepted, status

    determine_receiver()
    if receiver == -1:
        return
    sender_side = True
    options = get_options(sender_side)
    while True:
        player = set_side(sender_side)
        player_offer = set_side(sender_side, "offer")
        category = set_side(sender_side, "input")
        if category:
            category = category[0].casefold()
            if category not in options:
                category = "_"

        match category:
            case "p":
                property_trade(player, player_offer)
            case "b":
                money_trade(player, player_offer)
            case "g":
                goojf_trade(jailed_list[set_side(sender_side).INDEX], player_offer)
            case "":
                return
            case "a":
                review_trade(player_offer)
                confirm = input("[trade] Are you sure?(y/[n]):")
                try:
                    if confirm[0].casefold() != "y":
                        raise IndexError
                except IndexError:
                    print("Trade not accepted.")
                    continue
                accepted[int(not sender_side)] = True
                if all(accepted):
                    status = True
                    return

                sender_side = not sender_side
                options = get_options(sender_side)
            case "t":
                sender_side = not sender_side
                options = get_options(sender_side)
                continue
            case _:
                print("Invalid option")
                continue


def determine_receiver():
    global receiver
    while True:
        try:
            receiver = input("\n[trade] Player (index) you want to trade with:")
            if not receiver:
                receiver = -1
                return
            receiver = int(receiver) - 1
            if receiver not in player_list or receiver == sender.INDEX:
                raise ValueError
            receiver = player_list[receiver]
            return
        except ValueError:
            print("Invalid player")
            continue


def get_options(sender_side) -> list[str]:
    player = set_side(sender_side)
    options = []
    print(
        '\nType "t" to switch trading sides,\n'
        '"a" to accept/unaccept trade (Switches sides automatically)'
    )

    print("\nYou currently have:")
    if any(player.properties.values()):
        print("(p) _P_roperties")
        options.append("p")
    if sender.balance > 0:
        print("(b) Money (_b_alance)")
        options.append("b")
    if jailed_list[player.INDEX]["goojf"]:
        print("(g) _G_et Out Of Jail Free cards")
        options.append("g")
    return options


def property_options(prompt, player) -> list | None:
    options = []
    match prompt:
        case "t":
            print("\nYou have these property types:")
            if any(
                [
                    squares[street].improvement_level <= 0
                    for street in player.properties["street"]
                ]
            ):
                print("(s) _S_treet")
                options.append("s")
            elif player.properties["railroad"]:
                print("(r) _R_ailroad")
                options.append("r")
            elif player.properties["utility"]:
                print("(u) _U_tility")
                options.append("u")
            return options
        case "s":
            print("\nYou have these applicable street(s):")
            for i, street in enumerate(player.properties["street"]):
                street = squares[street]
                if street.improvement_level > 0:
                    continue
                print(f"{i+1}. {street.NAME}")
        case "r":
            print("\nYou have these applicable railroad(s):")
            for i, railroad in enumerate(player.properties["railroad"]):
                railroad = squares[railroad]
                print(f"{i+1}. {railroad.NAME}")
        case "u":
            if len(player.properties["utility"]) > 1:
                print("\nYou have these applicable utilities:")
            else:
                print("\nYou have this applicable utility:")
            for i, util in enumerate(player.properties["utility"]):
                util = squares[util]
                print(f"{i+1}. {util.NAME}")


def property_trade(player, player_offer):
    while True:
        options = property_options("t", player)
        option = input("\n[trade] Select type:")
        if not option:
            break
        option = option[0].casefold()
        if option not in options:
            print("Invalid type")
            continue
        property_options(option, player)
        option = {"s": "street", "r": "railroad", "u": "utility"}[option]
        property_select(player, player_offer, option)


def property_select(player, player_offer, property_type):
    property_offer = player_offer["property"][property_type]
    properties = player.properties[property_type]

    while True:
        try:
            option = input(f"\n[trade] Select {property_type}:")
            if not option:
                break
            option = int(option) - 1
            if option not in range(len(properties)):
                raise ValueError
            if option in property_offer:
                property_offer.remove(properties[option])
                print(f"{property_type.capitalize()} removed from offer")
                continue
            property_offer.append(properties[option])
            print(f"{property_type.capitalize()} added to offer")
        except ValueError:
            print("Invalid option")
            continue


def money_trade(player, player_offer):
    balance = player.balance
    while True:
        amount = input("[trade] How much money?:")
        if not amount:
            return
        try:
            amount = abs(int(amount))
            if amount > balance:
                raise ValueError
            break
        except ValueError:
            print("Invalid amount")

    player_offer.update({"money": amount})
    print(f"Money offer set to ${amount}")


def goojf_trade(jail_cell, player_offer):
    while True:
        amount = input("[trade] How many GOOJF cards?:")
        if not amount:
            return
        try:
            amount = abs(int(amount))
            if amount > jail_cell["goojf"]:
                raise ValueError
            break
        except ValueError:
            print("Invalid amount")
    player_offer.update({"goojf": amount})
    print(f"GOOJF cards offer set to {amount} card(s)")


def review_trade(offer):
    print("\nHere's an overview of your offer:")
    for property_type, properties in offer["property"].items():
        if not properties:
            continue
        print(f"{property_type.capitalize()}:")
        for offered_property in properties:
            print(f"- {squares[offered_property].NAME}")
    if offer["money"]:
        print(f"Money: {offer['money']}")
    if offer["goojf"]:
        print(f"GOOJF cards: {offer['goojf']}")


def apply_trade(player, other, other_offer):
    player_goojf = jailed_list[player.INDEX]["goojf"]
    other_goojf = jailed_list[other.INDEX]["goojf"]

    for property_type in player.properties:
        player.properties[property_type].extend(other_offer["property"][property_type])
        other.properties[property_type] = [
            property_
            for property_ in other.properties[property_type]
            if property_ not in other_offer["property"][property_type]
        ]
        for property_ in other_offer["property"][property_type]:
            property_ = squares[property_]
            property_.owner = player.INDEX

    player.balance += other_offer["money"]
    other.balance -= other_offer["money"]

    player_goojf += other_offer["goojf"]
    other_goojf -= other_offer["goojf"]
