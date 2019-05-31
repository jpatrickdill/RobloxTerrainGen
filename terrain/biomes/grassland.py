import random
from terrain.biomes.util import get_cells_intersecting
from terrain.tree import Oak

GRID_SIZE = 36  # square grid size


def get_trees(x0, y0, x1, y1):
    # return trees within bounds

    random.seed((x0 << 16) + y0)

    trees = []

    for cell in get_cells_intersecting(GRID_SIZE, x0, y0, x1, y1):
        tx = cell[0]*GRID_SIZE + random.randrange(GRID_SIZE)
        ty = cell[1]*GRID_SIZE + random.randrange(GRID_SIZE)
        t = Oak(tx, ty)

        if x0 < tx < x1 and y0 < ty < y1:
            trees.append(t)

    return trees
