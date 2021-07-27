import numpy as np

import mining
import cluster
import bfs
from lux.misc import *
from lux.game_map import Position


class Mover(object):
    def __init__(self):
        self.miner = mining.Miner()
        self.cluster = cluster.Cluster()

    def update(self, game, player):
        self.map = game.map
        self.w, self.h = self.map.width, self.map.height
        self.miner.update(self.map, player)
        self.open = np.ones((self.h, self.w), dtype="bool")
        self.city_locs = set()
        for city in player.cities.values():
            self.city_locs |= set(
                map(lambda c: (c.pos.x, c.pos.y), city.citytiles))

        self.cluster.update(self.map, player, self.city_locs)

    def on_map(self, x, y):
        return x >= 0 and y >= 0 and x < self.w and y < self.h

    def passable(self, x, y):
        return self.on_map(x, y) and self.open[y][x]

    def can_move(self, unit, dir):
        dx, dy = DELTA_FROM_DIRECTION[dir]
        return self.passable(unit.pos.x + dx, unit.pos.y + dy)

    def update_board(self, unit, dir):
        x, y = unit.pos.x, unit.pos.y
        dx, dy = DELTA_FROM_DIRECTION[dir]
        if not (x + dx, y + dy) in self.city_locs:
            self.open[y + dy][x + dx] = False

    # This function isn't big enough to warrant its own class yet.
    def get_build_dir(self, unit):
        x, y = unit.pos.x, unit.pos.y

        def is_empty(x, y):
            return self.map.get_cell(x, y).is_empty()

        def no_cities(x, y):
            return not (x, y) in self.city_locs

        build_locs = bfs.search(is_empty, self.w, self.h, [(x, y)], no_cities)
        if len(build_locs) == 0:
            build_locs = bfs.search(is_empty, self.w, self.h, [(x, y)])

        def potential(pos): return self.miner.ps[0][pos[1]][pos[0]]
        loc = max(build_locs, key=potential)

        for dir in unit.pos.direction_to(Position(*loc)):
            if self.can_move(unit, dir):
                break
        return dir

    def move(self, unit, type="mine"):
        x, y = unit.pos.x, unit.pos.y

        if type == "mine":
            dir = self.miner.dir(
                x, y, passable=self.passable, unit_type=unit.type)
        elif type == "build":
            dir = self.get_build_dir(unit)
        elif type == "city":
            dir = self.cluster.dir(x, y, passable=self.passable)

        self.update_board(unit, dir)
        return unit.move(dir)
