def get_new_coordinates(coordinates, vertical, width, height, axis='x', reverse=False):
    if reverse:
        return coordinates[::-1]
    if axis == 'x':
        if vertical:
            return coordinates[0], width - 2 - coordinates[1]
        else:
            return coordinates[0], width - 1 - coordinates[1]
    else:
        if vertical:
            return height - 1 - coordinates[0], coordinates[1]
        else:
            return height - 2 - coordinates[0], coordinates[1]


def get_opposite_direction(direction):
    return direction + 2 if direction < 1 else direction - 2
