from os import path
from random import randint


class Files:
    def __init__(self):
        self.squares = {}
        self.com_chest = {}
        self.chance = {}
        self.file_setup()

    def file_setup(self):
        print("\nLoading files...")
        file_list = [
            "data/squares.py",
            "data/com_chest.py",
            "data/chance.py",
            "data/textopoly.py",
            "TextopolyAgain.py",
        ]

        for file in file_list:
            if not path.isfile(file):
                print(f'File "{file}" is missing\nPlease download all files')
                return

        with (
            open("data/squares.py", "r+") as squares_file,
            open("data/com_chest.py", "r+") as com_chest_file,
            open("data/chance.py", "r+") as chance_file,
        ):

            self.squares = eval(squares_file.read())
            self.com_chest = eval(com_chest_file.read())
            self.chance = eval(chance_file.read())

        print("Loaded successfully!")


files = Files()


class Player:
    def __init__(
        self,
        index: int,
        location: int,
        balance: int,
        properties: list,
        jail: bool,
        jail_out_free: bool,
        in_jail_turns: int,
        doubles: int,
    ):
        self.index = index
        self.location = location
        self.balance = balance
        self.properties = properties
        self.jail = jail
        self.jail_out_free = jail_out_free
        self.in_jail_turns = in_jail_turns
        self.doubles = doubles

    def normal_turn(self, jail_doubles=False, roll_one=0, roll_two=0):
        if not jail_doubles:
            input("\nRoll dice >")
            roll_one, roll_two = (randint(1, 6), randint(1, 6))
            print(f"1st: {roll_one}, 2nd: {roll_two} = " f"{roll_one + roll_two}")

            self.doubles_count(roll_one, roll_two)

        input()
        self.advance(roll_one + roll_two)
        current_square = files.squares[self.location]
        print(f"New square:\n{self.location} - " f"{current_square['name']}")

        self.landing_square(current_square, (roll_one, roll_two))

        input("\nEnter to Continue...")

    def landing_square(self, current_square, dice_rolls):
        square_type = current_square["type"]
        if square_type == "street":
            self.street_property(current_square)
        elif square_type == "railroad":
            self.railroad_property(current_square)
        elif square_type == "utility":
            self.utility_property(current_square, dice_rolls)
        elif square_type == "comChest":
            self.com_chest_card()
        elif square_type == "chance":
            self.chance_card()
        elif square_type == "tax":
            self.tax_square(current_square)

    def street_property(self, current_square):
        pass

    def railroad_property(self, current_square):
        pass

    def utility_property(self, current_square, dice_rolls):
        roll_one, roll_two = dice_rolls
        if current_square["owner"] == "none":
            self.purchase(current_square)
            # This one looks real crappy
            if (
                files.squares[28]["owner"] == self.index
                and files.squares[12] == self.index
            ):
                electric, water = files.squares[12], files.squares[28]
                electric.update({"improvementLevel": 2})
                electric.update({"owner": self.index})
                water.update({"improvementLevel": 2})
                water.update({"owner": self.index})
                files.squares.update({12: electric})
                files.squares.update({28: water})
                return
            current_square.update({"improvementLevel": 1})
            files.squares.update({current_square["index"]: current_square})

    def com_chest_card(self):
        input("Pick Card >")
        card = files.com_chest[randint(0, 13)]
        print(card["name"])
        if card["type"] == "balance":
            self.balance += card["value"]
        elif card["type"] == "GOOJF":
            self.jail_out_free = True
        elif card["type"] == "jail":
            self.go_to_jail()
        elif card["type"] == "go":
            self.location = 0
            self.balance += 200

    def chance_card(self):
        input("Pick Card >")
        card = files.chance[randint(0, 12)]
        print(card["name"])
        if card["type"] == "set_loc_property":
            self.location = card["value"]
            if self.location > card["value"]:
                print("You passed Go")
                self.balance += 200
        elif card["type"] == "balance":
            self.balance += card["value"]
        elif card["type"] == "move":
            self.location -= card["value"]
        elif card["type"] == "GOOJF":
            self.jail_out_free = True
        elif card["type"] == "jail":
            self.go_to_jail()
        elif card["type"] == "go":
            self.location = 0
            self.balance += 200

    def corner_square(self):
        if self.location == 0:
            print("You landed on Go, recieve $200")
            self.balance += 200
        elif self.location == 30:
            print("You landed on Go To Jail!")
            self.go_to_jail()

    def tax_square(self, current_square):
        print(f"You paid ${current_square['cost']} in {current_square['name']}")
        self.balance -= current_square["cost"]

    def purchase(self, current_square: dict):
        option = input(
            f"Would you like to purchase {current_square['name']}"
            f"\nfor ${current_square['cost']}? (y/[n]):"
        )
        if option == "y" and self.balance - current_square["cost"] >= 0:
            self.balance -= current_square["cost"]
            self.properties.append(self.location)
            current_square.update({"owner": self.index})
            files.squares.update({current_square["index"]: current_square})
            print(
                f"You have bought {current_square['name']} for ${current_square['cost']}"
            )

    def go_to_jail(self):
        self.jail = True
        self.location = 10
        print("You have been sent to Jail")

    def in_jail(self):
        print("You're in Jail\n")
        if self.in_jail_turns <= 3:
            print("(r) _R_oll doubles")
        if self.jail_out_free:
            print("(f) Use Get Out Of Jail _F_ree card")
        print("([b]) Pay $50 _b_ail")
        option = input("Enter choice:")

        print(self.jail_options(option))

    def jail_options(self, option):
        if option == "r" and self.in_jail_turns <= 3:
            input("\nRoll dice >")
            roll_one, roll_two = (randint(1, 6), randint(1, 6))
            print(f"1st roll: {roll_one}, 2nd roll: {roll_two}")

            if roll_one == roll_two:
                self.get_out_of_jail((True, roll_one, roll_two))
                return "You rolled a double!" "\nYou've been released"

            return "You didn't roll a double" "\nYou'll remain in Jail"

        elif option == "f" and self.jail_out_free:
            self.get_out_of_jail()
            return "You have used your Get Out Of Jail Free Card"

        self.balance -= 50
        self.get_out_of_jail()
        return "You've paid $50 bail to get out of jail"

    def get_out_of_jail(self, double_roll=(False, 0, 0)):
        jail_doubles, roll_one, roll_two = double_roll
        self.jail = False
        self.normal_turn(jail_doubles, roll_one, roll_two)

    def print_stats(self, current_square):
        print(
            f"\nPlayer {self.index + 1}'s turn"
            f"\nCurrent balance: {self.balance}"
            f"\nCurrent square:\n{self.location} - {current_square['name']}"
        )

    def advance(self, moves):
        if self.location + moves == 40:
            self.location = 0
            return
        if self.location + moves > 39:
            self.location = (self.location + moves) - 40
            print("You passed Go, recieve $200")
            self.balance += 200
            return
        self.location += moves

    def doubles_count(self, roll_one, roll_two):
        if roll_one == roll_two:
            print("Doubles!")
            self.doubles += 1
        else:
            self.doubles = 0
        if self.doubles >= 3:
            print("You rolled 3 consecutive doubles!")
            self.go_to_jail()


def player_setup():
    while True:
        player_count = input("\nHow many players?(2-8):")
        if not player_count.isdigit():
            print("Try again")
            continue
        if not int(player_count) in range(2, 8 + 1):
            print("Try again")
            continue
        player_count = int(player_count)
        break

    player_list = {}
    for count in range(0, player_count):
        player_list.update({count: Player(count, 0, 1500, [], False, False, 0, 0)})

    # Player_num, players, remaining_players
    return 0, player_list, [i for i in range(0, player_count)]


def turn_advance(player_index, player_list, current_player):
    if 0 < current_player.doubles < 3 and not current_player.jail:
        return player_index
    if max(list(player_list.keys())) == player_index:
        return min(list(player_list.keys()))
    return player_index + 1


def update_squares_info(index, key, value):
    updated_square: dict = files.squares[index]
    updated_square.update({key: value})
    files.squares.update(updated_square)


def welcome():
    input(
        "\nWelcome to Textopoly!\n"
        "\nNotes:"
        "\nPress enter to advance prompts."
        "\nIf you don't choose a valid option while in jail,"
        "\nYou'll automatically pay $50 bail."
    )
