from options.debug_cheats import *


class PlayerType:
    def __init__(self):
        self.INDEX: int = 0
        self.location: int = 0
        self.balance: int = 0
        self.doubles: int = 0
        self.properties: dict[str, list[int]] = {}
        self.color_sets: list[str] = []


(sender_offer, receiver_offer, status, accepted,
 player_list, jailed_list, squares) = {}, {}, None, [], {}, {}, {}
sender: None | PlayerType = None
receiver: None | PlayerType = None


def start_trade(sender_, player_list_, jailed_list_, squares_):
    global sender_offer, receiver_offer, accepted,\
        sender, receiver, player_list, jailed_list, squares
    sender, player_list, jailed_list, files = (
        sender_, player_list_, jailed_list_, squares_)

    sender_offer = {
        "property": {"street": [], "railroad": [], "utility": []},
        "money": 0,
        "goojf": 0,
    }
    receiver_offer = {
        "property": {"street": [], "railroad": [], "utility": []},
        "money": 0,
        "goojf": 0,
    }
    accepted = [False, False]

    trade()
    if status is None:
        print("Trade canceled")
    elif status is True:
        apply_trade(sender, receiver, receiver_offer)
        apply_trade(receiver, sender, sender_offer)
        print("Trade successful")


def trade():
    global accepted, status
    determine_receiver()
    sender_side = True
    options = get_options(sender_side)
    while True:
        if sender_side:
            offer = sender_offer
            category = input("\nAdd to sender offer:")
        else:
            offer = receiver_offer
            category = input("\nAdd to receiver offer:")
        if category in options:
            category = category[0].casefold()

        match category:
            case "p":
                property_trade(sender_side)
            case "b":
                money_trade(sender_side)
            case "g":
                goojf_trade(sender_side)
            case "m":
                return
            case "a":
                review_trade(offer)
                confirm = input("Are you sure?(y/[n]):")
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
            receiver = (
                int(input("\nPlayer (index) you want to trade with:")) - 1
            )
            if (
                receiver not in player_list
                or SINGLE_PLAYER
                or receiver == sender.INDEX
            ):
                raise ValueError
            receiver = player_list[receiver]
            return
        except ValueError:
            print("Invalid player")
            continue


def get_options(sender_side) -> list[str]:
    if sender_side:
        player = sender
    else:
        player = receiver
    print(
        '\nType "m" to return to last menu, "t" to switch trading sides,\n'
        '"a" to accept/unaccept trade (Switches sides automatically)\n'
    )
    options = []
    print("\nYou currently have:")
    if player.properties:
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


def property_trade(sender_side):
    if sender_side:
        player = sender
        player_offer = sender_offer
    else:
        player = receiver
        player_offer = receiver_offer

    while True:
        options = property_options("t", player)
        option = input("\nSelect type:")[0].casefold()
        if option == "m":
            break
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
            option = input(f"\nSelect {property_type}:")
            if option == "m":
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


def money_trade(sender_side):
    if sender_side:
        balance = sender.balance
    else:
        balance = receiver.balance

    while True:
        try:
            amount = abs(int(input("How much money?:")))
            if amount > balance:
                raise ValueError
            break
        except ValueError:
            print("Invalid amount")
    if sender_side:
        sender_offer.update({"money": amount})
    else:
        receiver_offer.update({"money": amount})
    print(f"Money offer set to ${amount}")


def goojf_trade(sender_side):
    if sender_side:
        jail_cell = jailed_list[sender.INDEX]
    else:
        jail_cell = jailed_list[receiver.INDEX]

    while True:
        try:
            amount = abs(int(input("How many GOOJF cards?:")))
            if amount > jail_cell["goojf"]:
                raise ValueError
            break
        except ValueError:
            print("Invalid amount")
    if sender_side:
        sender_offer.update({"goojf": amount})
    else:
        receiver_offer.update({"goojf": amount})
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
        player.properties[property_type].extend(
            other_offer["property"][property_type]
        )
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
