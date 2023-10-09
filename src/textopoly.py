try:
    from abc import ABC, abstractmethod
    from random import randint
    from options.debug_cheats import *
    from options.house_rules import *
    from utils import files, jail, stats, mortgage, houses, trade, misc
except ModuleNotFoundError:
    print("Couldn't find a module,\nPlease download all files.")
    raise SystemExit


if __name__ == "__main__" and MODULE_GUARD:
    print("Please run the main.py file,\nThis module is meant to be imported.")
    raise SystemExit

print("Loading game...")


class Square(ABC):
    def __init__(self, index: int, name: str, square_type: str):
        self.INDEX = index
        self.NAME = name
        self.SQUARE_TYPE = square_type

    def __repr__(self):
        return str(vars(self))


class Tax(Square):
    def __init__(self, index: int, name: str, square_type: str, cost: int):
        super().__init__(index, name, square_type)
        self.COST = cost

    def landing(self, player):
        print(f"You paid ${self.COST} in {self.NAME}")
        player.balance -= self.COST


class Corner(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        if player.location == 30 and not SKIP_JAIL:
            print("You landed on Go To Jail!")
            jail.jail_player(player)
        elif player.location == 20 and PARKING_BONUS_SKIP_SPACES is False:
            if type(PARKING_BONUS) is not int:
                return
            amount = abs(PARKING_BONUS)
            player.balance += amount
            print(f"You got the free parking bonus of ${amount}")


class ComChest(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player):
        input("Pick Card >")
        card = files.COM_CHEST[randint(0, 13)]
        print(card["name"])
        match card["name"]:
            case "balance":
                player.balance += card["value"]
            case "goojf":
                jail.goojf_card(player, 1)
            case "jail":
                jail.jail_player(player)
            case "go":
                player.location = 0
                player.balance += 200


class Chance(Square):
    def __init__(self, index: int, name: str, square_type: str):
        super().__init__(index, name, square_type)

    @staticmethod
    def landing(player, dice_roll):
        input("Pick Card >")
        card = files.CHANCE[randint(0, 12)]
        print(card["name"])
        match card["type"]:
            case "set_loc_property":
                player.location = card["value"]
                if player.location > card["value"]:
                    print("You passed Go")
                    player.balance += 200

                square = files.squares[player.location]
                if square.SQUARE_TYPE == "utility":
                    square.landing(player, dice_roll)
                else:
                    square.landing(player)

            case "balance":
                player.balance += card["value"]
            case "move":
                player.location -= card["value"]
            case "goojf":
                jail.goojf_card(player, 1)
            case "jail":
                jail.jail_player(player)
            case "go":
                player.location = 0
                player.balance += 200


class Ownable(Square, ABC):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        owner: None | int,
        mortgaged: bool,
    ):
        super().__init__(index, name, square_type)
        self.COST = cost
        self.owner = owner
        self.mortgaged = mortgaged

    def purchase(self, player):
        if not NO_AUCTION_ONLY:
            option = input(
                f"\nWould you like to purchase {self.NAME}\nfor ${self.COST}? (y/[n]):"
            )
        else:
            option = "n"

        if option == "y" and player.balance - self.COST >= 0:
            self.receive_property(player, self.COST)
            print(f"You have bought {self.NAME} for ${self.COST}")
        elif NO_AUCTION_ONLY is None or NO_AUCTION_ONLY:
            print("\nAuction!")
            status = misc.auction(self, player_data.player_list)
            if status is False:
                return
            player, bid = status
            self.receive_property(player, bid)

    @abstractmethod
    def receive_property(self, player, cost):
        ...


class Street(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        color: str,
        improvement_cost: int,
        rent_levels: dict[int, int],
        owner: None | int,
        mortgaged: bool,
        improvement_level: int,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.COLOR = color
        self.improvement_level = improvement_level
        self.IMPROVEMENT_COST = improvement_cost
        self.RENT_LEVELS = rent_levels

    def receive_property(self, player, cost):
        player.balance -= cost
        player.properties["street"].append(self.INDEX)
        self.update_color_set(player)
        files.squares[player.location].owner = player.INDEX

    def update_color_set(self, player):
        color_set = files.PROPERTY_SETS["street"][self.COLOR]
        color_set_squares = [files.squares[square] for square in color_set]

        if all([street.owner == player.INDEX for street in color_set_squares]):
            player.color_sets.append(self.COLOR)
            print(f"Player {player.INDEX} got the {self.COLOR} color set!")

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owner_player = player_data.player_list[self.owner]
        print(f"Player {self.owner + 1} owns this street")
        if owner_player is player:
            return

        if jail.jailed_list[owner_player.INDEX]["jailed"] and NO_JAIL_RENT:
            print("This street's owner is in jail, no rent will be collected")
            return

        rent = self.RENT_LEVELS[self.improvement_level]
        if self.improvement_level > 0:
            print(f"And this street has {self.improvement_level} houses\n")
        elif self.COLOR in player.color_sets and self.improvement_level == 0:
            print("And also owns the color set")
            rent *= 2
        print(f"You'll pay ${rent} to player {owner_player.INDEX + 1}")
        player.balance -= rent
        owner_player.balance += rent


class Railroad(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        rent_levels: dict[int, int],
        owner: None | int,
        mortgaged: bool,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.RENT_LEVELS = rent_levels

    def receive_property(self, player, cost):
        player.balance -= cost
        player.properties["railroad"].append(self.INDEX)
        files.squares[player.location].owner = player.INDEX

    def landing(self, player):
        if self.owner is None:
            self.purchase(player)
            return

        owner_player = player_data.player_list[self.owner]
        if jail.jailed_list[owner_player.INDEX]["jailed"] and NO_JAIL_RENT:
            print("This railroad's owner is in jail, no rent will be collected")
            return

        owned_railroads = len(
            [
                railroad
                for railroad in files.PROPERTY_SETS["railroad"]
                if self.owner == files.squares[railroad].owner
            ]
        )
        rent = 25 * (2**owned_railroads)
        print(
            f"Player {self.owner + 1} owns this railroad,\n"
            f"And owns {owned_railroads} railroads\n"
            f"You'll pay ${rent} to player {self.owner + 1}"
        )
        player.balance -= rent
        owner_player.balance += rent


class Utility(Ownable):
    def __init__(
        self,
        index: int,
        name: str,
        square_type: str,
        cost: int,
        owner: None | int,
        mortgaged: bool,
    ):
        super().__init__(index, name, square_type, cost, owner, mortgaged)
        self.OTHER_UTIL = None

    def receive_property(self, player, cost):
        player.balance -= cost
        player.properties["utility"].append(self.INDEX)
        files.squares[player.location].owner = player.INDEX

    def define_other_util(self):
        self.OTHER_UTIL = [
            files.squares[util]
            for util in files.PROPERTY_SETS["utility"]
            if util != self.INDEX
        ][0]

    def landing(self, player, dice_roll):
        self.define_other_util()
        if self.owner is None:
            self.purchase(player)
            return

        owner_player: Player = player_data.player_list[self.owner]
        if jail.jailed_list[owner_player.INDEX]["jailed"] and NO_JAIL_RENT:
            print("This utility's owner is in jail, no rent will be collected")
            return

        print(f"Player {self.owner + 1} owns this utility,")
        multiplier = 4
        if self.owner == self.OTHER_UTIL.owner:
            print("And also owns the other utility,")
            multiplier = 10
        print(
            f"You'll pay {multiplier} times your dice roll ({dice_roll}) "
            f"to player {self.owner + 1}"
        )
        player.balance -= dice_roll * multiplier
        owner_player.balance += dice_roll * multiplier


def square_dto(square: dict[str, str | int | None | bool | dict]) -> Square:
    square_args = list(square.values())
    match square["TYPE"]:
        case "street":
            square_args.extend((None, False, 0))
            square_obj = Street(*square_args)
        case "railroad":
            square_args.extend((None, False))
            square_obj = Railroad(*square_args)
        case "utility":
            square_args.extend((None, False))
            square_obj = Utility(*square_args)
        case "com_chest":
            square_obj = ComChest(*square_args)
        case "chance":
            square_obj = Chance(*square_args)
        case "tax":
            square_obj = Tax(*square_args)
        case "corner":
            square_obj = Corner(*square_args)
        case _:
            raise TypeError("Invalid square type")
    return square_obj


files.dict_to_obj(square_dto)
print("Loaded successfully!")


class Player:
    def __init__(self, index):
        self.INDEX: int = index
        self.location: int = 0
        self.balance: int = 1500
        self.doubles: int = 0
        self.color_sets: list[str] = []
        self.properties: dict[str, list[int]] = {
            "street": [],
            "railroad": [],
            "utility": [],
        }
        START_ENABLED = any(
            (START_BALANCE, START_LOCATION, START_DOUBLES, START_PROPERTIES)
        )
        if START_ENABLED:
            self.start_options()

    def __repr__(self):
        return str(vars(self))

    def normal_turn(self, dice_roll=(0, 0)):
        dice_roll = self.turn_options(True, dice_roll)
        input()
        self.advance(sum(dice_roll))

        square = files.squares[self.location]
        print(f"New square:\n" f"{self.location} - {square.NAME}")
        if square.SQUARE_TYPE in ("utility", "chance"):
            square.landing(self, sum(dice_roll))
        else:
            square.landing(self)

        self.turn_options(False)

    def turn_options(self, turn_start, dice_roll=(0, 0)) -> tuple[int, int]:
        if dice_roll != (0, 0):
            return dice_roll
        while True:
            print()
            has_properties = any(self.properties.values())
            jail_cell = jail.jailed_list[self.INDEX]
            options = ["v"]

            if has_properties:
                print("(m) _M_ortgage")
                options.append("m")
            if self.balance or jail_cell["goojf"]:
                print("(t) _T_rade")
                options.append("t")
            if self.color_sets:
                print("(h) Buy/sell _h_ouses")
                options.append("h")
            print("(v) _V_iew stats")
            if turn_start:
                print("[d] Roll _d_ice")
            else:
                print("[e] _E_nd turn")

            option = input("Enter option:")
            if option:
                option = option[0].casefold()
            if option not in options and turn_start:
                return self.roll_dice()
            match option:
                case "m":
                    mortgage.mortgage(self, files)
                case "t":
                    trade.start_trade(
                        self, player_data.player_list, jail.jailed_list, files
                    )
                case "h":
                    houses.exchange(self, files)
                case "v":
                    stats.stat_options(self, player_data.player_list, files.squares)
                case _:
                    break

    def roll_dice(self) -> tuple[int, int]:
        if SKIP_DICE:
            return 0, 0

        input("\nRoll dice >")
        dice_roll = (randint(1, 6), randint(1, 6))
        while (
            PARKING_BONUS_SKIP_SPACES is True
            and (sum(dice_roll) + self.location) % files.BOARD_LENGTH
            in files.PROPERTY_SETS["skip"]
        ):
            dice_roll = (randint(1, 6), randint(1, 6))
        print(f"1st: {dice_roll[0]} + 2nd: {dice_roll[1]} = {sum(dice_roll)}")

        self.doubles_roll(*dice_roll)
        return dice_roll

    def doubles_roll(self, roll_one, roll_two):
        if roll_one == roll_two and not DOUBLES_LOCK:
            print("Doubles!")
            self.doubles += 1
        else:
            self.doubles = 0

        if self.doubles >= 3:
            print("You rolled 3 consecutive doubles!")
            jail.jail_player(self)

    def advance(self, moves):
        new_location = self.location + moves
        if new_location == files.BOARD_LENGTH and GO_BONUS:
            self.location = 0
            print("You landed directly on Go, receive $400")
            self.balance += 400
            return
        elif new_location >= files.BOARD_LENGTH:
            self.location = new_location % files.BOARD_LENGTH
            print("You passed Go, receive $200")
            self.balance += 200
            return
        self.location = new_location

    def start_options(self):
        if self.INDEX in START_LOCATION:
            self.location = START_LOCATION[self.INDEX]
        if self.INDEX in START_BALANCE:
            self.balance = START_BALANCE[self.INDEX]
        if self.INDEX in START_DOUBLES:
            self.doubles = START_DOUBLES[self.INDEX]
        if self.INDEX in START_PROPERTIES:
            self.properties = START_PROPERTIES[self.INDEX]
        self.color_sets = [
            color
            for color in files.PROPERTY_SETS["street"]
            if all(
                street in self.properties["street"]
                for street in files.PROPERTY_SETS["street"][color]
            )
        ]


class PlayerData:
    def __init__(self):
        self.player_index = 0
        self.player_list = {}

    def player_setup(self):
        player_count = 1
        if PLAYER_COUNT_OVERRIDE > 0:
            player_count = PLAYER_COUNT_OVERRIDE

        while not (SINGLE_PLAYER or PLAYER_COUNT_OVERRIDE):
            try:
                player_count = input("\nHow many players?([2]-8):")

                if not player_count.isnumeric():
                    player_count = 2
                    break

                player_count = int(player_count)
                if not (player_count in range(2, 8 + 1)):
                    raise ValueError

                break
            except ValueError:
                print("Try again")
                continue

        self.player_list = {count: Player(count) for count in range(player_count)}

        for player in list(self.player_list.values()):
            jail.create_jail_space(player)

    def bankruptcy(self, player: Player):
        if not BANKRUPTCY_CHECK:
            return

        if player.balance < 0:
            self.player_list.pop(player.INDEX)
            if QUICK_END:
                print(
                    f"Player {player.INDEX+1} lost!\n"
                    f"Players {', '.join(self.player_list.keys())}"
                )
                raise SystemExit

        if len(self.player_list) == 1 and not SINGLE_PLAYER:
            winning_player: Player = list(self.player_list.values())[0]
            print(f"Congrats! Player {winning_player.INDEX+1} won the game!")
            raise SystemExit

        if len(self.player_list) == 0:
            print("No one won the game!")
            raise SystemExit

    def turn_advance(self, player: Player):
        player_cell = jail.jailed_list[player.INDEX]
        players = self.player_list.keys()

        if player.doubles in range(1, 3) and not player_cell["jailed"]:
            return
        if self.player_index == max(players):
            self.player_index = min(players)
            return

        self.player_index += 1


player_data = PlayerData()
