import math
from typing import List

from .constants import Constants

from lux.misc import NEIGHBORS
DIRECTIONS = Constants.DIRECTIONS
RESOURCE_TYPES = Constants.RESOURCE_TYPES


class Resource:
    def __init__(self, r_type: str, amount: int):
        self.type = r_type
        self.amount = amount


class Cell:
    def __init__(self, x, y):
        self.pos = Position(x, y)
        self.resource: Resource = None
        self.citytile = None
        self.road = 0

    def has_resource(self):
        return self.resource is not None and self.resource.amount > 0

    def is_empty(self):
        return not self.has_resource() and self.citytile is None


class GameMap:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.map: List[List[Cell]] = [None] * height
        for y in range(0, self.height):
            self.map[y] = [None] * width
            for x in range(0, self.width):
                self.map[y][x] = Cell(x, y)

    def get_cell_by_pos(self, pos) -> Cell:
        return self.map[pos.y][pos.x]

    def get_cell(self, x, y) -> Cell:
        return self.map[y][x]

    def _setResource(self, r_type, x, y, amount):
        """
        do not use this function, this is for internal tracking of state
        """
        cell = self.get_cell(x, y)
        cell.resource = Resource(r_type, amount)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, pos) -> int:
        return abs(pos.x - self.x) + abs(pos.y - self.y)

    def distance_to(self, pos):
        """
        Returns Manhattan (L1/grid) distance to pos
        """
        return self - pos

    def is_adjacent(self, pos):
        return (self - pos) <= 1

    def __eq__(self, pos) -> bool:
        return self.x == pos.x and self.y == pos.y

    def equals(self, pos):
        return self == pos

    def translate(self, direction, units) -> 'Position':
        if direction == DIRECTIONS.NORTH:
            return Position(self.x, self.y - units)
        elif direction == DIRECTIONS.EAST:
            return Position(self.x + units, self.y)
        elif direction == DIRECTIONS.SOUTH:
            return Position(self.x, self.y + units)
        elif direction == DIRECTIONS.WEST:
            return Position(self.x - units, self.y)
        elif direction == DIRECTIONS.CENTER:
            return Position(self.x, self.y)

    def direction_to(self, target_pos: 'Position') -> DIRECTIONS:
        """
        Return closest position to target_pos from this position
        """
        dx = target_pos.x - self.x
        dy = target_pos.y - self.y
        if dx == dy == 0:
            return DIRECTIONS.CENTER
        if abs(dx) > abs(dy):
            if dx > 0:
                return DIRECTIONS.EAST
            else:
                return DIRECTIONS.WEST
        else:
            if dy > 0:
                return DIRECTIONS.SOUTH
            else:
                return DIRECTIONS.NORTH

    def directions_to(self, target_pos: 'Position'):
        dx = target_pos.x - self.x
        dy = target_pos.y - self.y
        if dx == dy == 0:
            return [DIRECTIONS.CENTER, *NEIGHBORS]

        if dx > 0:
            x_dirs = [DIRECTIONS.EAST, DIRECTIONS.WEST]
        else:
            x_dirs = [DIRECTIONS.WEST, DIRECTIONS.EAST]

        if dy > 0:
            y_dirs = [DIRECTIONS.SOUTH, DIRECTIONS.NORTH]
        else:
            y_dirs = [DIRECTIONS.NORTH, DIRECTIONS.SOUTH]

        if abs(dx) > abs(dy):
            return [x_dirs[0], y_dirs[0], y_dirs[1], x_dirs[1]]
        else:
            return [y_dirs[0], x_dirs[0], x_dirs[1], y_dirs[1]]

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
