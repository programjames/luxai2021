import numpy as np
from lux.misc import *


class BFS(object):
    def __init__(self, width, height, starting_locs, passable=None):
        if passable is None:
            def passable(x, y): return True
        self.width, self.height = width, height
        self.dists = np.full((self.height, self.width), np.inf)
        for x, y in starting_locs:
            self.dists[y][x] = 0

        open_set = set(starting_locs)
        closed_set = open_set.copy()

        d = 0
        while len(open_set) > 0:
            d += 1
            new_open = set()
            for x, y in open_set:
                for dx, dy in DELTA_NEIGHBORS:
                    new_x, new_y = x + dx, y + dy
                    if not self.on_map(new_x, new_y) or (new_x, new_y) in closed_set:
                        continue
                    if not passable(new_x, new_y):
                        continue

                    new_open.add((new_x, new_y))
                    closed_set.add((new_x, new_y))
                    self.dists[new_y][new_x] = d
            open_set = new_open

    def on_map(self, x, y):
        return x >= 0 and y >= 0 and x < self.width and y < self.height

    def distance(self, x, y):
        return self.dists[y][x]

    def sorted_dirs(self, x, y, can_stay=True, passable=None):
        if passable is None:
            def passable(x, y): return True

        if can_stay:
            dirs = [Constants.DIRECTIONS.CENTER]
            ds = [self.dists[y][x]]
            if not passable(x, y):
                ds[0] = np.inf
        else:
            dirs = []
            ds = []

        for dx, dy in DELTA_NEIGHBORS:
            new_x, new_y = x + dx, y + dy
            if passable(new_x, new_y):
                ds.append(self.dists[new_y][new_x])
                dirs.append(DIRECTION_FROM_DELTA[(dx, dy)])
        return [dir for _, dir in sorted(zip(ds, dirs))]

    def dir(self, x, y, can_stay=True, passable=None):
        return self.sorted_dirs(x, y, can_stay, passable)[0]


def search(found_criterion, width, height, starting_locs, passable=None):
    if passable is None:
        def passable(x, y): return True

    def on_map(x, y):
        return x >= 0 and y >= 0 and x < width and y < height

    found_set = set()
    for x, y in starting_locs:
        if found_criterion(x, y):
            found_set.add((x, y))

    open_set = set(starting_locs)
    closed_set = open_set.copy()

    while len(open_set) > 0 and len(found_set) == 0:
        new_open = set()
        for x, y in open_set:
            for dx, dy in DELTA_NEIGHBORS:
                new_x, new_y = x + dx, y + dy
                if not on_map(new_x, new_y) or (new_x, new_y) in closed_set:
                    continue

                if found_criterion(new_x, new_y):
                    found_set.add((new_x, new_y))

                if not passable(new_x, new_y):
                    continue

                new_open.add((new_x, new_y))
                closed_set.add((new_x, new_y))
        open_set = new_open

    return found_set
