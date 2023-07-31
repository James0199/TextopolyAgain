from os import path
from random import randint


class Player:
    def __init__(
        self,
        location: int,
        balance: int,
        properties: list,
        jail: bool,
        jail_out_free: bool,
        in_jail_turns: int,
        doubles: int,
    ):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.jail = jail
        self.jail_out_free = jail_out_free
        self.in_jail_turns = in_jail_turns
        self.doubles = doubles

    def normal_turn(self, jail_doubles, roll_one=0, roll_two=0):
        if not jail_doubles:
            roll_one, roll_two = dice_roll()
            print(f"1st: {roll_one}, 2nd: {roll_two} = " f"{roll_one + roll_two}")

            self.doubles_count(roll_one, roll_two)

        input()
        self.advance(roll_one + roll_two)
        current_square = squares[self.location]
        print(f"New square:\n{self.location} - " f"{current_square['name']}")

        self.landing_square(current_square)

    def landing_square(self, current_square):
        square_type = current_square["type"]
        if square_type == "street":
            pass
        elif square_type == "railroad":
            pass
        elif square_type == "utility":
            pass
        elif square_type == "comChest":
            self.com_chest_card()
        elif square_type == "chance":
            self.chance_card()
        elif square_type == "tax":
            pass

    def com_chest_card(self):
        input("Pick Card >")
        card = com_chest[randint(0, 14)]
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
        card = chance[randint(0, 14)]
        card = com_chest[randint(0, 14)]
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

    def go_to_jail(self):
        self.jail = True
        self.location = 10
        print("You have been sent to Jail")

    def jail_conditions(self):
        if self.location == 30:
            print("\nYou landed on Go to Jail!")
            self.go_to_jail()
        elif self.doubles >= 3:
            print("\nYou rolled 3 consecutive doubles!")
            self.go_to_jail()

    def in_jail(self):
        print("You're in Jail\n")
        if self.in_jail_turns <= 3:
            print("(r) _R_oll doubles")
        if self.jail_out_free:
            print("(f) Use Get Out Of Jail _F_ree card")
        print("([b]) Pay $50 _b_ail")
        option = input("Enter choice:")

        self.jail_options(option)

    def jail_options(self, option):
        if option == "r" and self.in_jail_turns <= 3:
            roll_one, roll_two = dice_roll()
            print(f"1st roll: {roll_one}, 2nd roll: {roll_two}")

            if roll_one == roll_two:
                print("You rolled a double!" "\nYou've been released")
                self.get_out_of_jail((False, roll_one, roll_two))
                return
            print("You didn't roll a double" "\nYou'll remain in Jail")
            return

        elif option == "f" and self.jail_out_free:
            print("You have used your Get Out Of Jail Free Card")
            self.get_out_of_jail(False)
            return

        print("You've paid $50 bail to get out of jail")
        self.balance -= 50
        self.get_out_of_jail((False))
        return

    def get_out_of_jail(self, double_roll=(False, 0, 0)):
        jail_doubles, roll_one, roll_two = double_roll
        self.jail = False
        self.normal_turn(jail_doubles, roll_one, roll_two)

    def print_stats(self, player_num, current_square):
        print(
            f"\nPlayer {player_num}'s turn"
            f"\nCurrent balance: {self.balance}"
            f"\nCurrent square:\n{self.location} - {current_square['name']}"
        )

    def advance(self, moves):
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
    for count in range(1, player_count + 1):
        player_list.update({count: Player(0, 1500, [], False, False, 0, 0)})

    # Player_num, players, remaining_players
    return 1, player_list, [i for i in range(1, player_count + 1)]


def file_setup():
    file_list = [
        "data/squares.py",
        "data/com_chest.py",
        "data/chance.py",
        "TextopolyAgain.py",
    ]

    for file in file_list:
        if not path.isfile(file):
            print(f'File "{file}" is missing' "\nPlease download all files")

    global squares, com_chest, chance

    with open("data/squares.py", "r+") as squares_file, open(
        "data/com_chest", "r+"
    ) as com_chest_file, open("data/chance.py", "r+") as chance_file:

        squares = eval(squares_file.read())
        com_chest_list, com_chest = eval(com_chest_file.read())
        chance_list, chance = eval(chance_file.read())


def turnAdvance(player_num, remaining_players):
    if player_num == max(remaining_players):
        return min(remaining_players)

    return remaining_players[remaining_players.index(player_num) + 1]


def dice_roll():
    input("\nRoll dice >")
    roll_one, roll_two = (randint(1, 6), randint(1, 6))

    return roll_one, roll_two


def welcome():
    input(
        "\nWelcome to Textopoly!\n"
        "\nNotes:"
        "\nPress enter to advance prompts."
        "\nIf you don't choose a valid option while in jail,"
        "\nYou'll automatically pay $50 bail."
    )
