{
    0: {"name": "Advance to Boardwalk", "type": "set_loc_property", "value": 39},
    1: {
        "name": "Advance to Go\n(Collect $200)",
        "type": "go",
    },
    2: {
        "name": "Advance to Illinois Avenue." "\nIf you pass Go, collect $200",
        "type": "set_loc_property",
        "value": 24,
    },
    3: {
        "name": "Advance to St. Charles Place." "\nIf you pass Go, collect $200",
        "type": "set_loc_property",
        "value": 11,
    },
    4: {
        "name": "Take a trip to Reading Railroad." "\nIf you pass Go, collect $200",
        "type": "set_loc_property",
        "value": 15,
    },
    5: {
        "name": "Advance to B. & O. Railroad." "\n If you pass Go, collect $200",
        "type": "set_loc_property",
        "value": 25,
    },
    6: {
        "name": "Advance to Water Works" "\n If you pass Go, collect $200",
        "type": "set_loc_property",
        "value": 28,
    },
    7: {"name": "Bank pays you dividend of $50", "type": "balance", "value": 50},
    8: {
        "name": "Get Out Of Jail Free",
        "type": "GOOJF",
    },
    9: {
        "name": "Go to Jail."
        "\nGo directly to Jail, do not pass Go, do not collect $200",
        "type": "jail",
    },
    10: {"name": "Go Back 3 Spaces", "type": "move", "value": -3},
    11: {"name": "Speeding fine $15", "type": "balance", "value": -15},
    12: {
        "name": "Your building loan matures." "\nCollect $150",
        "type": "balance",
        "value": 150,
    },
}
