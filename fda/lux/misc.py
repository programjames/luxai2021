from lux.game_constants import GAME_CONSTANTS as gc
from lux.constants import Constants


def is_day(turn):
    return turn % (gc["PARAMETERS"]["DAY_LENGTH"] +
                   gc["PARAMETERS"]["NIGHT_LENGTH"]) < gc["PARAMETERS"]["DAY_LENGTH"]


def turns_till_day(turn):
    r = (turn - 1) % (gc["PARAMETERS"]["DAY_LENGTH"] +
                      gc["PARAMETERS"]["NIGHT_LENGTH"])
    if r < gc["PARAMETERS"]["DAY_LENGTH"]:
        return 0
    return gc["PARAMETERS"]["DAY_LENGTH"] + gc["PARAMETERS"]["NIGHT_LENGTH"] - r


DIRECTION_FROM_DELTA = {
    (0, 0): Constants.DIRECTIONS.CENTER,
    (1, 0): Constants.DIRECTIONS.EAST,
    (-1, 0): Constants.DIRECTIONS.WEST,
    (0, 1): Constants.DIRECTIONS.SOUTH,
    (0, -1): Constants.DIRECTIONS.NORTH
}

DELTA_FROM_DIRECTION = dict((value, key)
                            for key, value in DIRECTION_FROM_DELTA.items())

U = {0: "WORKER", 1: "CART", "WORKER": 0, "CART": 1}


DIRECTIONS = Constants.DIRECTIONS
NEIGHBORS = [DIRECTIONS.NORTH, DIRECTIONS.EAST,
             DIRECTIONS.SOUTH, DIRECTIONS.WEST]

DELTA_NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
