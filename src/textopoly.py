try:
    from abc import ABC, abstractmethod
    from random import randint
    from options.debug_cheats import *
    from options.house_rules import *
    from utils import files, jail, stats
except ModuleNotFoundError:
    print("Couldn't find a module,\nPlease download all files.")
    raise SystemExit
except ImportError:
    print(
        "Couldn't load a module,\n"
        "If the problem persists,\n"
        "Submit an issue on this project's Github"
    )
    raise SystemExit


if __name__ == "__main__" and MODULE_GUARD:
    print("Please run the main.py file,\n" "This module is meant to be imported.")
    raise SystemExit

print("Loading game...")


class Square(ABC):
    def __init__(self, index: int, name: str, square_type: str):
        self.INDEX = index
        self.NAME = name
        self.SQUARE_TYPE = square_type

    def __repr__(self):
        return str(vars(self))


class Tax(Square):
    def __init__(self, index: int, name: str, square_type: str, cost: int):
        super().__init__(index, name, square_type)
        self.COST = cost

    def landing(self, player):
        print(f"You paid ${self.COST} in {self.NAME}")
        player.balance -= self.COST


class Corner(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        if player.location == 30 and not SKIP_JAIL:
            print("You landed on Go To Jail!")
            jail.jail_player(player)


class ComChest(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        input("Pick Card >")
        card = files.COM_CHEST[randint(0, 13)]
        print(card["name"])
        match card["name"]:
            case "balance":
                player.balance += card["value"]
            case "goojf":
                jail.goojf_card(player, 1)
            case "jail":
                jail.jail_player(player)
            case "go":
                player.location = 0
                player.balance += 200


class Chance(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player, dice_roll):
        input("Pick Card >")
        card = files.CHANCE[randint(0, 12)]
        print(card["name"])
        match card["type"]:
            case "set_loc_property":
                player.location = card["value"]
                if player.location > card["value"]:
                    print("You passed Go")
                    player.balance += 200

                square = files.squares[player.location]
                if square.SQUARE_TYPE == "utility":
                    square.landing(player, dice_roll)
                else:
                    square.landing(player)

            case "balance":
                player.balance += card["value"]
            case "move":
                player.location -= card["value"]
            case "goojf":
                jail.goojf_card(player, 1)
            case "jail":
                jail.jail_player(player)
            case "go":
                player.location = 0
                player.balance += 200


class Ownable(Square, ABC):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        owner: None | int,
        mortgaged: bool,
    ):
        super().__init__(index, name, square_type)
        self.COST = cost
        self.owner = owner
        self.mortgaged = mortgaged

    def purchase(self, player):
        if not NO_AUCTION_ONLY:
            option = input(
                f"\nWould you like to purchase {self.NAME}\nfor ${self.COST}? (y/[n]):"
            )
        else:
            option = "n"

        if option == "y" and player.balance - self.COST >= 0:
            self.receive_property(player, self.COST)
            print(f"You have bought {self.NAME} for ${self.COST}")
        elif NO_AUCTION_ONLY is None or NO_AUCTION_ONLY:
            print("\nAuction!")
            status = auction(self)
            if status is False:
                return
            player, bid = status
            self.receive_property(player, bid)

    @abstractmethod
    def receive_property(self, player, cost):
        ...


class Street(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        color: str,
        improvement_cost: int,
        rent_levels: dict[int, int],
        owner: None | int,
        mortgaged: bool,
        improvement_level: int,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.COLOR = color
        self.improvement_level = improvement_level
        self.IMPROVEMENT_COST = improvement_cost
        self.RENT_LEVELS = rent_levels

    def receive_property(self, player, cost):
        player.balance -= cost
        player.properties["street"].append(self.INDEX)
        self.update_color_set(player)
        files.squares[player.location].owner = player.INDEX

    def update_color_set(self, player):
        color_set = files.PROPERTY_SETS["street"][self.COLOR]
        color_set_squares = [files.squares[square] for square in color_set]

        if all([street.owner == player.INDEX for street in color_set_squares]):
            player.color_sets.append(self.COLOR)
            print(f"Player {player.INDEX} got the {self.COLOR} color set!")

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owner_player = player_data.player_list[self.owner]
        print(f"Player {self.owner + 1} owns this street")
        if owner_player is player:
            return

        rent = self.RENT_LEVELS[self.improvement_level]
        if self.improvement_level > 0:
            print(f"And this street has {self.improvement_level} houses\n")
        elif self.COLOR in player.color_sets and self.improvement_level == 0:
            print("And also owns the color set")
            rent *= 2
        print(f"You'll pay ${rent} to player {owner_player.INDEX + 1}")
        player.balance -= rent
        owner_player.balance += rent


class Railroad(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        rent_levels: dict[int, int],
        owner: None | int,
        mortgaged: bool,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.RENT_LEVELS = rent_levels

    def receive_property(self, player, cost):
        player.balance -= cost
        player.properties["railroad"].append(self.INDEX)
        files.squares[player.location].owner = player.INDEX

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owner_player = player_data.player_list[self.owner]
        owned_railroads = len(
            [
                railroad
                for railroad in files.PROPERTY_SETS["railroad"]
                if self.owner == files.squares[railroad].owner
            ]
        )
        rent = 25 * (2**owned_railroads)
        print(
            f"Player {self.owner + 1} owns this railroad,\n"
            f"And owns {owned_railroads} railroads\n"
            f"You'll pay ${rent} to player {self.owner + 1}"
        )
        player.balance -= rent
        owner_player.balance += rent


class Utility(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        owner: None | int,
        mortgaged: bool,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.OTHER_UTIL = None

    def receive_property(self, player, cost):
        player.balance -= cost
        player.properties["utility"].append(self.INDEX)
        files.squares[player.location].owner = player.INDEX

    def define_other_util(self):
        self.OTHER_UTIL = [
            files.squares[util]
            for util in files.PROPERTY_SETS["utility"]
            if util != self.INDEX
        ][0]

    def landing(self, player, dice_roll):
        self.define_other_util()
        if self.owner is None:
            self.purchase(player)
            return

        owner_player: Player = player_data.player_list[self.owner]
        print(f"Player {self.owner + 1} owns this utility,")
        multiplier = 4
        if self.owner == self.OTHER_UTIL.owner:
            print("And also owns the other utility,")
            multiplier = 10
        print(
            f"You'll pay {multiplier} times your dice roll ({dice_roll}) "
            f"to player {self.owner + 1}"
        )
        player.balance -= dice_roll * multiplier
        owner_player.balance += dice_roll * multiplier


def square_dto(square: dict[str, str | int | None | bool | dict]) -> Square:
    square_args = [arg for arg in square.values()]
    match square["TYPE"]:
        case "street":
            square_args.extend((None, False, 0))
            square_obj = Street(*square_args)
        case "railroad":
            square_args.extend((None, False))
            square_obj = Railroad(*square_args)
        case "utility":
            square_args.extend((None, False))
            square_obj = Utility(*square_args)
        case "com_chest":
            square_obj = ComChest(*square_args)
        case "chance":
            square_obj = Chance(*square_args)
        case "tax":
            square_obj = Tax(*square_args)
        case "corner":
            square_obj = Corner(*square_args)
        case _:
            raise TypeError("Invalid square type")
    return square_obj


files.dict_to_obj(square_dto)


class Trade:
    def __init__(self, sender):
        self.sender_offer = {
            "property": {"street": [], "railroad": [], "utility": []},
            "money": 0,
            "goojf": 0,
        }
        self.receiver_offer = {
            "property": {"street": [], "railroad": [], "utility": []},
            "money": 0,
            "goojf": 0,
        }
        self.sender: Player = sender
        self.receiver: None | Player = None
        self.status: None | bool = None
        self.accepted = [False, False]

        self.trade()
        if self.status is None:
            print("Trade canceled")
        elif self.status is True:
            self.apply_trade(self.sender, self.receiver, self.receiver_offer)
            self.apply_trade(self.receiver, self.sender, self.sender_offer)
            print("Trade successful")

    def __repr__(self):
        return str(vars(self))

    def trade(self):
        self.determine_receiver()
        sender_side = True
        options = self.options(sender_side)
        while True:
            if sender_side:
                offer = self.sender_offer
                category = input("\nAdd to sender offer:")
            else:
                offer = self.receiver_offer
                category = input("\nAdd to receiver offer:")
            if category in options:
                category = category[0].casefold()

            match category:
                case "p":
                    self.property_trade(sender_side)
                case "b":
                    self.money_trade(sender_side)
                case "g":
                    self.goojf_trade(sender_side)
                case "m":
                    return
                case "a":
                    self.review_trade(offer)
                    confirm = input("Are you sure?(y/[n]):")
                    try:
                        if confirm[0].casefold() != "y":
                            raise IndexError
                    except IndexError:
                        print("Trade not accepted.")
                        continue
                    self.accepted[int(not sender_side)] = True
                    if all(self.accepted):
                        self.status = True
                        return

                    sender_side = not sender_side
                    options = self.options(sender_side)
                case "t":
                    sender_side = not sender_side
                    options = self.options(sender_side)
                    continue
                case _:
                    print("Invalid option")
                    continue
            # </editor-fold>

    def determine_receiver(self):
        while True:
            try:
                self.receiver = (
                    int(input("\nPlayer (index) you want to trade with:")) - 1
                )
                if (
                    self.receiver not in player_data.player_list
                    or SINGLE_PLAYER
                    or self.receiver == self.sender.INDEX
                ):
                    raise ValueError
                self.receiver = player_data.player_list[self.receiver]
                return
            except ValueError:
                print("Invalid player")
                continue

    def options(self, sender_side) -> list[str]:
        if sender_side:
            player = self.sender
        else:
            player = self.receiver
        print(
            '\nType "m" to return to last menu, "t" to switch trading sides,\n'
            '"a" to accept/unaccept trade (Switches sides automatically)\n'
        )
        options = []
        print("\nYou currently have:")
        if player.properties:
            print("(p) _P_roperties")
            options.append("p")
        if self.sender.balance > 0:
            print("(b) Money (_b_alance)")
            options.append("b")
        if jail.jailed_list[player.INDEX]["goojf"]:
            print("(g) _G_et Out Of Jail Free cards")
            options.append("g")
        return options

    @staticmethod
    def property_options(prompt, player) -> list | None:
        options = []
        match prompt:
            case "t":
                print("\nYou have these property types:")
                if any(
                    [
                        files.squares[street].improvement_level <= 0
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
                    street: Street = files.squares[street]
                    if street.improvement_level > 0:
                        continue
                    print(f"{i+1}. {street.NAME}")
            case "r":
                print("\nYou have these applicable railroad(s):")
                for i, railroad in enumerate(player.properties["railroad"]):
                    railroad: Railroad = files.squares[railroad]
                    print(f"{i+1}. {railroad.NAME}")
            case "u":
                if len(player.properties["utility"]) > 1:
                    print("\nYou have these applicable utilities:")
                else:
                    print("\nYou have this applicable utility:")
                for i, util in enumerate(player.properties["utility"]):
                    util: Utility = files.squares[util]
                    print(f"{i+1}. {util.NAME}")

    def property_trade(self, sender_side):
        if sender_side:
            player = self.sender
            player_offer = self.sender_offer
        else:
            player = self.receiver
            player_offer = self.receiver_offer

        while True:
            options = self.property_options("t", player)
            option = input("\nSelect type:")[0].casefold()
            if option == "m":
                break
            if option not in options:
                print("Invalid type")
                continue
            self.property_options(option, player)
            option = {"s": "street", "r": "railroad", "u": "utility"}[option]
            self.property_select(player, player_offer, option)

    @staticmethod
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

    def money_trade(self, sender_side):
        if sender_side:
            balance = self.sender.balance
        else:
            balance = self.receiver.balance

        while True:
            try:
                amount = abs(int(input("How much money?:")))
                if amount > balance:
                    raise ValueError
                break
            except ValueError:
                print("Invalid amount")
        if sender_side:
            self.sender_offer.update({"money": amount})
        else:
            self.receiver_offer.update({"money": amount})
        print(f"Money offer set to ${amount}")

    def goojf_trade(self, sender_side):
        if sender_side:
            jail_cell = jail.jailed_list[self.sender.INDEX]
        else:
            jail_cell = jail.jailed_list[self.receiver.INDEX]

        while True:
            try:
                amount = abs(int(input("How many GOOJF cards?:")))
                if amount > jail_cell["goojf"]:
                    raise ValueError
                break
            except ValueError:
                print("Invalid amount")
        if sender_side:
            self.sender_offer.update({"goojf": amount})
        else:
            self.receiver_offer.update({"goojf": amount})
        print(f"GOOJF cards offer set to {amount} card(s)")

    @staticmethod
    def review_trade(offer):
        print("\nHere's an overview of your offer:")
        for property_type, properties in offer["property"].items():
            if not properties:
                continue
            print(f"{property_type.capitalize()}:")
            for offered_property in properties:
                print(f"- {files.squares[offered_property].NAME}")
        if offer["money"]:
            print(f"Money: {offer['money']}")
        if offer["goojf"]:
            print(f"GOOJF cards: {offer['goojf']}")

    @staticmethod
    def apply_trade(player, other, other_offer):
        player_goojf = jail.jailed_list[player.INDEX]["goojf"]
        other_goojf = jail.jailed_list[other.INDEX]["goojf"]

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
                property_: Ownable = files.squares[property_]
                property_.owner = player.INDEX

        player.balance += other_offer["money"]
        other.balance -= other_offer["money"]
        player_goojf += other_offer["goojf"]
        other_goojf -= other_offer["goojf"]


class Mortgage:
    def __init__(self, player):
        self.player = player
        self.mortgage()

    def __repr__(self):
        return str(vars(self))

    def mortgage(self):
        self.print_options()
        while True:
            try:
                selected_type = input("\nSelect type:")[0].casefold()
                if selected_type == "m":
                    return
                for property_type in self.player.properties:
                    if selected_type[0].casefold() == property_type[0].casefold():
                        selected_type = property_type
                properties: list = self.player.properties[selected_type]
            except (IndexError, KeyError):
                print("Invalid type")
                continue

            option = self.property_select(selected_type, properties)
            if option == "m":
                continue

            property_obj: Ownable = files.squares[properties[option]]
            if not property_obj.mortgaged:
                property_obj.mortgaged = True
                print(f"{selected_type.capitalize()} mortgaged.")
                self.player.balance += property_obj.COST
                print(self.player.balance, property_obj.COST)
            elif property_obj.mortgaged:
                unmortgage_cost = round(property_obj.COST * 1.1)
                if self.player.balance < unmortgage_cost:
                    print("Not enough balance")
                    continue
                property_obj.mortgaged = False
                print(f"{selected_type.capitalize()} unmortgaged.")
                self.player.balance -= round(property_obj.COST * 1.1)

    def print_options(self):
        print(
            '\nType "m" to return to last menu\n'
            "\nYou currently have these properties:"
        )
        for property_type in self.player.properties:
            if self.player.properties[property_type]:
                if property_type == "street" and all(
                    [
                        files.squares[street].improvement_level > 0
                        for street in self.player.properties["street"]
                    ]
                ):
                    continue
                print(f"{property_type.capitalize()}:")
                for i, owned_property in enumerate(
                    self.player.properties[property_type]
                ):
                    if type(owned_property) is Street:
                        if owned_property.improvement_level > 0:
                            continue
                    print(f"{i+1}. {files.squares[owned_property].NAME}")

    @staticmethod
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


class HouseBuySell:
    def __init__(self, player):
        self.player = player
        self.menu()

    def __repr__(self):
        return str(vars(self))

    def options(self, no_print=False) -> tuple[dict, list] | dict:
        applicable_streets = {"buy": [], "sell": []}
        color_sets: dict[str, list[Street]] = {
            color: [
                files.squares[street] for street in files.PROPERTY_SETS["street"][color]
            ]
            for color in self.player.color_sets
        }
        for color in color_sets:
            house_cap = max(
                [street_.improvement_level for street_ in color_sets[color]]
            )
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

    def menu(self):
        applicable_streets, options = self.options()
        print('Type "m" to return to last menu')
        while True:
            if applicable_streets["buy"]:
                print("(b) _B_uy")
            if applicable_streets["sell"]:
                print("(s) _S_ell")
            option = input("Enter option:")
            if option:
                option = option[0].casefold()
            if option not in options:
                print("Invalid option")
                continue
            match option:
                case "b":
                    self.house_action(applicable_streets, "buy")
                    self.options(True)
                case "s":
                    self.house_action(applicable_streets, "sell")
                    self.options(True)
                case "m":
                    return
                case _:
                    print("Invalid option")
                    continue

    def house_action(self, applicable_streets, action):
        for i, street in enumerate(applicable_streets[action]):
            print(f"{i+1}. {street.NAME}")
        while True:
            street_index = input("Select street:")
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
        selected_street: Street = applicable_streets[action][street_index]
        if action == "buy":
            selected_street.improvement_level += 1
            self.player.balance -= selected_street.IMPROVEMENT_COST
            print(
                f"House bought on {selected_street.NAME} for "
                f"${selected_street.IMPROVEMENT_COST}"
            )
        else:
            selected_street.improvement_level -= 1
            self.player.balance += selected_street.IMPROVEMENT_COST // 2
            print(
                f"House sold on {selected_street.NAME} for "
                f"${selected_street.IMPROVEMENT_COST // 2}"
            )


print("Loaded successfully!")


class Player:
    def __init__(self, index):
        self.INDEX: int = index
        self.location: int = 0
        self.balance: int = 1500
        self.doubles: int = 0
        self.properties: dict[str, list[int]] = {
            "street": [],
            "railroad": [],
            "utility": [],
        }
        self.color_sets: list[str] = []
        START_ENABLED = any(
            (START_BALANCE, START_LOCATION, START_DOUBLES, START_PROPERTIES)
        )
        if START_ENABLED:
            self.start_options()

    def __repr__(self):
        return str(vars(self))

    def normal_turn(self, dice_roll=(0, 0)):
        dice_roll = self.turn_options(True, dice_roll)
        input()
        self.advance(sum(dice_roll))

        square = files.squares[self.location]
        print(f"New square:\n" f"{self.location} - {square.NAME}")
        if square.SQUARE_TYPE in ("utility", "chance"):
            square.landing(self, sum(dice_roll))
        else:
            square.landing(self)

        self.turn_options(False)

    def turn_options(self, turn_start, dice_roll=(0, 0)) -> tuple[int, int]:
        if dice_roll != (0, 0):
            return dice_roll
        while True:
            print()
            has_properties = any(
                [bool(property_type) for property_type in self.properties.values()]
            )
            jail_cell = jail.jailed_list[self.INDEX]
            options = ["v"]

            if has_properties:
                print("(m) _M_ortgage")
                options.append("m")
            if self.balance or jail_cell["goojf"]:
                print("(t) _T_rade")
                options.append("t")
            if self.color_sets:
                print("(h) Buy/sell _h_ouses")
                options.append("h")
            print("(v) _V_iew stats")
            if turn_start:
                print("[d] Roll _d_ice")
            else:
                print("[e] _E_nd turn")

            option = input("Enter option:")
            if option:
                option = option[0].casefold()
            if option not in options and turn_start:
                return self.roll_dice()
            match option:
                case "m":
                    Mortgage(self)
                    print(self.balance)
                case "t":
                    Trade(self)
                case "h":
                    HouseBuySell(self)
                case "v":
                    stats.stat_options(self, player_data, files.squares)
                case _:
                    break

    def roll_dice(self) -> tuple[int, int]:
        if SKIP_DICE:
            return 0, 0

        input("\nRoll dice >")
        dice_roll = (randint(1, 6), randint(1, 6))
        print(f"1st: {dice_roll[0]} + 2nd: {dice_roll[1]} = {sum(dice_roll)}")

        self.doubles_roll(*dice_roll)
        return dice_roll

    def doubles_roll(self, roll_one, roll_two):
        if roll_one == roll_two and not DOUBLES_LOCK:
            print("Doubles!")
            self.doubles += 1
        else:
            self.doubles = 0

        if self.doubles >= 3:
            print("You rolled 3 consecutive doubles!")
            jail.jail_player(self)

    def advance(self, moves):
        new_location = self.location + moves
        if new_location == 40 and GO_BONUS:
            self.location = 0
            print("You landed directly on Go, receive $400")
            self.balance += 400
            return
        elif new_location >= 40:
            self.location = new_location % 40
            print("You passed Go, receive $200")
            self.balance += 200
            return
        self.location = new_location

    def start_options(self):
        if self.INDEX in START_LOCATION:
            self.location = START_LOCATION[self.INDEX]
        if self.INDEX in START_BALANCE:
            self.balance = START_BALANCE[self.INDEX]
        if self.INDEX in START_DOUBLES:
            self.doubles = START_DOUBLES[self.INDEX]
        if self.INDEX in START_PROPERTIES:
            self.properties = START_PROPERTIES[self.INDEX]
        self.color_sets = [
            color
            for color in files.PROPERTY_SETS["street"]
            if all(
                street in self.properties["street"]
                for street in files.PROPERTY_SETS["street"][color]
            )
        ]


class PlayerData:
    def __init__(self):
        self.player_index = 0
        self.player_list = {}

    def player_setup(self):
        player_count = 1
        if PLAYER_COUNT_OVERRIDE > 0:
            player_count = PLAYER_COUNT_OVERRIDE
        while not (SINGLE_PLAYER or PLAYER_COUNT_OVERRIDE):
            try:
                player_count = int(input("\nHow many players?(2-8):"))
                if not (player_count in range(2, 8 + 1)):
                    raise ValueError
                break
            except ValueError:
                print("Try again")
                continue

        self.player_list = {count: Player(count) for count in range(player_count)}

        for player in list(self.player_list.values()):
            jail.create_jail_space(player)

    def bankruptcy(self, player: Player):
        if not BANKRUPTCY_CHECK:
            return

        if player.balance < 0:
            self.player_list.pop(player.INDEX)

        if len(self.player_list) == 1 and not SINGLE_PLAYER:
            winning_player: Player = list(self.player_list.values())[0]
            print(f"Congrats! Player {winning_player.INDEX} won the game!")
            raise SystemExit

        if len(self.player_list) == 0:
            print("No one won the game!")
            raise SystemExit

    def turn_advance(self, player: Player):
        player_cell = jail.jailed_list[player.INDEX]
        players = self.player_list.keys()

        if player.doubles in range(1, 3) and not player_cell["jailed"]:
            return
        if self.player_index == max(players):
            self.player_index = min(players)
            return

        self.player_index += 1


player_data = PlayerData()


def welcome():
    try:
        with open("data/welcome.txt") as welcome_file:
            input(welcome_file.read())
    except FileNotFoundError:
        print("Could not find welcome.txt file")


def auction(square: Ownable) -> bool | tuple[Player, int]:
    print(
        "Input format: (player index), (amount of money)"
        '\nExample: 1, 200; Enter "end" to end auction\n'
    )
    if square.COST % 20 != 0:
        start_bid = 25
    else:
        start_bid = 20
    player_high, highest_bid = -1, start_bid
    print(f"Starting bid: ${start_bid}")
    while True:
        try:
            option = input("Enter bid: ")
            if option == "end":
                break
            option = option.split(", ")
            player: Player = player_data.player_list[int(option[0]) - 1]
            player_bid = int(option[1])

            if player.balance < player_bid:
                print("Not enough balance\n")
                continue
            if player_bid < highest_bid + start_bid:
                print(f"Must be higher than highest bid by at least ${start_bid}\n")
                continue

            player_high = player
            highest_bid = player_bid
            print(f"New bid: ${highest_bid} by player {player_high.INDEX+1}")

        except ValueError:
            print("Invalid input\n")
            continue
        except IndexError:
            print("Invalid player\n")
            continue

    if (player_high, highest_bid) == (-1, start_bid):
        print("No one got the property")
        return False

    print(f"Player {player_high.INDEX+1} got the property!")
    return player_high, highest_bid
