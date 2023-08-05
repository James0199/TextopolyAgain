from data.textopoly import *

welcome()
players = PlayerData()

while True:
    current_player = players.player_list[players.player_index]
    current_square = files.squares[current_player.location]

    current_player.print_stats(current_square)

    if current_player.jail:
        current_player.in_jail()
    else:
        current_player.normal_turn()

    players.bankruptcy(current_player)

    players.turn_advance(current_player)
