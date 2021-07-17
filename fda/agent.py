import math
import sys
import numpy as np
import pathing

if __package__ == "":
    # not sure how to fix this atm
    from lux.game import Game
    from lux.game_map import Cell, RESOURCE_TYPES
    from lux.constants import Constants
    from lux.game_constants import GAME_CONSTANTS
    from lux import annotate
else:
    from .lux.game import Game
    from .lux.game_map import Cell, RESOURCE_TYPES
    from .lux.constants import Constants
    from .lux.game_constants import GAME_CONSTANTS
    from .lux import annotate

DIRECTIONS = Constants.DIRECTIONS
neighbors = [DIRECTIONS.NORTH, DIRECTIONS.EAST,
             DIRECTIONS.SOUTH, DIRECTIONS.WEST]
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

    num_units = len(player.units)
    num_citytiles = sum(len(city.citytiles) for city in player.cities.values())

    cities_to_build = 0
    for k, city in player.cities.items():
        city.cities_to_build = 0
        if (city.fuel > city.get_light_upkeep() * GAME_CONSTANTS["PARAMETERS"]["NIGHT_LENGTH"] + 100):
            # if our city has enough fuel to survive the whole night and 1000 extra fuel, lets increment citiesToBuild and let our workers know we have room for more city tiles
            city.cities_to_build += 1
        for citytile in city.citytiles:
            if citytile.can_act():
                if num_units < num_citytiles:
                    actions.append(citytile.build_worker())
                else:
                    actions.append(citytile.research())

    # we iterate over all our units and do something with them
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            if unit.get_cargo_space_left() > GAME_CONSTANTS["PARAMETERS"]["RESOURCE_CAPACITY"]["WORKER"] * 0.1:
                # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
                best_move = pather.best_move(unit)
                pather.update_board(unit, best_move)
                if best_move != DIRECTIONS.CENTER:
                    actions.append(unit.move(best_move))
            else:
                # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
                if len(player.cities) > 0:
                    closest_dist = math.inf
                    closest_city_tile = None
                    for k, city in player.cities.items():
                        for city_tile in city.citytiles:
                            dist = city_tile.pos.distance_to(unit.pos)
                            if dist < closest_dist:
                                closest_dist = dist
                                closest_city_tile = city_tile
                    move_dir = unit.pos.direction_to(closest_city_tile.pos)
                    if unit.can_build(game_state.map) and closest_city_tile.city.cities_to_build > 0 and unit.pos.is_adjacent(closest_city_tile.pos):
                        actions.append(unit.build_city())
                    elif unit.cargo.wood == GAME_CONSTANTS["PARAMETERS"]["CITY_WOOD_COST"] and unit.pos.distance_to(closest_city_tile.pos) > 5:
                        if unit.can_build(game_state.map):
                            actions.append(unit.build_city())
                        else:
                            moves = pather.sorted_moves(unit)
                            if moves[0] == DIRECTIONS.CENTER:
                                best_move = moves[1]
                            else:
                                best_move = moves[0]
                            pather.update_board(unit, best_move)
                            actions.append(unit.move(best_move))
                    else:
                        pather.update_board(unit, move_dir)
                        actions.append(unit.move(move_dir))
                else:
                    if unit.can_build(game_state.map):
                        actions.append(unit.build_city())
                    else:
                        moves = pather.sorted_moves(unit)
                        if moves[0] == DIRECTIONS.CENTER:
                            best_move = moves[1]
                        else:
                            best_move = moves[0]
                        pather.update_board(unit, best_move)
                        actions.append(unit.move(best_move))

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))

    return actions
