from random import randint
from textopoly import *


# File and player setup
squares = file_setup()
players, remaining_players = player_setup()

# Initialize variables
player_num = 1

print("Press enter to roll dice")
while True:
    current_player = players[player_num]
    current_square = squares[current_player.location]

    current_player.print_stats(player_num, current_square)

    if current_player.jail == True:
        current_player.in_jail()
    else:
        current_player.normal_turn(squares)

    current_player.jail_conditions()

    input("\nEnter to Continue...")

    player_num = turnAdvance(player_num, remaining_players)