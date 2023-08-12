from os import path
from random import randint

if __name__ == "__main__":
    print(
        "Please run the TextopolyAgain.py file,\n"
        "This module is meant to be imported."
    )
    exit()


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
        if player.location == 0:
            print("You landed on Go, receive $200")
            player.balance += 200
        elif player.location == 30:
            print("You landed on Go To Jail!")
            jail.jail_player(player)


class ComChest(Square):
    def __init__(self, index, name, square_type):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        input("Pick Card >")
        card: ComChestCard = files.com_chest[randint(0, 14)]
        print(card.name)
        if card.name == "balance":
            player.balance += card.name
        elif card.card_type == "GOOJF":
            jail.GOOJF_card(player, True)
        elif card.card_type == "jail":
            jail.jail_player(player)
        elif card.card_type == "go":
            player.location = 0
            player.balance += 200


class Chance(Square):
    def __init__(self, index, name, square_type):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        input("Pick Card >")
        card: ChanceCard = files.chance[randint(0, 13)]
        print(card.name)
        if card.card_type == "set_loc_property":
            player.location = card.value
            if player.location > card.value:
                print("You passed Go")
                player.balance += 200
        elif card.card_type == "balance":
            player.balance += card.value
        elif card.card_type == "move":
            player.location -= card.value
        elif card.card_type == "GOOJF":
            jail.GOOJF_card(player, True)
        elif card.card_type == "jail":
            jail.jail_player(player)
        elif card.card_type == "go":
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
        pass


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
        pass


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

    def landing(self, player, dice_rolls):
        pass


class Cards:
    def __init__(self, name: str, card_type: str, value: None | int):
        self.name = name
        self.card_type = card_type
        self.value = value


class ChanceCard(Cards):
    def __init__(self, name: str, card_type: str, value: None | int):
        super().__init__(name, card_type, value)


class ComChestCard(Cards):
    def __init__(self, name: str, card_type: str, value: None | int):
        super().__init__(name, card_type, value)


class Files:
    def __init__(self):
        self.squares = {}
        self.com_chest = {}
        self.chance = {}
        self.file_setup()

    def load_files(self):
        with (
            open("data/squares.py", "r+") as squares_file,
            open("data/com_chest.py", "r+") as com_chest_file,
            open("data/chance.py", "r+") as chance_file,
        ):

            self.squares = eval(squares_file.read())
            self.com_chest = eval(com_chest_file.read())
            self.chance = eval(chance_file.read())

    @staticmethod
    def files_exist():
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
                exit()

    @staticmethod
    def square_dto(square):
        square_type = square["type"]
        if square_type == "street":
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
        elif square_type == "railroad":
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
        elif square_type == "utility":
            square_obj = Utility(
                square["index"],
                square["name"],
                square_type,
                square["cost"],
                None,
                False,
            )
            return square_obj
        elif square_type == "comChest":
            square_obj = ComChest(
                square["index"],
                square["name"],
                square_type,
            )
            return square_obj
        elif square_type == "chance":
            square_obj = Chance(
                square["index"],
                square["name"],
                square_type,
            )
            return square_obj
        elif square_type == "tax":
            square_obj = Tax(
                square["index"], square["name"], square_type, square["cost"]
            )
            return square_obj
        elif square_type == "corner":
            square_obj = Corner(
                square["index"],
                square["name"],
                square_type,
            )
            return square_obj

    def file_setup(self):
        print("\nLoading files...")

        self.files_exist()
        self.load_files()
        self.dict_to_obj()

        print("Loaded successfully!")

    def dict_to_obj(self):
        new_squares = {}
        new_com_chest = {}
        new_chance = {}

        for index, square in list(self.squares.items()):
            square_obj = self.square_dto(square)
            new_squares.update({index: square_obj})

        for index, card in list(self.com_chest.items()):
            card_obj = ComChestCard(card["name"], card["type"], card["value"])
            new_com_chest.update({index: card_obj})

        for index, card in list(self.chance.items()):
            card_obj = ChanceCard(card["name"], card["type"], card["value"])
            new_chance.update({index: card_obj})

        self.squares = new_squares
        self.com_chest = new_com_chest
        self.chance = new_chance


class Jail:
    def __init__(self):
        self.jailed_list = {}

    def create_jail_space(self, player):
        if player.index not in self.jailed_list:
            self.jailed_list.update(
                {player.index: {"jailed": False, "GOOJF": False, "jail_turns": 0}}
            )

    def jail_player(self, player):
        self.create_jail_space(player)
        self.jailed_list[player.index]["jailed"] = True
        player.location = 10
        print("You have been sent to Jail")

    def GOOJF_card(self, player, get_card):
        if get_card:
            self.create_jail_space(player)
            self.jailed_list[player.index]["GOOJF"] = True
            print("You received the Get Out Of Jail Free card")
            return
        self.jailed_list[player.index]["GOOJF"] = False

    def get_out_of_jail(self, player, double_roll=(0, 0)):
        roll_one, roll_two = double_roll
        self.jailed_list[player.index]["jailed"] = False
        player.normal_turn(roll_one, roll_two)


files = Files()
jail = Jail()


class Player:
    def __init__(
        self,
        index: int,
    ):
        self.index = index
        self.location = 0
        self.balance = 1500
        self.properties = []
        self.jail = False
        self.jail_out_free = False
        self.in_jail_turns = 0
        self.doubles = 0

    def normal_turn(self, roll_one=0, roll_two=0):
        if (roll_one, roll_two) == (0, 0):
            input("\nRoll dice >")
            roll_one, roll_two = (randint(1, 6), randint(1, 6))
            print(f"1st: {roll_one}, 2nd: {roll_two} = " f"{roll_one + roll_two}")

            self.doubles_count(roll_one, roll_two)

        input()
        self.advance(roll_one + roll_two)
        current_square = files.squares[self.location]
        print(f"New square:\n{self.location} - " f"{current_square.name}")

        self.landing_square(current_square, (roll_one, roll_two))

        input("\nEnter to Continue...")

    def landing_square(self, current_square, dice_rolls):
        if current_square.square_type == "utility":
            current_square.landing(self, dice_rolls)
            return
        current_square.landing(self)

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
                jail.get_out_of_jail(self, (roll_one, roll_two))
                return "You rolled a double!\nYou've been released"

            self.in_jail_turns += 1
            return "You didn't roll a double\nYou'll remain in Jail"

        elif option == "f" and self.jail_out_free:
            jail.get_out_of_jail(self)
            jail.GOOJF_card(self, False)
            return "You've used your Get Out Of Jail Free Card"

        self.balance -= 50
        jail.get_out_of_jail(self)
        return "You've paid $50 bail to get out of jail"

    def print_stats(self, current_square):
        print(
            f"\nPlayer {self.index + 1}'s turn"
            f"\nCurrent balance: {self.balance}"
            f"\nCurrent square:\n{self.location} - {current_square.name}"
        )

    def advance(self, moves):
        new_location = self.location + moves
        if new_location == 40:
            self.location = 0
            return
        if new_location > 40:
            self.location = new_location % 40
            print("You passed Go, receive $200")
            self.balance += 200
            return
        self.location = new_location

    def doubles_count(self, roll_one, roll_two):
        if roll_one == roll_two:
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

        for count in range(0, player_count):
            self.player_list.update({count: Player(count)})

        self.remaining_players = [i for i in range(0, player_count)]

    def bankruptcy(self, player: Player):
        if player.balance < 0:
            self.player_list.pop(player.index)
            return
        if len(self.player_list) == 1:
            winning_player: Player = list(self.player_list.values())[0]
            print(f"Congrats! Player {winning_player.index} won the game!")
            exit()

    def turn_advance(self, player: Player):
        if player.doubles in range(1, 3 + 1) and not player.jail:
            return
        if max(list(self.player_list.keys())) == self.player_index:
            self.player_index = min(list(self.player_list.keys()))
            return
        self.player_index += 1


def welcome():
    input(
        "\nWelcome to Textopoly!\n"
        "\nNotes:"
        "\nPress enter to advance prompts."
        "\nIf you don't choose a valid option while in jail,"
        "\nYou'll automatically pay $50 bail."
    )
