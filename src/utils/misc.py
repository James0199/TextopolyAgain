def auction(square, player_list):
    print(
        "Input format: (player index), (amount of money)"
        '\nExample: 1, 200; Enter "end" to end auction\n'
    )
    if square.COST % 20 != 0:
        start_bid = 25
    else:
        start_bid = 20
    player_high, highest_bid = -1, start_bid
    print(f"Starting bid: ${start_bid}")
    while True:
        try:
            option = input("[auction] Enter bid:")
            if option in ("end", ""):
                break
            option = option.split(", ")
            player = player_list[int(option[0]) - 1]
            player_bid = int(option[1])

            if player.balance < player_bid:
                print("Not enough balance\n")
                continue
            if player_bid < highest_bid + start_bid:
                print(f"Must be higher than highest bid by at least ${start_bid}\n")
                continue

            player_high = player
            highest_bid = player_bid
            print(f"New bid: ${highest_bid} by player {player_high.INDEX+1}")

        except ValueError:
            print("Invalid input\n")
            continue
        except IndexError:
            print("Invalid player\n")
            continue

    if (player_high, highest_bid) == (-1, start_bid):
        print("No one got the property")
        return False

    print(f"Player {player_high.INDEX+1} got the property!")
    return player_high, highest_bid


def welcome():
    try:
        with open("data/welcome.txt") as welcome_file:
            input(welcome_file.read())
    except FileNotFoundError:
        print("Could not find welcome.txt file")
