from random import randint
from textopoly import *


# File and player setup
squares = file_setup()
players, remaining_players = player_setup()

# Initialize variables
player_num = 1
double_rolls = 0
in_jail_turns = 0

print("Press enter to roll dice")
while True:
    current_player = players[player_num]
    current_square = squares[current_player.location]

    current_player.print_stats(player_num, current_square)

    if current_player.jail == True:
        in_jail_turns = current_player.in_jail(in_jail_turns)
    else:
        double_rolls = current_player.normal_turn(double_rolls, squares)

    current_player.jail_conditions(double_rolls)

    input("\nEnter to Continue...")

    if player_num == max(remaining_players):
        player_num = min(remaining_players)
        continue
    player_num = remaining_players[remaining_players.index(player_num) + 1]
    