import random

from terrain.material import Material
from terrain.biomes.util import get_cells_intersecting
from terrain.tree import Oak, Palm, Redwood


def get_positions(x0, y0, x1, y1, grid_size):
    random.seed((x0 << 16) + (y0 << 8) + grid_size)

    positions = []

    for cell in get_cells_intersecting(grid_size, x0, y0, x1, y1):
        tx = cell[0] * grid_size + random.randrange(grid_size)
        ty = cell[1] * grid_size + random.randrange(grid_size)

        if x0 < tx < x1 and y0 < ty < y1:
            positions.append((tx, ty))

    return positions


class Biome(object):
    def __init__(self):
        self.trees = []

    def add_tree(self, tree):
        self.trees.append(tree)

    def material_at(self, cell, slope):
        return Material.Grass

    def __call__(self, x0, y0, x1, y1):
        return self.trees


class Beach(Biome):
    def material_at(self, cell, slope):
        return Material.Sand if slope <= 0.8 else Material.Sandstone

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 48):
            self.add_tree(Palm(x, y))

        return self.trees


class Grassland(Biome):
    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.93 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 86):
            self.add_tree(Oak(x, y))

        return self.trees


class TemperateDeciduousForest(Biome):
    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.93 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 42):
            self.add_tree(Oak(x, y))

        return self.trees


class TemperateRainForest(Biome):
    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.85 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 34):
            self.add_tree(Oak(x, y))

        return self.trees


class TropicalRainForest(Biome):
    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.7 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 22):
            self.add_tree(Oak(x, y))

        return self.trees


class SeasonalForest(Biome):
    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.9 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 64):
            self.add_tree(Oak(x, y))

        return self.trees


class SubtropicalDesert(Biome):
    def material_at(self, cell, slope):
        return Material.Sand if slope <= 0.75 else Material.Sandstone

    def __call__(self, x0, y0, x1, y1):
        return self.trees


class TemperateDesert(Biome):
    def material_at(self, cell, slope):
        return Material.Sand if slope <= 0.75 else Material.Sandstone

    def __call__(self, x0, y0, x1, y1):
        return self.trees


class Shrubland(Biome):
    def material_at(self, cell, slope):
        if slope <= 0.8:
            return Material.Grass
        elif slope < 1:
            return Material.Ground
        else:
            return Material.Rock

    def __call__(self, x0, y0, x1, y1):
        return self.trees


class Taiga(Biome):
    def material_at(self, cell, slope):
        return Material.Grass if slope <= 1 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 36):
            self.add_tree(Redwood(x, y))

        return self.trees


class Snow(Biome):
    def material_at(self, cell, slope):
        return Material.Snow if slope <= 0.7 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        return self.trees


class Bare(Biome):
    def material_at(self, cell, slope):
        return Material.Ground if slope < 0.7 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        return self.trees
