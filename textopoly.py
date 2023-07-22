from random import randint
from os import path

class Player:
    def __init__(self, location: int,
                 balance: int,
                 properties: list,
                 jail: bool,
                 jail_out_free: bool):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.jail = jail
        self.jail_out_free = jail_out_free
    

    def normal_turn(self, double_rolls, squares):

        input("\nRoll dice >")
        rollOne, rollTwo = (randint(1, 6), randint(1, 6))
        print(f"1st: {rollOne}, 2nd: {rollTwo} = {rollOne + rollTwo}")

        if rollOne == rollTwo:
            print("Doubles!")
            double_rolls += 1
        else:
            double_rolls = 0
        
        input()
        self.advance(rollOne + rollTwo)
        current_square = squares[self.location]
        print(f"New square:\n{self.location} - "
              f"{current_square['name']}")
        
        return double_rolls
    
    def in_jail(self, in_jail_turns):
        print("You are in Jail")

        return in_jail_turns


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
    
    def go_to_jail(self):
        self.jail = True
        self.location = 10
        print("You have been sent to Jail")

    def jail_conditions(self, double_rolls):
        if self.location == 30:
            print("\nYou landed on Go to Jail!")
            self.go_to_jail()
        elif double_rolls >= 3:
            print("\nYou rolled 3 consecutive doubles!")
            self.go_to_jail()


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
        # Player(location, balance, properties, jail, jail_out_free)
        player_list.update({count: Player(0, 1500, [], False, False)})
    
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
