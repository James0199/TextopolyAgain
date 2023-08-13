from data.textopoly import *

welcome()
player_data = PlayerData()

while True:
    player = player_data.player_list[player_data.player_index]
    square = files.squares[player.location]
    player_cell = jail.jailed_list[player.index]

    print_stats(player, square)

    if player_cell["jailed"]:
        jail.jail_options(player)
    else:
        player.normal_turn()

    player_data.bankruptcy(player)
    player_data.turn_advance(player)
