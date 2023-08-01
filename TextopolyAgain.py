from data.textopoly import *

welcome()

squares, com_chest, chance = file_setup()
player_num, players, remaining_players = player_setup()

while True:
    current_player = players[player_num]
    current_square = squares[current_player.location]

    current_player.print_stats(player_num, current_square)

    if current_player.jail:
        current_player.in_jail(False)
    else:
        current_player.normal_turn()

    input("\nEnter to Continue...")

    player_num = turn_advance(player_num, remaining_players)
