from random import randint
from textopoly import *

input("\nWelcome to Textopoly!\n"
      "\nNotes:"
      "\nPress enter to advance prompts."
      "\nIf you don't choose a valid option while in jail,"
      "\nYou'll automatically pay $50 bail.")

# File and player setup
squares = file_setup()
players, remaining_players = player_setup()

# Initialize variables
player_num = 1

while True:
    current_player = players[player_num]
    current_square = squares[current_player.location]

    current_player.print_stats(player_num, current_square)

    if current_player.jail == True:
        current_player.in_jail(squares, False)
    else:
        current_player.normal_turn(squares)

    current_player.jail_conditions()

    input("\nEnter to Continue...")

    player_num = turnAdvance(player_num, remaining_players)