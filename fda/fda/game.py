def prepare_scores(game_map, resource_type=None):
    rate = GAME_CONSTANTS["RESOURCE_TO_FUEL_RATE"][resource_type]
    nx, ny = game_map.width, game_map.height
    scores = np.zeros((nx, ny))
    for x in range(nx):
        for y in range(ny):
            c = game_map.get_cell(x, y)
            if c.has_resource():
                if resource_type != None and c.resource.type != resource_type:
                    continue
                scores[y][x] = rate * c.resource.amount
    return scores


def prepare_resistances(game_map, unit_type, daytime=True):
    def res(road):
        r = GAME_CONSTANTS["UNIT_ACTION_COOLDOWN"][unit_type]
        if daytime is False:
            r *= 2
        r -= road
        r = max(r, 1)
        return 1 / r

    nx, ny = game_map.width, game_map.height
    resistances = np.zeros(game_map.width, game_map.height)
    for x in range(nx):
        for y in range(ny):
            resistances[y][x] = res(game_map.get_cell(x, y).road)

    return resistances
