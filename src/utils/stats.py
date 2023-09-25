def main_stats(player, square):
    print(
        f"\nPlayer {player.INDEX + 1}'s turn"
        f"\nBalance: ${player.balance}"
        f"\nSquare: {square.INDEX} - {square.NAME}"
    )


def stat_options(player, player_data, squares):
    print(
        '\nType "m" to return to last menu\n'
        "(p) View _p_layer stats\n"
        "(s) View square (properties) stats"
    )
    while True:
        option = input("Enter option:")
        if option:
            option = option.casefold()[0]
        match option:
            case "p":
                print(f"\nYour player index: {player.INDEX+1}")
                while True:
                    try:
                        player_select = input("Enter player (index): ")
                        if player_select == "m":
                            break
                        player_select = player_data.player_list[int(player_select) - 1]
                        player_stats(player_select)
                    except (ValueError, IndexError):
                        print("Invalid player index")
            case "s":
                pass
            case "m":
                break
            case _:
                print("Invalid option")
                continue


def player_stats(player):
    stats = vars(player).items()
    print()
    for attr, value in stats:
        match attr:
            case "INDEX":
                print(f"Player index: {value+1}")
            case "balance":
                print(f"{attr.capitalize()}: ${value}")
            case "doubles":
                print(f"Consecutive doubles: {value}")
            case "color_sets":
                print(f"Owned color sets: {', '.join(value)}")
    print()
