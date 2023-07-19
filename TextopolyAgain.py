from random import randint
from time import sleep

# Welcome to my potentially better code than the old one

class Player:
    def __init__(self, location, balance, properties, extras):
        self.location = location
        self.balance = balance
        self.properties = properties
        self.extras = extras

# Setting player count
while True:
    playerCount = input("How many players?(2-8):")
    if not playerCount.isdigit():
        print("Try again")
        continue
    if not int(playerCount) in range(2, 8+1):
        print("Try again")
        continue
    break

# Creating player data
playerList = {}
for count in range(1, playerCount+1):
    playerList.update({count: Player(0, 1500, [], {"Jail": False, "JailOutFree": False, "Doubles": 0})})
# test

# 123