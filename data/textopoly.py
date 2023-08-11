from os import path
from random import randint


class Square:
    def __init__(self, index: int, name: str, square_type: str):
        self.index = index
        self.name = name
        self.square_type = square_type


class Tax(Square):
    def __init__(self, index, name, square_type, cost):
        super().__init__(index, name, square_type)
        self.cost = cost

    def landing(self, current_player):
        print(f"You paid ${self.cost} in {self.name}")
        current_player.balance -= self.cost


class Corner(Square):
    def __init__(self, index, name, square_type):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(current_player):
        if current_player.location == 0:
            print("You landed on Go, receive $200")
            current_player.balance += 200
        elif current_player.location == 30:
            print("You landed on Go To Jail!")
            current_player.go_to_jail()


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

    def purchase(self, current_player):
        option = input(
            f"Would you like to purchase {self.name}" f"\nfor ${self.cost}? (y/[n]):"
        )
        if option == "y" and current_player.balance - self.cost >= 0:
            current_player.balance -= self.cost
            current_player.properties.append(current_player.location)
            files.update_squares(self.index, "owner", current_player.index)
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

    def landing(self, current_player):
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

    def landing(self, current_player):
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

    def landing(self, current_player):
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


class ComChest(Square):
    def __init__(self, index, name, square_type):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(current_player):
        input("Pick Card >")
        card: ComChestCard = files.com_chest[randint(0, 14)]
        print(card.name)
        if card.name == "balance":
            current_player.balance += card.name
        elif card.card_type == "GOOJF":
            current_player.jail_out_free = True
        elif card.card_type == "jail":
            current_player.go_to_jail()
        elif card.card_type == "go":
            current_player.location = 0
            current_player.balance += 200


class Chance(Square):
    def __init__(self, index, name, square_type):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(current_player):
        input("Pick Card >")
        card: ChanceCard = files.chance[randint(0, 13)]
        print(card.name)
        if card.card_type == "set_loc_property":
            current_player.location = card.value
            if current_player.location > card.value:
                print("You passed Go")
                current_player.balance += 200
        elif card.card_type == "balance":
            current_player.balance += card.value
        elif card.card_type == "move":
            current_player.location -= card.value
        elif card.card_type == "GOOJF":
            current_player.jail_out_free = True
        elif card.card_type == "jail":
            current_player.go_to_jail()
        elif card.card_type == "go":
            current_player.location = 0
            current_player.balance += 200


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

    def update_squares(self, index, attr, value):
        updated_square = self.squares[index]
        setattr(updated_square, attr, value)
        self.squares.update({index: updated_square})


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
        print(f"New square:\n{self.location} - " f"{current_square.name}")

        self.landing_square(current_square, (roll_one, roll_two))

        input("\nEnter to Continue...")

    def landing_square(self, current_square, dice_rolls):
        square_type = current_square.square_type
        if square_type == "utility":
            current_square.landing(self, dice_rolls)
            return
        current_square.landing(self)

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
            f"\nCurrent square:\n{self.location} - {current_square.name}"
        )

    def advance(self, moves):
        if self.location + moves == 40:
            self.location = 0
            return
        if self.location + moves > 40:
            self.location %= 40
            print("You passed Go, receive $200")
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
            self.player_list.update(
                {count: Player(count, 0, 1500, [], False, False, 0, 0)}
            )

        self.remaining_players = [i for i in range(0, player_count)]

    def bankruptcy(self, current_player: Player):
        if current_player.balance < 0:
            self.player_list.pop(current_player.index)
            return
        if len(self.player_list) == 1:
            winning_player: Player = list(self.player_list.values())[0]
            print(f"Congrats! Player {winning_player.index} won the game!")
            exit()

    def turn_advance(self, current_player: Player):
        if current_player.doubles in range(1, 3 + 1) and not current_player.jail:
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
