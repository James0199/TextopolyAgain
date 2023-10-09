"""Custom house rules

These are some house rules to customize your game
You can look these up on the Monopoly Wiki or
the official site for a detailed description
"""

# OPTION = Value  # Default value
# Additional Notes

NO_AUCTION_ONLY = None  # None
# False = No auction,
# True = Auction only (no regular purchase)

PARKING_BONUS_SKIP_SPACES = None  # None
# False = Free parking bonus,
# True = Skip community chest/chance spaces

PARKING_BONUS = 0  # 0
# Only works with PARKING_BONUS_SKIP_SPACES = False
# Negative values will still give a positive amount

GO_BONUS = False  # False
# Get $400 when landing directly on Go

QUICK_END = False  # False
# End game after 1 player is bankrupt

NO_JAIL_RENT = False  # False
# Rent is not collected if the property owner is in jail

QUICK_JAIL = False  # False
# Ends jail within 1 turn
# You're forced to pay $50 bail if you don't roll a double
