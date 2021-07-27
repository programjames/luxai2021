import math
import sys
import numpy as np

import moving
from lux.misc import *
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES, Position
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate

game_state = None

mover = moving.Mover()


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

    # Update stuff
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height
    turn = game_state.turn

    mover.update(game_state, player)

    # Build/research at citytiles
    num_units = len(player.units)
    num_citytiles = sum(len(city.citytiles) for city in player.cities.values())

    for city in player.cities.values():
        for citytile in city.citytiles:
            if citytile.can_act():
                if num_units < num_citytiles:
                    actions.append(citytile.build_worker())
                else:
                    actions.append(citytile.research())

    # Move units
    for unit in player.units:
        if not unit.can_act():
            mover.update_board(unit, DIRECTIONS.CENTER)

    def should_go_to_city(unit):
        if mover.cluster.bfs.distance(unit.pos.x, unit.pos.y) > 3:
            return False
        return turns_till_night(turn) < 5 or (turns_till_day(turn) > 0 and unit.get_fuel() == 0)

    workers = set(u for u in player.units if u.can_act())  # and u.is_worker())
    for unit in workers:
        if should_go_to_city(unit):
            actions.append(mover.move(unit, "city"))
        elif is_day(turn) and unit.has_build_wood():
            if unit.can_build(game_state.map):
                mover.update_board(unit, DIRECTIONS.CENTER)
                actions.append(unit.build_city())
            else:
                actions.append(mover.move(unit, "build"))
        else:
            actions.append(mover.move(unit, "mine"))

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))

    return actions
