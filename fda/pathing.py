import fda
from lux.game_constants import GAME_CONSTANTS as gc
from lux.constants import Constants
from lux.misc import *
from lux.annotate import circle

import numpy as np

import sys


class Pather(object):
    def __init__(self, game, player):
        self.map = game.map
        day = is_day(game.turn)
        resource_types = ["WOOD"]
        for t in ["COAL", "URANIUM"]:
            if player.research_points >= gc["PARAMETERS"]["RESEARCH_REQUIREMENTS"][t]:
                resource_types.append(t)
        self.scores = fda.prepare_scores(
            game.map, player, resource_types)
        self.rs = dict()
        for unit_type in ["WORKER", "CART"]:
            self.rs[U[unit_type]] = fda.prepare_resistances(
                game.map, unit_type, day)
        self.ps = dict()
        for unit_type, r in self.rs.items():
            self.ps[unit_type] = fda.get_potential_dirichlet(-self.scores, r)

        self.is_open = np.ones((game.map.height, game.map.width), dtype="bool")

        # Flood fill to make city_moves

        self.city_moves = [
            [0 for i in range(game.map.width)] for j in range(game.map.height)]

        self.city_locs = set()
        for city in player.cities.values():
            self.city_locs |= set(
                map(lambda c: (c.pos.x, c.pos.y), city.citytiles))
        open_set = self.city_locs
        closed_set = open_set.copy()
        d = 0
        while len(open_set) > 0:
            new_open = set()
            d += 1
            for x, y in open_set:
                for dx, dy in DELTA_NEIGHBORS:
                    new_x, new_y = x + dx, y + dy
                    if not self.on_map(new_x, new_y) or (new_x, new_y) in closed_set:
                        continue
                    new_open.add((new_x, new_y))
                    closed_set.add((new_x, new_y))
                    self.city_moves[new_y][new_x] = d
            open_set = new_open

        # print(*resource_types, file=sys.stderr)

    def on_map(self, x, y):
        return x >= 0 and y >= 0 and x < self.map.width and y < self.map.height

    def can_move(self, x, y):
        return self.on_map(x, y) and self.is_open[y][x]

    def sorted_mine_moves(self, unit):
        x, y = unit.pos.x, unit.pos.y
        p = self.ps[unit.type]
        ps = [p[y][x]]
        dirs = [Constants.DIRECTIONS.CENTER]
        for dx, dy in DELTA_NEIGHBORS:
            new_x, new_y = x + dx, y + dy
            if self.can_move(new_x, new_y):
                ps.append(p[new_y][new_x])
                dirs.append(DIRECTION_FROM_DELTA[(dx, dy)])
        return [d for _, d in sorted(zip(ps, dirs))]

    def mine_move(self, unit):
        x, y = unit.pos.x, unit.pos.y
        p = self.ps[unit.type]
        best_p = p[y][x]
        best_dir = Constants.DIRECTIONS.CENTER
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self.can_move(new_x, new_y) and p[new_y][new_x] > best_p:
                best_p = p[new_y][new_x]
                best_dir = DIRECTION_FROM_DELTA[(dx, dy)]
        return best_dir

    def sorted_city_moves(self, unit):
        x, y = unit.pos.x, unit.pos.y
        dirs = [Constants.DIRECTIONS.CENTER]
        ds = [self.city_moves[y][x]]
        if not self.can_move(x, y):
            ds[0] = np.inf
        for dx, dy in DELTA_NEIGHBORS:
            new_x, new_y = x + dx, y + dy
            if self.can_move(new_x, new_y) and self.city_moves[new_y][new_x] < ds[0]:
                ds.append(self.city_moves[new_y][new_x])
                dirs.append(DIRECTION_FROM_DELTA[(dx, dy)])
        return [d for _, d in sorted(zip(ds, dirs))]

    def city_move(self, unit):
        return self.sorted_city_moves(unit)[0]

    def move(self, unit, how="mine"):
        if how == "mine":
            move_dir = self.mine_move(unit)
        elif how == "city":
            move_dir = self.city_move(unit)
        self.update_board(unit, move_dir)
        return unit.move(move_dir)

    def update_board(self, unit, move):
        dx, dy = DELTA_FROM_DIRECTION[move]
        if not (unit.pos.x + dx, unit.pos.y + dy) in self.city_locs:
            self.is_open[unit.pos.y + dy][unit.pos.x + dx] = False
