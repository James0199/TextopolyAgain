from random import randint
from os import path

class Player:
    def __init__(self, location: int,
                 balance: int,
                 properties: list,
                 jail: bool,
                 jail_out_free: bool,
                 in_jail_turns: int,
                 doubles: int,):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.jail = jail
        self.jail_out_free = jail_out_free
        self.in_jail_turns = in_jail_turns
        self.doubles = doubles
    

    def normal_turn(self, squares, jail_doubles, roll_one=0, roll_two=0):
        if not jail_doubles:
            roll_one, roll_two = dice_roll()
            print(f"1st: {roll_one}, 2nd: {roll_two} = {roll_one + roll_two}")

            if roll_one == roll_two:
                print("Doubles!")
                self.doubles += 1
            else:
                self.doubles = 0
        
        input()
        self.advance(roll_one + roll_two)
        current_square = squares[self.location]
        print(f"New square:\n{self.location} - "
              f"{current_square['name']}")
    

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

    def in_jail(self, squares):
        print("You're in Jail\n")
        if self.in_jail_turns <= 3:
            print("(r) _R_oll doubles")
        if self.jail_out_free:
            print("(f) Use Get Out Of Jail _F_ree card")
        print("([b]) Pay $50 _b_ail")
        option = input("Enter choice:")

        self.jail_options(option, squares)
    
    def jail_options(self, option, squares):
        if option == "r" and self.in_jail_turns <= 3:
            roll_one, roll_two = dice_roll()
            print(f"1st roll: {roll_one}, 2nd roll: {roll_two}")

            if roll_one == roll_two:
                print("You rolled a double!"
                      "\nYou've been released")
                self.get_out_of_jail(squares, (False, roll_one, roll_two))
                return
            print("You didn't roll a double"
                  "\nYou'll remain in Jail")
            return
        
        elif option == "f" and self.jail_out_free:
            print("You have used your Get Out Of Jail Free Card")
            self.get_out_of_jail(squares, False)
            return
        
        print("You've paid $50 bail to get out of jail")
        self.balance -= 50
        self.get_out_of_jail(squares, False)
        return

    def get_out_of_jail(self, squares, double_roll=(False, 0, 0)):
        jail_doubles, roll_one, roll_two = double_roll
        self.jail = False
        self.normal_turn(squares, jail_doubles, roll_one, roll_two)


    def print_stats(self, player_num, current_square):
        print(f"\nPlayer {player_num}'s turn"
              f"\nCurrent balance: {self.balance}"
              f"\nCurrent square:\n{self.location} - {current_square['name']}")
    
    def advance(self, moves):
        if self.location + moves > 39:
            self.location = (self.location + moves) - 40
            print("You passed Go, recieve $200")
            self.balance += 200
            return
        self.location += moves

    def add_balance(self, amount):
        self.balance += amount

    def remove_balance(self, amount):
        self.balance -= amount


def player_setup():
    # Setting player count
    while True:
        player_count = input("\nHow many players?(2-8):")
        if not player_count.isdigit():
            print("Try again")
            continue
        if not int(player_count) in range(2, 8+1):
            print("Try again")
            continue
        player_count = int(player_count)
        break
    
    # Creating player data
    player_list = {}
    for count in range(1, player_count+1):
        # Player(location, balance, properties, jail, jail_out_free, in_jail_turns, doubles)
        player_list.update({count: Player(0, 1500, [], False, False, 0, 0)})
    
    return player_list, [i for i in range(1, player_count+1)]


def file_setup():
    file_list = ["data/squares.py",]

    for file in file_list:
        if not path.isfile(file):
            print(f'File "{file}" is missing'
                  '\nPlease download all files')

    with open("data/squares.py", "r+") as squares_file:
        squares = eval(squares_file.read())

    return squares

def turnAdvance(player_num, remaining_players):
    if player_num == max(remaining_players):
        return min(remaining_players)
    
    return remaining_players[remaining_players.index(player_num) + 1]

def dice_roll():
    input("\nRoll dice >")
    roll_one, roll_two = (randint(1, 6), randint(1, 6))

    return roll_one, roll_two