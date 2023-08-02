from data.textopoly import *

welcome()

squares = file_setup()
player_index, players, lost_players = player_setup()

while True:
    current_player = players[player_index]
    current_square = squares[current_player.location]

    current_player.print_stats(current_square)

    if current_player.jail:
        current_player.in_jail()
    else:
        current_player.normal_turn()

    player_index = turn_advance(player_index, players, current_player)
