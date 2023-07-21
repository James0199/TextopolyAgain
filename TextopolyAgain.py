from random import randint
from time import sleep

class Player:
    def __init__(self, location, balance, properties, extras):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras
    
    def print_stats(self, player_index):
        print(f"\nPlayer {player_index}'s turn"
              f"\nCurrent balance: {self.balance}"
              f"Current square:\n{self.location} - {squares[self.location]['name']}")
    
    def add_balance(self, amount):
        self.balance += amount

    def remove_balance(self, amount):
        self.balance -= amount

    def advance(self, moves):
        if self.location + moves > 39:
            self.location = (self.location + moves) - 40
            print("You passed Go, recieve $200")
            self.balance += 200
            return
        self.location += moves
    
    def go_to_jail(self):
        self.extras["jail"] = True
        self.location = 10
        print("You have been sent to Jail")

    def normal_turn(self, double_rolls):
        input("\nRoll dice >")
        rollOne, rollTwo = (randint(1, 6), randint(1, 6))
        print(f"1st: {rollOne}, 2nd: {rollTwo} = {rollOne + rollTwo}")

        if rollOne == rollTwo:
            print("Doubles!")
            double_rolls += 1
        else:
            double_rolls = 0
        
        self.advance(rollOne + rollTwo)
        print(f"\nNew square:\n{players[player_index].location} - {squares[players[player_index].location]['name']}")
        
        return double_rolls
    
    def inJail(self, inJailTurns):
        print("You are in Jail")

def playerSetup():
    # Setting player count
    while True:
        player_count = input("How many players?(2-8):")
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
        player_list.update({count: Player(0, 1500, [], {"jail": False, "jailOutFree": False})})
    
    return player_list, [i for i in range(1, player_count+1)]

# Setting up external files
with open("squares.txt", "r") as squares_file:
    squares = eval(squares_file.read())

# Setting up player data and game data
players, remaining_players = playerSetup()
player_index = 1
double_rolls = 0; inJailTurns = 0
current_player = players[player_index]

print("Press enter to roll dice")

while True:
    current_player.print_stats(player_index)

    if current_player.extras["jail"] == True:
        inJailTurns = current_player.inJail()
    else:
        double_rolls = current_player.normal_turn(double_rolls)

    input("\nEnter to Continue...")

    if current_player.location == 30:
        print("You landed on Go to Jail!")
        current_player.go_to_jail()
    elif double_rolls >= 3:
        print("You rolled 3 consecutive doubles!")
        current_player.go_to_jail()
    
    if player_index == max(remaining_players):
        player_index = min(remaining_players)
        continue

    player_index = remaining_players[remaining_players.index(player_index) + 1]
    current_player = players[player_index]
    