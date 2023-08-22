from os import path
from random import randint

if __name__ == "__main__":
    print(
        "Please run the TextopolyAgain.py file,\n"
        "This module is meant to be imported."
    )
    exit()

# Debugging constants
LOCATION_LOCK = False
DOUBLES_LOCK = False
START_LOCATION = 0
SKIP_DICE = False
SINGLE_PLAYER = False


class Square:
    def __init__(self, index: int, name: str, square_type: str):
        self.index = index
        self.name = name
        self.square_type = square_type


class Tax(Square):
    def __init__(self, index, name, square_type, cost):
        super().__init__(index, name, square_type)
        self.cost = cost

    def landing(self, player):
        print(f"You paid ${self.cost} in {self.name}")
        player.balance -= self.cost


class Corner(Square):
    def __init__(self, index, name, square_type):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        if player.location == 30:
            print("You landed on Go To Jail!")
            jail.jail_player(player)


class ComChest(Square):
    def __init__(self, index, name, square_type):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        input("Pick Card >")
        card = files.com_chest[randint(0, 13)]
        print(card["name"])
        match card["name"]:
            case "balance":
                player.balance += card.name
            case "GOOJF":
                jail.GOOJF_card(player, True)
            case "jail":
                jail.jail_player(player)
            case "go":
                player.location = 0
                player.balance += 200


class Chance(Square):
    def __init__(self, index, name, square_type):
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
            case "GOOJF":
                jail.GOOJF_card(player, True)
            case "jail":
                jail.jail_player(player)
            case "go":
                player.location = 0
                player.balance += 200


class Ownable(Square):
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

    def purchase(self, player):
        option = input(
            f"Would you like to purchase {self.name}" f"\nfor ${self.cost}? (y/[n]):"
        )
        if option == "y" and player.balance - self.cost >= 0:
            player.balance -= self.cost
            player.properties.append(player.location)
            files.squares[player.location].owner = player.index
            print(f"You have bought {self.name} for ${self.cost}")


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
        rent_levels: dict,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.color = color
        self.improvement_level = improvement_level
        self.IMPROVEMENT_COST = improvement_cost
        self.rent_levels = rent_levels

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owned_color_set = all(
            [square.owner == self.owner for square in files.color_sets[self.color]]
        )
        owner_player = player_data.player_list[self.owner]
        print(f"Player {self.owner+1} owns this street")

        rent = self.rent_levels[self.improvement_level]
        if self.improvement_level > 0:
            print(f"And this street has {self.improvement_level} houses\n")
        if owned_color_set and self.improvement_level == 0:
            print("And also owns the color set")
            rent *= 2
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
        rent_levels: dict,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.rent_levels = rent_levels

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owner_player = player_data.player_list[self.owner]
        owned_railroads = len(
            [
                railroad
                for railroad in (5, 15, 25, 35)
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
        if self.index == 12:
            self.other_util = 28
        else:
            self.other_util = 12

    def landing(self, player, dice_roll):
        owner_player: Player = player_data.player_list[self.owner]

        if self.owner is None:
            self.purchase(player)
            return

        print(f"Player {self.owner+1} owns this utility,")
        multiplier = 4
        if self.owner == files.squares[self.other_util].owner:
            print("And also owns the other utility,")
            multiplier = 10
        print(
            f"You'll pay {multiplier} times your dice roll ({dice_roll}) to player {self.owner+1}"
        )
        player.balance -= dice_roll * multiplier
        owner_player.balance += dice_roll * multiplier


class Card:
    def __init__(self, name: str, card_type: str, value: None | int, chance: bool):
        self.chance = chance
        self.name = name
        self.card_type = card_type
        self.value = value


class Files:
    def __init__(self):
        self.squares = {}
        self.com_chest = {}
        self.chance = {}
        self.color_sets = {}
        self.file_setup()

    def load_files(self):
        with (
            open("data/squares.txt", "r+") as squares_file,
            open("data/com_chest.txt", "r+") as com_chest_file,
            open("data/chance.txt", "r+") as chance_file,
            open("data/color_sets.txt", "r+") as color_sets_file,
        ):

            self.squares = eval(squares_file.read())
            self.com_chest = eval(com_chest_file.read())
            self.chance = eval(chance_file.read())
            self.color_sets = eval(color_sets_file.read())

    @staticmethod
    def files_exist():
        file_list = [
            "data/squares.txt",
            "data/com_chest.txt",
            "data/chance.txt",
            "data/color_sets.txt",
            "data/textopoly.py",
            "TextopolyAgain.py",
        ]

        for file in file_list:
            if not path.isfile(file):
                print(f'File "{file}" is missing\nPlease download all files')
                exit()

    @staticmethod
    def square_dto(square):
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
                return square_obj
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
                return square_obj
            case "utility":
                square_obj = Utility(
                    square["index"],
                    square["name"],
                    square_type,
                    square["cost"],
                    None,
                    False,
                )
                return square_obj
            case "comChest":
                square_obj = ComChest(
                    square["index"],
                    square["name"],
                    square_type,
                )
                return square_obj
            case "chance":
                square_obj = Chance(
                    square["index"],
                    square["name"],
                    square_type,
                )
                return square_obj
            case "tax":
                square_obj = Tax(
                    square["index"], square["name"], square_type, square["cost"]
                )
                return square_obj
            case "corner":
                square_obj = Corner(
                    square["index"],
                    square["name"],
                    square_type,
                )
                return square_obj

    def dict_to_obj(self):
        new_squares = {}

        for index, square in list(self.squares.items()):
            square_obj = self.square_dto(square)
            new_squares.update({index: square_obj})

        self.squares = new_squares

    def file_setup(self):
        print("\nLoading files...")

        self.files_exist()
        self.load_files()
        self.dict_to_obj()

        print("Loaded successfully!")


class Jail:
    def __init__(self):
        self.jailed_list = {}

    def create_jail_space(self, player):
        self.jailed_list.update(
            {player.index: {"jailed": False, "GOOJF": False, "jail_turns": 0}}
        )

    def jail_player(self, player):
        player_cell = self.jailed_list[player.index]

        player_cell.update({"jailed": True})
        player.location = 10
        print("You have been sent to Jail")

    def GOOJF_card(self, player, get_card):
        player_cell = self.jailed_list[player.index]

        if not get_card:
            player_cell.update({"GOOJF": True})
            return

        player_cell.update({"GOOJF": True})
        print("You received the Get Out Of Jail Free card")

    def get_out_of_jail(self, player, double_roll=(0, 0)):
        player_cell = self.jailed_list[player.index]

        player_cell.update({"jailed": False})
        player.normal_turn(*double_roll)

    def jail_options(self, player):
        player_cell = self.jailed_list[player.index]

        print("You're in Jail\n")
        if player_cell["jail_turns"] <= 3:
            print("(r) _R_oll doubles")
        if player_cell["GOOJF"]:
            print("(f) Use Get Out Of Jail _F_ree card")
        print("([b]) Pay $50 _b_ail")

        option = input("Enter choice:")
        self.jail_escape(option, player, player_cell)

    def jail_escape(self, option, player, player_cell):
        if option == "r" and player_cell.in_jail_turns <= 3:
            input("\nRoll dice >")
            roll_one, roll_two = (randint(1, 6), randint(1, 6))
            print(f"1st: {roll_one} + 2nd: {roll_two} = {roll_one + roll_two}")

            if roll_one == roll_two:
                print("You rolled a double!\nYou've been released")
                self.get_out_of_jail(player, (roll_one, roll_two))
                return

            print("You didn't roll a double\nYou'll remain in Jail")
            player_cell.in_jail_turns += 1
            return

        elif option == "f" and player_cell.jail_out_free:
            print("You've used your Get Out Of Jail Free Card")
            self.GOOJF_card(player, False)
            self.get_out_of_jail(player)
            return

        player.balance -= 50
        print("You've paid $50 bail to get out of jail")
        self.get_out_of_jail(player)
        return


files = Files()
jail = Jail()


class Player:
    def __init__(
        self,
        index: int,
    ):
        self.index = index
        self.location = START_LOCATION
        self.balance = 1500
        self.properties = []
        self.doubles = 0

    def normal_turn(self, roll_one=0, roll_two=0):
        if (roll_one, roll_two) == (0, 0) and not SKIP_DICE:
            input("\nRoll dice >")
            roll_one, roll_two = (randint(1, 6), randint(1, 6))
            print(f"1st: {roll_one}, 2nd: {roll_two} = " f"{roll_one + roll_two}")

            self.doubles_count(roll_one, roll_two)

        input()
        self.advance(roll_one + roll_two)
        square = files.squares[self.location]
        print(f"New square:\n{self.location} - " f"{square.name}")

        if square.square_type == "utility":
            square.landing(self, roll_one + roll_two)
        else:
            square.landing(self)

        input("\nEnd turn...")

    def advance(self, moves):
        new_location = self.location + moves
        if new_location >= 40:
            self.location = new_location % 40
            print("You passed Go, receive $200")
            self.balance += 200
            return
        self.location = new_location

    def doubles_count(self, roll_one, roll_two):
        if roll_one == roll_two and not DOUBLES_LOCK:
            print("Doubles!")
            self.doubles += 1
        else:
            self.doubles = 0

        if self.doubles >= 3:
            print("You rolled 3 consecutive doubles!")
            jail.jail_player(self)


class PlayerData:
    def __init__(self):
        self.player_index = 0
        self.player_list = {}
        self.remaining_players = []

        self.player_setup()

    def player_setup(self):
        player_count = 1
        while not SINGLE_PLAYER:
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
        if player.balance < 0:
            self.player_list.pop(player.index)
            return
        if len(self.player_list) == 1:
            winning_player: Player = list(self.player_list.values())[0]
            print(f"Congrats! Player {winning_player.index} won the game!")
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
    input(
        "\nWelcome to Textopoly!\n"
        "\nNotes:"
        "\n- Press enter to advance prompts."
        "\n- If you don't choose a valid option while in jail,"
        "\n  You'll automatically pay $50 bail."
    )


def print_stats(player, square):
    print(
        f"\nPlayer {player.index + 1}'s turn"
        f"\nCurrent balance: {player.balance}"
        f"\nCurrent square:\n{player.location} - {square.name}"
    )
