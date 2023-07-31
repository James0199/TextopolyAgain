from data.textopoly import *

welcome()

squares, com_chest, chance = file_setup()
players, remaining_players = player_setup()

player_num = 1

while True:
    current_player = players[player_num]
    current_square = squares[current_player.location]

    current_player.print_stats(player_num, current_square)

    if current_player.jail == True:
        current_player.in_jail(False)
    else:
        current_player.normal_turn()

    current_player.jail_conditions()

    input("\nEnter to Continue...")

    player_num = turnAdvance(player_num, remaining_players)