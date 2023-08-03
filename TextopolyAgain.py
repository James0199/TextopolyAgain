from data.textopoly import *

welcome()
player_index, players, remaining_players = player_setup()

while True:
    current_player = players[player_index]
    current_square = files.squares[current_player.location]

    current_player.print_stats(current_square)

    if current_player.jail:
        current_player.in_jail()
    else:
        current_player.normal_turn()

    players = bankruptcy(current_player, players)

    player_index = turn_advance(player_index, players, current_player)
