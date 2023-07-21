from random import randint
from time import sleep

class Player:
    def __init__(self, location, balance, properties, extras):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras
    
    def printStats(self, playerIndex):
        print(f"\nPlayer {playerIndex}'s turn"
              f"\nCurrent balance: {self.balance}"
              f"Current square:\n{self.location} - {squares[self.location]['name']}")
    
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
        print("You have been sent to Jail")

    def normalTurn(self, doubleRolls):
        input("\nRoll dice >")
        rollOne, rollTwo = (randint(1, 6), randint(1, 6))
        print(f"1st: {rollOne}, 2nd: {rollTwo} = {rollOne + rollTwo}")

        if rollOne == rollTwo:
            print("Doubles!")
            doubleRolls += 1
        else:
            doubleRolls = 0
        
        self.advance(rollOne + rollTwo)
        print(f"\nNew square:\n{players[playerIndex].location} - {squares[players[playerIndex].location]['name']}")
        
        return doubleRolls
    
    def inJail(self, inJailTurns):
        print("You are in Jail")

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
        playerList.update({count: Player(0, 1500, [], {"jail": False, "jailOutFree": False})})
    
    return playerList, [i for i in range(1, playerCount+1)]

# Setting up external files
with open("squares.txt", "r") as squaresFile:
    squares = eval(squaresFile.read())

# Setting up player data and game data
players, remainingPlayers = playerSetup()
playerIndex = 1
doubleRolls = 0; inJailTurns = 0
currentPlayer = players[playerIndex]

print("Press enter to roll dice")

while True:
    currentPlayer.printStats(playerIndex)

    if currentPlayer.extras["jail"] == True:
        inJailTurns = currentPlayer.inJail()
    else:
        doubleRolls = currentPlayer.normalTurn(doubleRolls)

    input("\nEnter to Continue...")

    if currentPlayer.location == 30:
        print("You landed on Go to Jail!")
        currentPlayer.goToJail()
    elif doubleRolls >= 3:
        print("You rolled 3 consecutive doubles!")
        currentPlayer.goToJail()
    
    if playerIndex == max(remainingPlayers):
        playerIndex = min(remainingPlayers)
        continue

    playerIndex = remainingPlayers[remainingPlayers.index(playerIndex) + 1]
    currentPlayer = players[playerIndex]
    