from options.debug_cheats import *
from random import randint


jailed_list: dict[int, dict[str, bool | int]] = {}


def create_jail_space(player):
    jailed_list.update(
        {
            player.INDEX: {
                "jailed": False,
                "goojf": 0,
                "jail_turns": 0,
            }
        }
    )
    if any((START_JAILED, START_GOOJF)):
        start_options(player)


def jail_player(player):
    player_cell = jailed_list[player.INDEX]

    player_cell["jailed"] = True
    player.location = 10
    print("You have been sent to Jail")


def goojf_card(player, amount):
    player_cell = jailed_list[player.INDEX]

    if amount > 0:
        print(f"You've recieved {amount} goojf card(s)")
    elif amount < 0:
        print(f"You've lost/used {abs(amount)} goojf card(s)")

    player_cell["goojf"] += amount


def get_out_of_jail(player, double_roll=(0, 0)):
    player_cell = jailed_list[player.INDEX]

    player_cell["jailed"] = False
    player.normal_turn(double_roll)


def jail_turn(player):
    player_cell = jailed_list[player.INDEX]

    print("You're in Jail\n")
    options = []
    if player_cell["jail_turns"] <= 3:
        print("(r) _R_oll doubles")
        options.append("r")
    if player_cell["goojf"] > 0:
        print("(f) Use Get Out Of Jail _F_ree card")
        options.append("f")
    print("[b] Pay $50 _b_ail")

    option = input("Enter choice:")
    if option in options:
        option = option[0].casefold()
    match option:
        case "r":
            input("\nRoll dice >")
            roll_one, roll_two = (randint(1, 6), randint(1, 6))
            print(f"1st: {roll_one} + 2nd: {roll_two} = {roll_one + roll_two}")
            if roll_one == roll_two:
                print("You rolled a double!\nYou've been released")
                get_out_of_jail(player, (roll_one, roll_two))
                return
            print("You didn't roll a double\nYou'll remain in Jail")
            player_cell["jail_turns"] += 1
            return
        case "f":
            print("You've used your Get Out Of Jail Free Card")
            goojf_card(player, -1)
            get_out_of_jail(player)
            return
        case _:
            player.balance -= 50
            print("You've paid $50 bail to get out of jail")
            get_out_of_jail(player)
            return


def start_options(player):
    player_cell = jailed_list[player.INDEX]
    if player.INDEX in START_JAILED:
        player_cell["jailed"] = START_JAILED[player.INDEX]
    if player.INDEX in START_GOOJF:
        player_cell["goojf"] = START_GOOJF[player.INDEX]
