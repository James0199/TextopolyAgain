try:
    from abc import ABC, abstractmethod
    from random import randint
    from modules.debug_cheats import *
except ModuleNotFoundError:
    print("Couldn't find a module,\nPlease download all files.")
    raise SystemExit
except ImportError:
    print(
        "Couldn't load a module,\n"
        "Make sure to use Python 3.10+\n\n"
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
        self.index = index
        self.name = name
        self.square_type = square_type


class Tax(Square):
    def __init__(self, index: int, name: str, square_type: str, cost: int):
        super().__init__(index, name, square_type)
        self.cost = cost

    def landing(self, player):
        print(f"You paid ${self.cost} in {self.name}")
        player.balance -= self.cost


class Corner(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        if SKIP_JAIL:
            return
        if player.location == 30:
            print("You landed on Go To Jail!")
            jail.jail_player(player)


class ComChest(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        input("Pick Card >")
        card = files.com_chest[randint(0, 13)]
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
    def landing(player):
        input("Pick Card >")
        card = files.chance[randint(0, 12)]
        print(card["name"])
        match card["type"]:
            case "set_loc_property":
                player.location = card["value"]
                if player.location > card["value"]:
                    print("You passed Go")
                    player.balance += 200

                square = files.squares[player.location]
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
        self.cost = cost
        self.owner = owner
        self.mortgaged = mortgaged

    @abstractmethod
    def purchase(self, player):
        ...


class Street(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        owner: None | int,
        mortgaged: bool,
        color: str,
        improvement_level: int,
        improvement_cost: int,
        rent_levels: dict[int, int],
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.color = color
        self.improvement_level = improvement_level
        self.IMPROVEMENT_COST = improvement_cost
        self.rent_levels = rent_levels

    def purchase(self, player):
        option = input(
            f"\nWould you like to purchase {self.name}\nfor ${self.cost}? (y/[n]):"
        )
        if option == "y" and player.balance - self.cost >= 0:
            player.balance -= self.cost
            player.properties["street"].append(self.index)
            self.update_color_set(player)
            files.squares[player.location].owner = player.index
            print(f"You have bought {self.name} for ${self.cost}")

    def update_color_set(self, player):
        color_set = files.property_sets["street"][self.color]
        color_set_squares = [files.squares[square] for square in color_set]

        if all([street.owner == player.index for street in color_set_squares]):
            player.color_sets.append(self.color)
            print(f"Player {player.index} got the {self.color} color set!")

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owner_player = player_data.player_list[self.owner]
        print(f"Player {self.owner+1} owns this street")
        if owner_player is player:
            return

        rent = self.rent_levels[self.improvement_level]
        if self.improvement_level > 0:
            print(f"And this street has {self.improvement_level} houses\n")
        elif self.color in player.color_sets and self.improvement_level == 0:
            print("And also owns the color set")
            rent *= 2
        print(f"You'll pay ${rent} to player {owner_player.index+1}")
        player.balance -= rent
        owner_player.balance += rent


class Railroad(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        owner: None | int,
        mortgaged: bool,
        rent_levels: dict[int, int],
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.rent_levels = rent_levels

    def purchase(self, player):
        option = input(
            f"\nWould you like to purchase {self.name}" f"\nfor ${self.cost}? (y/[n]):"
        )
        if option == "y" and player.balance - self.cost >= 0:
            player.balance -= self.cost
            player.properties["railroad"].append(self.index)
            files.squares[player.location].owner = player.index
            print(f"You have bought {self.name} for ${self.cost}")

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owner_player = player_data.player_list[self.owner]
        owned_railroads = len(
            [
                railroad
                for railroad in files.property_sets["railroad"]
                if self.owner == files.squares[railroad].owner
            ]
        )
        rent = 25 * (2**owned_railroads)
        print(
            f"Player {self.owner+1} owns this railroad,\n"
            f"And owns {owned_railroads} railroads\n"
            f"You'll pay ${rent} to player {self.owner+1}"
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
        self.other_util = None

    def purchase(self, player):
        option = input(
            f"\nWould you like to purchase {self.name}\nfor ${self.cost}? (y/[n]):"
        )
        if option == "y" and player.balance - self.cost >= 0:
            player.balance -= self.cost
            player.properties["utility"].append(self.index)
            files.squares[player.location].owner = player.index
            print(f"You have bought {self.name} for ${self.cost}")

    def define_other_util(self):
        self.other_util = [
            files.squares[util]
            for util in files.property_sets["utility"]
            if util != self.index
        ][0]

    def landing(self, player, dice_roll):
        self.define_other_util()
        if self.owner is None:
            self.purchase(player)
            return

        owner_player: Player = player_data.player_list[self.owner]
        print(f"Player {self.owner+1} owns this utility,")
        multiplier = 4
        if self.owner == self.other_util.owner:
            print("And also owns the other utility,")
            multiplier = 10
        print(
            f"You'll pay {multiplier} times your dice roll ({dice_roll}) "
            f"to player {self.owner+1}"
        )
        player.balance -= dice_roll * multiplier
        owner_player.balance += dice_roll * multiplier


class Files:
    def __init__(self):
        self.com_chest = {}
        self.chance = {}
        self.property_sets = {}
        self.load_files()
        self.squares = {
            index: self.square_dto(square)
            for index, square in list(self.squares.items())
        }

    def load_files(self):
        if not LOAD_FILES:
            return
        try:
            with (
                open("data/squares.txt", "r+") as squares_file,
                open("data/com_chest.txt", "r+") as com_chest_file,
                open("data/chance.txt", "r+") as chance_file,
                open("data/property_sets.txt", "r+") as property_sets_file,
            ):
                self.squares = eval(squares_file.read())
                self.com_chest = eval(com_chest_file.read())
                self.chance = eval(chance_file.read())
                self.property_sets = eval(property_sets_file.read())
        except FileNotFoundError:
            if FILE_CHECK:
                print("Please download all files")
                raise SystemExit

    @staticmethod
    def square_dto(square) -> Square:
        square_type = square["type"]
        match square_type:
            case "street":
                square_obj = Street(
                    square["index"],
                    square["name"],
                    square_type,
                    square["cost"],
                    None,
                    False,
                    square["color"],
                    0,
                    square["IMPROVEMENT_COST"],
                    square["rent_levels"],
                )
            case "railroad":
                square_obj = Railroad(
                    square["index"],
                    square["name"],
                    square_type,
                    square["cost"],
                    None,
                    False,
                    square["rent_levels"],
                )
            case "utility":
                square_obj = Utility(
                    square["index"],
                    square["name"],
                    square_type,
                    square["cost"],
                    None,
                    False,
                )
            case "comChest":
                square_obj = ComChest(
                    square["index"],
                    square["name"],
                    square_type,
                )
            case "chance":
                square_obj = Chance(
                    square["index"],
                    square["name"],
                    square_type,
                )
            case "tax":
                square_obj = Tax(
                    square["index"],
                    square["name"],
                    square_type,
                    square["cost"],
                )
            case "corner":
                square_obj = Corner(
                    square["index"],
                    square["name"],
                    square_type,
                )
            case _:
                raise TypeError("Invalid square type")
        return square_obj


class Jail:
    def __init__(self):
        self.jailed_list: dict[int, dict[str, bool | int]] = {}

    def create_jail_space(self, player):
        self.jailed_list.update(
            {
                player.index: {
                    "jailed": False,
                    "goojf": 0,
                    "jail_turns": 0,
                }
            }
        )
        if any((START_JAILED, START_GOOJF)):
            self.start_options(player)

    def jail_player(self, player):
        player_cell = self.jailed_list[player.index]

        player_cell["jailed"] = True
        player.location = 10
        print("You have been sent to Jail")

    def goojf_card(self, player, amount):
        player_cell = self.jailed_list[player.index]

        if amount > 0:
            print(f"You've recieved {amount} goojf card(s)")
        elif amount < 0:
            print(f"You've lost/used {abs(amount)} goojf card(s)")

        player_cell["goojf"] += amount

    def get_out_of_jail(self, player, double_roll=(0, 0)):
        player_cell = self.jailed_list[player.index]

        player_cell["jailed"] = False
        player.normal_turn(double_roll)

    def jail_turn(self, player):
        player_cell = self.jailed_list[player.index]

        print("You're in Jail\n")
        options = []
        if player_cell["jail_turns"] <= 3:
            print("(r) _R_oll doubles")
            options.append("r")
        if player_cell["goojf"] > 0:
            print("(f) Use Get Out Of Jail _F_ree card")
            options.append("f")
        print("[b] Pay $50 _b_ail")

        option = input("Enter choice:")
        if option in options:
            option = option[0].casefold()
        match option:
            case "r":
                input("\nRoll dice >")
                roll_one, roll_two = (randint(1, 6), randint(1, 6))
                print(f"1st: {roll_one} + 2nd: {roll_two} = {roll_one + roll_two}")
                if roll_one == roll_two:
                    print("You rolled a double!\nYou've been released")
                    self.get_out_of_jail(player, (roll_one, roll_two))
                    return
                print("You didn't roll a double\nYou'll remain in Jail")
                player_cell["jail_turns"] += 1
                return
            case "f":
                print("You've used your Get Out Of Jail Free Card")
                self.goojf_card(player, -1)
                self.get_out_of_jail(player)
                return
            case _:
                player.balance -= 50
                print("You've paid $50 bail to get out of jail")
                self.get_out_of_jail(player)
                return

    def start_options(self, player):
        player_cell = self.jailed_list[player.index]
        if player.index in START_JAILED:
            player_cell["jailed"] = START_JAILED[player.index]
        if player.index in START_GOOJF:
            player_cell["goojf"] = START_GOOJF[player.index]


files = Files()
jail = Jail()


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
                    int(input("\nPlayer (number) you want to trade with:")) - 1
                )
                if (
                    self.receiver not in player_data.player_list
                    or SINGLE_PLAYER
                    or self.receiver == self.sender.index
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
        if jail.jailed_list[player.index]["goojf"]:
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
                    print(f"{i+1}. {street.name}")
            case "r":
                print("\nYou have these applicable railroad(s):")
                for i, railroad in enumerate(player.properties["railroad"]):
                    railroad: Railroad = files.squares[railroad]
                    print(f"{i+1}. {railroad.name}")
            case "u":
                if len(player.properties["utility"]) > 1:
                    print("\nYou have these applicable utilities:")
                else:
                    print("\nYou have this applicable utility:")
                for i, util in enumerate(player.properties["utility"]):
                    util: Utility = files.squares[util]
                    print(f"{i+1}. {util.name}")

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
            jail_cell = jail.jailed_list[self.sender.index]
        else:
            jail_cell = jail.jailed_list[self.receiver.index]

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
                print(f"- {files.squares[offered_property].name}")
        if offer["money"]:
            print(f"Money: {offer['money']}")
        if offer["goojf"]:
            print(f"GOOJF cards: {offer['goojf']}")

    @staticmethod
    def apply_trade(player, other, other_offer):
        player_goojf = jail.jailed_list[player.index]["goojf"]
        other_goojf = jail.jailed_list[other.index]["goojf"]

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
                property_.owner = player.index

        player.balance += other_offer["money"]
        other.balance -= other_offer["money"]
        player_goojf += other_offer["goojf"]
        other_goojf -= other_offer["goojf"]


class Mortgage:
    def __init__(self, player):
        self.player = player
        self.mortgage()

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
                self.player.balance += property_obj.cost
                print(self.player.balance, property_obj.cost)
            elif property_obj.mortgaged:
                unmortgage_cost = round(property_obj.cost * 1.1)
                if self.player.balance < unmortgage_cost:
                    print("Not enough balance")
                    continue
                property_obj.mortgaged = False
                print(f"{selected_type.capitalize()} unmortgaged.")
                self.player.balance -= round(property_obj.cost * 1.1)

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
                    print(f"{i+1}. {files.squares[owned_property].name}")

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
                    print("Invalid index")
                continue


class HouseBuySell:
    def __init__(self, player):
        self.player = player
        self.menu()

    def options(self, no_print=False) -> tuple[dict, list] | dict:
        applicable_streets = {"buy": [], "sell": []}
        color_sets: dict[str, list[Street]] = {
            color: [
                files.squares[street] for street in files.property_sets["street"][color]
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
                print(f"- {street.name}")
        if applicable_streets["sell"]:
            options.append("s")
            print("You can sell houses on these streets:")
            for street in applicable_streets["sell"]:
                print(f"- {street.name}")
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
            print(f"{i+1}. {street.name}")
        while True:
            street_index = input("Select street:")
            if street_index == "m":
                break
            try:
                street_index = int(street_index) - 1
                if street_index not in range(len(applicable_streets[action])):
                    raise ValueError
            except ValueError:
                print("Invalid index")
                continue
        if street_index == "m":
            return
        selected_street: Street = applicable_streets[action][street_index]
        if action == "buy":
            selected_street.improvement_level += 1
            self.player.balance -= selected_street.IMPROVEMENT_COST
            print(
                f"House bought on {selected_street.name} for "
                f"${selected_street.IMPROVEMENT_COST}"
            )
        else:
            selected_street.improvement_level -= 1
            self.player.balance += selected_street.IMPROVEMENT_COST // 2
            print(
                f"House sold on {selected_street.name} for "
                f"${selected_street.IMPROVEMENT_COST // 2}"
            )


print("Loaded successfully!")


def welcome():
    try:
        with open("data/welcome.txt") as welcome_file:
            input(welcome_file.read())
    except FileNotFoundError:
        print("Could not find welcome.txt file")


if WELCOME_MESSAGE and LOAD_FILES:
    welcome()


class Player:
    def __init__(self, index):
        self.index: int = index
        self.location: int = 0
        self.balance: int = 1500
        self.doubles: int = 0
        self.properties: dict[str, list[int]] = {
            "street": [],
            "railroad": [],
            "utility": [],
        }
        self.color_sets: list[str] = []
        if any(
            (
                START_BALANCE,
                START_LOCATION,
                START_DOUBLES,
                START_PROPERTIES,
                START_COLOR_SETS,
            )
        ):
            self.start_options()

    def normal_turn(self, dice_roll=(0, 0)):
        dice_roll = self.turn_options(True, dice_roll)
        input()
        self.advance(sum(dice_roll))

        square = files.squares[self.location]
        print(f"New square:\n" f"{self.location} - {square.name}")
        if square.square_type == "utility":
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
            jail_cell = jail.jailed_list[self.index]
            options = []

            if has_properties:
                print("(m) _M_ortgage")
                options.append("m")
            if self.balance or jail_cell["goojf"]:
                print("(t) _T_rade")
                options.append("t")
            if self.color_sets:
                print("(h) Buy/sell _h_ouses")
                options.append("h")
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
        if new_location >= 40:
            self.location = new_location % 40
            print("You passed Go, receive $200")
            self.balance += 200
            return
        self.location = new_location

    def start_options(self):
        if self.index in START_LOCATION:
            self.location = START_LOCATION[self.index]
        if self.index in START_BALANCE:
            self.balance = START_BALANCE[self.index]
        if self.index in START_DOUBLES:
            self.doubles = START_DOUBLES[self.index]
        if self.index in START_PROPERTIES:
            self.properties = START_PROPERTIES[self.index]
        if self.index in START_COLOR_SETS:
            self.color_sets = START_COLOR_SETS[self.index]


class PlayerData:
    def __init__(self):
        self.player_index = 0
        self.player_list = {}

        self.player_setup()

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
            self.player_list.pop(player.index)

        if len(self.player_list) == 1 and not SINGLE_PLAYER:
            winning_player: Player = list(self.player_list.values())[0]
            print(f"Congrats! Player {winning_player.index} won the game!")
            raise SystemExit

        if len(self.player_list) == 0:
            print("No one won the game!")
            raise SystemExit

    def turn_advance(self, player: Player):
        player_cell = jail.jailed_list[player.index]
        players = self.player_list.keys()

        if player.doubles in range(1, 3) and not player_cell["jailed"]:
            return
        if self.player_index == max(players):
            self.player_index = min(players)
            return

        self.player_index += 1


player_data = PlayerData()


def print_stats(player, square):
    print(
        f"\nPlayer {player.index+1}'s turn"
        f"\nCurrent balance: {player.balance}"
        f"\n{square.index} - {square.name}"
    )
