try:
    from modules.textopoly import *
except ModuleNotFoundError:
    print("Please download all files.")
    raise SystemExit


def main():
    while True:
        player = player_data.player_list[player_data.player_index]
        square = files.squares[player.location]
        player_cell = jail.jailed_list[player.index]

        print_stats(player, square)

        if player_cell["jailed"]:
            jail.jail_turn(player)
        else:
            player.normal_turn()

        player_data.bankruptcy(player)
        player_data.turn_advance(player)


if __name__ == "__main__" and MODULE_GUARD:
    main()
