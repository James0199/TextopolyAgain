try:
    eval("str | int")
    from textopoly import *
except TypeError:
    print("This project requires Python 3.10+")
except ModuleNotFoundError:
    print("\nPlease download all files.\n")
    raise SystemExit


def main():
    while True:
        player = player_data.player_list[player_data.player_index]
        square = files.squares[player.location]
        player_cell = jail.jailed_list[player.INDEX]

        stats.main_stats(player, square)
        if player_cell["jailed"]:
            jail.jail_turn(player)
        else:
            player.normal_turn()

        player_data.bankruptcy(player)
        player_data.turn_advance(player)


if __name__ == "__main__":
    try:
        if WELCOME_MESSAGE:
            print("\nWelcome to Textopoly(Again)!\n[Made by James0199]")
            if LOAD_FILES:
                input(files.HELP)
        player_data.player_setup()
        main()
    except KeyboardInterrupt:
        print("\n\nGame Exited.")
        raise SystemExit
