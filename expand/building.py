import numpy as np

from lux.misc import *
from lux.game_map import Position


# TODO: Doesn't move around to build if there are 0 cities.

class Builder(object):
    MAX_BUILD_DISTANCE = 3

    def __init__(self, cities, pather):
        self.pather = pather
        self.empty = np.zeros(
            (pather.map.height, pather.map.width), dtype="bool")
        for x in range(pather.map.width):
            for y in range(pather.map.height):
                self.empty[y][x] = pather.map.get_cell(x, y).is_empty()

        # Find all locations bordering a city.
        self.build_locs = set()
        self.city_set = set()
        for city in cities:
            for citytile in city.citytiles:
                self.city_set.add((citytile.pos.x, citytile.pos.y))
        for x, y in self.city_set:
            for dx, dy in DELTA_NEIGHBORS:
                new_x, new_y = x + dx, y + dy
                if not self.pather.on_map(new_x, new_y):
                    continue
                if (new_x, new_y) in self.city_set or not self.empty[new_y][new_x]:
                    continue
                self.build_locs.add((new_x, new_y))

        # Flood fill to make build_moves

        self.build_moves = [
            [0 for i in range(pather.map.width)] for j in range(pather.map.height)]

        open_set = self.build_locs
        closed_set = open_set.copy()
        d = 0
        while len(open_set) > 0:
            d += 1
            new_open = set()
            for x, y in open_set:
                for dx, dy in DELTA_NEIGHBORS:
                    new_x, new_y = x + dx, y + dy
                    if (new_x, new_y) in self.city_set:
                        self.build_moves[new_y][new_x] = np.inf
                    if not self.pather.on_map(new_x, new_y) or (new_x, new_y) in closed_set or (new_x, new_y) in self.city_set:
                        continue
                    new_open.add((new_x, new_y))
                    closed_set.add((new_x, new_y))
                    self.build_moves[new_y][new_x] = d
            open_set = new_open

    def on_build_loc(self, unit):
        x, y = unit.pos.x, unit.pos.y
        return self.build_moves[y][x] == 0

    def build_move(self, unit):
        x, y = unit.pos.x, unit.pos.y
        move_dir = Constants.DIRECTIONS.CENTER
        d = self.build_moves[y][x]
        if not self.pather.can_move(x, y):
            d = np.inf
        for dx, dy in DELTA_NEIGHBORS:
            new_x, new_y = x + dx, y + dy
            if self.pather.can_move(new_x, new_y) and self.build_moves[new_y][new_x] < d:
                d = self.build_moves[new_y][new_x]
                move_dir = DIRECTION_FROM_DELTA[(dx, dy)]
        return move_dir

    def move(self, unit):
        move_dir = self.build_move(unit)
        self.pather.update_board(unit, move_dir)
        return unit.move(move_dir)

    def build(self, unit):
        self.pather.update_board(unit, DIRECTIONS.CENTER)
        return unit.build_city()

    def closest_empty_tile(self, x, y, max_iters=None):
        if self.empty[y][x]:
            return (x, y)
        if max_iters is None:
            max_iters = -1
        # BFS search
        open_set = {(x, y)}
        closed_set = open_set.copy()
        empty_tiles = set()
        while len(open_set) > 0 and len(empty_tiles) == 0 and max_iters != 0:
            max_iters -= 1
            new_open = set()
            for x, y in open_set:
                for dx, dy in DELTA_NEIGHBORS:
                    new_x, new_y = x + dx, y + dy
                    if not self.pather.on_map(new_x, new_y):
                        continue
                    if (new_x, new_y) in closed_set:
                        continue
                    if self.empty[new_y][new_x]:
                        empty_tiles.add((new_x, new_y))
                    new_open.add((new_x, new_y))
                    closed_set.add((new_x, new_y))
            open_set = new_open

        if len(empty_tiles) == 0:
            return None

        # Spot with highest worker potential:
        def potential(p): return self.pather.ps[0][p[1]][p[0]]
        return max(empty_tiles, key=potential)

    def best_build_loc(self, x, y):
        if len(self.build_locs) == 0:
            return self.closest_empty_tile(x, y)

        def distance(p): return abs(x - p[0]) + abs(y - p[1])
        best_loc = max(self.build_locs, key=distance)
        if distance(best_loc) <= self.MAX_BUILD_DISTANCE:
            return best_loc

        loc = self.closest_empty_tile(x, y, self.MAX_BUILD_DISTANCE)
        if not loc is None:
            return loc
        return best_loc
