import math
import sys
import numpy as np

import pathing
import building

from lux.misc import *
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES, Position
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate

game_state = None


def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
    else:
        game_state._update(observation["updates"])

    actions = []

    ### AI Code goes down here! ###
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height

    pather = pathing.Pather(game_state, player)
    builder = building.Builder(player.cities.values(), pather)

    num_units = len(player.units)
    num_citytiles = sum(len(city.citytiles) for city in player.cities.values())

    cities_to_build = 0
    if num_citytiles == 0:
        cities_to_build = 1
    for k, city in player.cities.items():
        city.cities_to_build = 0
        if (city.fuel > city.get_light_upkeep() * GAME_CONSTANTS["PARAMETERS"]["NIGHT_LENGTH"] + 100):
            city.cities_to_build += 1
            cities_to_build += 1
        for citytile in city.citytiles:
            if citytile.can_act():
                if num_units < num_citytiles:
                    actions.append(citytile.build_worker())
                else:
                    actions.append(citytile.research())

    for unit in player.units:
        if not unit.can_act():
            pather.update_board(unit, DIRECTIONS.CENTER)

    workers = set(u for u in player.units if u.can_act() and u.is_worker())

    print(turns_till_day(game_state.turn), file=sys.stderr)

    def in_danger(unit):
        return not is_day(game_state.turn) and unit.get_fuel() < unit.get_light_upkeep() * turns_till_day(game_state.turn)

    def moving_to_city(unit):
        if in_danger(unit):
            return True
        return unit.get_cargo_space_left() < GAME_CONSTANTS["PARAMETERS"]["RESOURCE_CAPACITY"]["WORKER"] * 0.1

    remove_set = set()
    for unit in workers:
        if not in_danger(unit):
            continue
        remove_set.add(unit)
        actions.append(pather.move(unit, "city"))

    workers -= remove_set

    remove_set = set()
    for unit in workers:
        if not moving_to_city(unit):
            continue
        remove_set.add(unit)
        if cities_to_build > 0 and unit.cargo.wood >= GAME_CONSTANTS["PARAMETERS"]["CITY_WOOD_COST"]:
            # Build a city
            if builder.on_build_loc(unit):
                actions.append(builder.build(unit))
            else:
                actions.append(builder.move(unit))
        else:
            actions.append(pather.move(unit, "city"))

    workers -= remove_set

    remove_set = set()
    for unit in workers:
        remove_set.add(unit)
        actions.append(pather.move(unit, "mine"))
    workers -= remove_set

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))

    return actions
