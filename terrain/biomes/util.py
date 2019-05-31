import math


def get_cells_intersecting(grid_size, x0, y0, x1, y1):
    lower = (int(math.floor(x0 / grid_size)), int(math.floor(y0 / grid_size)))
    upper = (int(math.ceil(x1 / grid_size)), int(math.ceil(y1 / grid_size)))

    cells = []

    for x in range(lower[0], upper[0] + 1):
        for y in range(lower[1], upper[1] + 1):
            cells.append((x, y))

    return cells
