import fda
from lux.game_constants import GAME_CONSTANTS as gc
from lux.constants import Constants
import lux.misc

import sys

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


class Pather(object):
    def __init__(self, game, player):
        is_day = lux.misc.is_day(game.turn)
        resource_types = ["WOOD"]
        for t in ["COAL", "URANIUM"]:
            if player.research_points >= gc["PARAMETERS"]["RESEARCH_REQUIREMENTS"][t]:
                resource_types.append(t)
        self.scores = fda.prepare_scores(
            game.map, player, resource_types)
        self.rs = dict()
        for unit_type in ["WORKER", "CART"]:
            self.rs[U[unit_type]] = fda.prepare_resistances(
                game.map, unit_type, is_day)
        self.ps = dict()
        for unit_type, r in self.rs.items():
            self.ps[unit_type] = fda.get_potential(-self.scores, r)

        print(player.research_points, resource_types, file=sys.stderr)
        print(self.ps[0].tolist(), file=open("test.txt", "w"))

        self.map = game.map

    def on_map(self, x, y):
        return x >= 0 and y >= 0 and x < self.map.width and y < self.map.height

    def sorted_moves(self, unit):
        x, y = unit.pos.x, unit.pos.y
        p = self.ps[unit.type]
        ps = [p[y][x]]
        dirs = [Constants.DIRECTIONS.CENTER]
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self.on_map(new_x, new_y):
                ps.append(p[new_y][new_x])
                dirs.append(DIRECTION_FROM_DELTA[(dx, dy)])
        return [d for _, d in sorted(zip(ps, dirs))]

    def best_move(self, unit):
        x, y = unit.pos.x, unit.pos.y
        p = self.ps[unit.type]
        best_p = p[y][x]
        best_dir = Constants.DIRECTIONS.CENTER
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self.on_map(new_x, new_y) and p[new_y][new_x] > best_p:
                best_p = p[new_y][new_x]
                best_dir = DIRECTION_FROM_DELTA[(dx, dy)]
        return best_dir

    def update_board(self, unit, move):
        dx, dy = DELTA_FROM_DIRECTION[move]
        self.ps[unit.type][unit.pos.y + dy][unit.pos.x + dx] = -200000
