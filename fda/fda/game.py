import numpy as np
from lux.game_constants import GAME_CONSTANTS as gc
import sys


def prepare_scores(game_map, player, resource_types=None):
    nx, ny = game_map.width, game_map.height
    scores = np.zeros((ny, nx))
    if resource_types is None:
        resource_types = ["WOOD", "COAL", "URANIUM"]
    for resource_type in resource_types:
        rate = gc["PARAMETERS"]["RESOURCE_TO_FUEL_RATE"][resource_type] * \
            gc["PARAMETERS"]["WORKER_COLLECTION_RATE"][resource_type]
        for x in range(nx):
            for y in range(ny):
                c = game_map.get_cell(x, y)
                if c.has_resource() and c.resource.type.upper() == resource_type:
                    scores[y][x] += rate
    return scores


def prepare_resistances(game_map, unit_type, daytime=True):
    def res(road):
        r = gc["PARAMETERS"]["UNIT_ACTION_COOLDOWN"][unit_type]
        if daytime is False:
            r *= 2
        r -= road
        r = max(r, 1)
        return r

    nx, ny = game_map.width, game_map.height
    resistances = np.zeros((ny, nx))
    for x in range(nx):
        for y in range(ny):
            resistances[y][x] = res(game_map.get_cell(x, y).road)

    return resistances
