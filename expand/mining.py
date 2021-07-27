import fda
from lux.game_constants import GAME_CONSTANTS as gc
from lux.constants import Constants
from lux.misc import *
from lux.annotate import circle

import numpy as np

import sys


class Miner(object):
    def update(self, game_map, player):
        self.map = game_map
        day = True  # Might change this later.
        resource_types = ["WOOD"]
        for t in ["COAL", "URANIUM"]:
            if player.research_points >= gc["PARAMETERS"]["RESEARCH_REQUIREMENTS"][t]:
                resource_types.append(t)
        self.scores = fda.prepare_scores(
            game_map, player, resource_types)
        self.rs = dict()
        for unit_type in ["WORKER", "CART"]:
            self.rs[U[unit_type]] = fda.prepare_resistances(
                game_map, unit_type, day)
        self.ps = dict()
        for unit_type, r in self.rs.items():
            self.ps[unit_type] = fda.get_potential_neumann(-self.scores, r)

    def sorted_dirs(self, x, y, passable=None, unit_type=None):
        if passable is None:
            def passable(x, y): return True
        if unit_type is None:
            unit_type = 0  # i.e. worker

        p = self.ps[unit_type]
        ps = [p[y][x]]
        dirs = [Constants.DIRECTIONS.CENTER]
        for dx, dy in DELTA_NEIGHBORS:
            new_x, new_y = x + dx, y + dy
            if passable(new_x, new_y):
                ps.insert(0, p[new_y][new_x])
                dirs.insert(0, DIRECTION_FROM_DELTA[(dx, dy)])
        return [d for _, d in sorted(zip(ps, dirs), reverse=True)]

    def dir(self, x, y, passable=None, unit_type=None):
        return self.sorted_dirs(x, y, passable, unit_type)[0]
