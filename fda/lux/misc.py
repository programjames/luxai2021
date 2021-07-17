from lux.game_constants import GAME_CONSTANTS as gc


def is_day(turn):
    return turn % (gc["PARAMETERS"]["DAY_LENGTH"] +
                   gc["PARAMETERS"]["NIGHT_LENGTH"]) < gc["PARAMETERS"]["DAY_LENGTH"]
