from random import randint
from time import sleep

class Player:
    def __init__(self, location, balance, properties, extras):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras
    
    def addBalance(self, amount):
        self.balance += amount

    def removeBalance(self, amount):
        self.balance -= amount

    def advance(self, moves):
        if self.location + moves > 39:
            self.location = (self.location + moves) - 40
            print("You passed Go, recieve $200")
            self.balance += 200
            return
        self.location += moves
    
    def goToJail(self):
        self.extras["jail"] = True
        self.location = 10


def playerSetup():
    # Setting player count
    while True:
        playerCount = input("How many players?(2-8):")
        if not playerCount.isdigit():
            print("Try again")
            continue
        if not int(playerCount) in range(2, 8+1):
            print("Try again")
            continue
        playerCount = int(playerCount)
        break
    
    # Creating player data
    playerList = {}
    for count in range(1, playerCount+1):
        playerList.update({count: Player(0, 1500, [], {"Jail": False, "JailOutFree": False})})
    
    return playerList, playerCount, [i for i in range(1, playerCount+1)]

# Setting up players and player data
players, playerCount, remainingPlayers = playerSetup()
currentP = 1

# Load squares data
with open("squares.txt", "r") as squaresFile:
    squares = eval(squaresFile.read())

print("Press enter to roll dice")

doubleRolls = 0
while True:
    print(f"\nCurrent balance: {players[currentP].balance}")
    print(f"Current square:\n{players[currentP].location} - {squares[players[currentP].location]['name']}")

    input("\nRoll dice >")
    rollOne, rollTwo = (randint(1, 6), randint(1, 6))
    print(f"1st: {rollOne}, 2nd: {rollTwo} = {rollOne + rollTwo}")

    if rollOne == rollTwo:
        print("Doubles!")
        doubleRolls += 1
    
    players[currentP].advance(rollOne + rollTwo)
    print(f"\nNew square:\n{players[currentP].location} - {squares[players[currentP].location]['name']}")

    input("\nEnter to Continue...")

    if doubleRolls == 0:
        if currentP == max(remainingPlayers):
            currentP = min(remainingPlayers)
            continue
        currentP = remainingPlayers[remainingPlayers.index(currentP) + 1]
        continue
    elif doubleRolls >= 3:
        print("You rolled 3 consecutive doubles!\n"
              "Go to Jail.")
        players[currentP].goToJail()