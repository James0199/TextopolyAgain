try:
    from abc import ABC, abstractmethod
    from random import randint
    from modules.config import *
except ModuleNotFoundError:
    print("Please download all files.")
    exit()
except ImportError:
    print(
        "Couldn't load a module,\n"
        "Make sure to use Python 3.10+\n\n"
        "If the problem persists,\n"
        "Submit an issue on this project's Github "
    )
    exit()


if __name__ == "__main__" and MODULE_GUARD:
    print(
        "Please run the TextopolyAgain.py file,\n"
        "This module is meant to be imported."
    )
    exit()

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
                player.balance += card.name
            case "goojf":
                jail.goojf_card(player, True)
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
        match card["card_type"]:
            case "set_loc_property":
                player.location = card.value
                if player.location > card.value:
                    print("You passed Go")
                    player.balance += 200
            case "balance":
                player.balance += card.value
            case "move":
                player.location -= card.value
            case "goojf":
                jail.goojf_card(player, True)
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
            f"Would you like to purchase {self.name}\nfor ${self.cost}? (y/[n]):"
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
            f"Would you like to purchase {self.name}" f"\nfor ${self.cost}? (y/[n]):"
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
            f"Would you like to purchase {self.name}" f"\nfor ${self.cost}? (y/[n]):"
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
        self.squares = {}
        self.com_chest = {}
        self.chance = {}
        self.property_sets = {}
        self.file_setup()

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
                exit()

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

    def dict_to_obj(self):
        new_squares = {}

        for index, square in list(self.squares.items()):
            square_obj = self.square_dto(square)
            new_squares.update({index: square_obj})

        self.squares = new_squares

    def file_setup(self):
        self.load_files()
        self.dict_to_obj()


class Jail:
    def __init__(self):
        self.jailed_list: dict[int, dict[str, bool | int]] = {}

    def create_jail_space(self, player):
        self.jailed_list.update(
            {
                player.index: {
                    "jailed": START_JAILED,
                    "goojf": START_GOOJF,
                    "jail_turns": 0,
                }
            }
        )

    def jail_player(self, player):
        player_cell = self.jailed_list[player.index]

        player_cell["jailed"] = True
        player.location = 10
        print("You have been sent to Jail")

    def goojf_card(self, player, get_card):
        player_cell = self.jailed_list[player.index]

        if not get_card:
            player_cell["goojf"] -= 1
            return

        player_cell["goojf"] += 1
        print("You received the Get Out Of Jail Free card")

    def get_out_of_jail(self, player, double_roll=(0, 0)):
        player_cell = self.jailed_list[player.index]

        player_cell["jailed"] = False
        player.normal_turn(double_roll)

    def jail_options(self, player):
        player_cell = self.jailed_list[player.index]

        print("You're in Jail\n")
        if player_cell["jail_turns"] <= 3:
            print("(r) _R_oll doubles")
        if player_cell["goojf"] > 0:
            print("(f) Use Get Out Of Jail _F_ree card")
        print("([b]) Pay $50 _b_ail")

        option = input("Enter choice:")
        if option == "r" and player_cell["jail_turns"] <= 3:
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

        elif option == "f" and player_cell["goojf"] > 0:
            print("You've used your Get Out Of Jail Free Card")
            self.goojf_card(player, False)
            self.get_out_of_jail(player)
            return

        player.balance -= 50
        print("You've paid $50 bail to get out of jail")
        self.get_out_of_jail(player)
        return


files = Files()
jail = Jail()
print("Loaded successfully!")


class Player:
    def __init__(
        self,
        index,
    ):
        self.index: int = index
        self.location: int = START_LOCATION
        self.balance: int = START_BALANCE
        self.properties: dict[str, list[int]] = {
            "street": [],
            "railroad": [],
            "utility": [],
        }
        self.color_sets: list[str] = []
        self.doubles: int = START_DOUBLES
        if START_PROPERTIES:
            self.properties = START_PROPERTIES[self.index]

    def normal_turn(self, dice_roll=(0, 0)):
        self.turn_options(dice_roll, True)

        input()
        self.advance(sum(dice_roll))
        square = files.squares[self.location]
        print(f"New square:\n" f"{self.location} - " f"{square.name}")

        self.landing(square, dice_roll)

        input("\nEnd turn...")

    def turn_options(self, dice_roll, turn_start):
        if dice_roll != (0, 0):
            return dice_roll
        while True:
            print()
            has_properties = all(
                [bool(properties) for properties in self.properties.values()]
            )
            if has_properties:
                print("(m) _M_ortgage\n" "(t) _T_rade")
            if self.color_sets:
                print("(h) Buy/sell _h_ouses")
            if turn_start:
                print("([d]) Roll _d_ice")
            else:
                print("([e]) _E_nd turn")

            option = input("Enter option:")
            if option == "m" and has_properties:
                continue
            elif option == "t" and has_properties:
                continue
            elif option == "h" and self.color_sets:
                continue
            if turn_start:
                return self.roll_dice()
            break

    def roll_dice(self):
        if SKIP_DICE:
            return 0, 0

        input("\nRoll dice >")
        dice_roll = (randint(1, 6), randint(1, 6))
        print(f"1st: {dice_roll[0]}, 2nd: {dice_roll[1]} = {sum(dice_roll)}")

        self.doubles_roll(*dice_roll)
        return dice_roll

    def landing(self, square, dice_roll):
        if square.square_type == "utility":
            square.landing(self, sum(dice_roll))
            return
        square.landing(self)

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


class PlayerData:
    def __init__(self):
        self.player_index = 0
        self.player_list = {}
        self.remaining_players = []

        self.player_setup()

    def player_setup(self):
        player_count = 1
        if PLAYER_COUNT_OVERRIDE > 0:
            player_count = PLAYER_COUNT_OVERRIDE
        while not SINGLE_PLAYER and not PLAYER_COUNT_OVERRIDE:
            player_count = input("\nHow many players?(2-8):")
            if not player_count.isdigit():
                print("Try again")
                continue
            if not int(player_count) in range(2, 8 + 1):
                print("Try again")
                continue
            player_count = int(player_count)
            break

        for count in range(0, player_count):
            self.player_list.update({count: Player(count)})
        self.remaining_players = [i for i in range(0, player_count)]

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
            exit()

        if len(self.player_list) == 0:
            print("No one won the game!")
            exit()

    def turn_advance(self, player: Player):
        player_cell = jail.jailed_list[player.index]
        players = list(self.player_list.keys())

        if 1 < player.doubles <= 3 and not player_cell["jailed"] or LOCATION_LOCK:
            return
        if max(players) == self.player_index:
            self.player_index = min(players)
            return

        self.player_index += 1


player_data = PlayerData()


def welcome():
    if not (WELCOME_MESSAGE or LOAD_FILES):
        return
    try:
        with open("data/welcome.txt") as welcome_file:
            print(welcome_file.read())
            input()
    except FileNotFoundError:
        print("Could not find welcome.txt file")


def print_stats(player, square):
    print(
        f"\nPlayer {player.index+1}'s turn"
        f"\nCurrent balance: {player.balance}"
        f"\n{square.index} - {square.name}"
    )
