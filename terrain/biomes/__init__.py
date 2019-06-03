import random
import math

from terrain.material import Material
from terrain.biomes.util import get_cells_intersecting
from terrain.tree import *


def dist(x0, y0, x1, y1):
    return math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def get_positions(x0, y0, x1, y1, grid_size, offset=None):
    random.seed((x0 << 16) + (y0 << 8) + grid_size + hash(offset or 0))

    positions = []

    for cell in get_cells_intersecting(grid_size, x0, y0, x1, y1):
        tx = cell[0] * grid_size + random.randrange(grid_size)
        ty = cell[1] * grid_size + random.randrange(grid_size)

        if x0 < tx < x1 and y0 < ty < y1:
            positions.append((tx, ty))

    return positions


class Biome(object):
    Name = "Biome"

    def __init__(self):
        self.trees = []

    def add_tree(self, tree):
        # check if tree is too close to any other trees
        for tree2 in self.trees:
            if dist(tree.x, tree.y, tree2.x, tree2.y) < (tree.diameter + tree2.diameter) / 2:
                return False

        self.trees.append(tree)

        return True

    def material_at(self, cell, slope):
        return Material.Grass

    def __call__(self, x0, y0, x1, y1):
        return self.trees


class Beach(Biome):
    Name = "Beach"

    def material_at(self, cell, slope):
        return Material.Sand if slope <= 0.8 else Material.Sandstone

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 48, "palms"):
            self.add_tree(Palm(x, y))

        return self.trees


class Grassland(Biome):
    Name = "Grassland"

    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.93 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 86, "oaks"):
            self.add_tree(Oak(x, y))

        for (x, y) in get_positions(x0, y0, x1, y1, 84, "palms"):
            self.add_tree(Palm(x, y))

        return self.trees


class TemperateDeciduousForest(Biome):
    Name = "Temp Decid Forest"

    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.93 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 82*0.6, "maples"):
            self.add_tree(Maple(x, y))

        for (x, y) in get_positions(x0, y0, x1, y1, 60*0.6, "aspens"):
            self.add_tree(QuakingAspen(x, y))

        for (x, y) in get_positions(x0, y0, x1, y1, 52*0.6, "sycamores"):
            self.add_tree(Sycamore(x, y))

        for (x, y) in get_positions(x0, y0, x1, y1, 36*0.6, "oaks"):
            self.add_tree(Oak(x, y))

        return self.trees


class TemperateRainForest(Biome):
    Name = "Temp Rain Forest"

    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.85 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 68, "coastaldouglasfirs"):
            self.add_tree(CoastalDouglasFir(x, y))

        for (x, y) in get_positions(x0, y0, x1, y1, 35, "northernconifer"):
            self.add_tree(NorthernConifer(x, y))

        for (x, y) in get_positions(x0, y0, x1, y1, 35, "vinemaples"):
            self.add_tree(VineMaple(x, y))

        for (x, y) in get_positions(x0, y0, x1, y1, 60, "oaks"):
            self.add_tree(Oak(x, y))

        return self.trees


class TropicalRainForest(Biome):
    Name = "Trop Rain Forest"

    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.7 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 22, "oaks"):
            self.add_tree(Oak(x, y))

        return self.trees


class SeasonalForest(Biome):
    Name = "Seasonal Forest"

    def material_at(self, cell, slope):
        return Material.Grass if slope <= 0.9 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 52, "oaks"):
            self.add_tree(Oak(x, y))

        return self.trees


class SubtropicalDesert(Biome):
    Name = "Subtrop Desert"

    def material_at(self, cell, slope):
        return Material.Sand if slope <= 0.75 else Material.Sandstone

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 48, "cacti"):
            self.add_tree(Cactus(x, y))

        return self.trees


class TemperateDesert(Biome):
    Name = "Temp Desert"

    def material_at(self, cell, slope):
        return Material.Sand if slope <= 0.75 else Material.Sandstone

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 28, "cacti"):
            self.add_tree(Cactus(x, y))

        return self.trees


class Shrubland(Biome):
    Name = "Shrubland"

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
    Name = "Taiga"

    def material_at(self, cell, slope):
        return Material.Grass if slope <= 1 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 28, "pines"):
            self.add_tree(Pine(x, y))

        return self.trees


class Snow(Biome):
    Name = "Snow"

    def material_at(self, cell, slope):
        return Material.Snow if slope <= 0.7 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        for (x, y) in get_positions(x0, y0, x1, y1, 64, "pines"):
            self.add_tree(Pine(x, y))

        return self.trees


class Bare(Biome):
    Name = "Bare"

    def material_at(self, cell, slope):
        return Material.Ground if slope < 0.7 else Material.Rock

    def __call__(self, x0, y0, x1, y1):
        return self.trees
