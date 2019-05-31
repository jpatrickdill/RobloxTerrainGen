import math

from opensimplex import OpenSimplex

from terrain.material import Material
from terrain.biomes import (Beach, Grassland, TemperateDeciduousForest, TemperateRainForest, TropicalRainForest,
                            SeasonalForest, Snow, Bare, Taiga, Shrubland, SubtropicalDesert, TemperateDesert)
from PIL import Image

Biomes = (Beach, Grassland, TemperateDeciduousForest, TemperateRainForest, TropicalRainForest,
          SeasonalForest, Snow, Bare, Taiga, Shrubland, SubtropicalDesert, TemperateDesert)

BiomeMap = {
    (241, 216, 169): Beach,
    (248, 211, 126): SubtropicalDesert,
    (251, 227, 174): TemperateDesert,
    (224, 251, 174): Grassland,
    (193, 243, 190): SeasonalForest,
    (23, 125, 54): TropicalRainForest,
    (136, 225, 111): TemperateDeciduousForest,
    (30, 164, 70): TemperateRainForest,
    (180, 197, 167): Shrubland,
    (148, 198, 142): Taiga,
    (195, 195, 195): Bare,
    (255, 255, 255): Snow
}

BiomeImg = Image.open("./terrain/biomes/biomes.png")
BiomeImgPix = BiomeImg.load()


def get_biome(cell):
    x = int(cell.moisture * 254)
    y = 399 - int(max(0, min(cell.height, 399)))

    return BiomeMap[BiomeImgPix[x, y]]


class Cell(object):
    def __init__(self, height, pos, material, moisture=1):
        self.height = height
        self.position = pos

        self.material = material
        self.moisture = moisture

    @property
    def biome(self):
        return get_biome(self)

    def __repr__(self):
        return "Cell({}, {}, moisture={}, biome={})".format(self.height, self.material.name, self.moisture,
                                                            self.biome.__name__)

    def json(self, max_height=None):
        return [self.height / max_height if max_height else self.height, self.material.value,
                self.biome.__name__, self.moisture, self.position[0], self.position[1]]


class Layer(object):
    def __init__(self, seed, scale, height):
        self.seed = seed
        self.scale = scale
        self.height = height

        self.simplex = OpenSimplex(seed)

    def get_pixel(self, x, y):
        alt = (self.simplex.noise2d(x / self.scale, y / self.scale) + 1) / 2 * self.height

        return alt

    def json(self):
        return {
            "seed": self.seed,
            "scale": self.scale,
            "height": self.height
        }


class Terrain(object):
    def __init__(self, dimensions, water_level=None, moisture_seed=None, modifier=None):
        self.layers = []
        self.moisture_seed = moisture_seed or 0

        self.moisture_noise = Layer(self.moisture_seed, dimensions[0]/3, 1)

        self.max_height = 0
        self.water_level = water_level or 0

        self.modifiers = [modifier] if modifier else []

        self.dimensions = dimensions
        self.bounds = [(-dimensions[0] / 2, -dimensions[1] / 2), (dimensions[0] / 2, dimensions[1] / 2)]

    def add_layer(self, layer):
        self.layers.append(layer)

        max_height = 0
        for layer in self.layers:
            max_height += layer.height

        self.max_height = max_height

    @classmethod
    def from_config(cls, config):
        t = Terrain(config.get("dimensions", (1000, 1000)),
                    water_level=config.get("water_level"), moisture_seed=config.get("moisture_seed"))

        for layer in config["layers"]:
            t.add_layer(Layer(layer["seed"], layer["scale"], layer["height"]))

        return t

    @property
    def config(self):
        return {
            "layers": [layer.json() for layer in self.layers],
            "moisture_seed": self.moisture_seed,

            "height": self.max_height,
            "water_level": self.water_level,

            "dimensions": self.dimensions,
            "bounds": self.bounds
        }

    def add_modifier(self, func):
        self.modifiers.append(func)

    def get_pixel(self, x, y):
        height = sum([layer.get_pixel(x, y) for layer in self.layers])

        nx = sum([layer.get_pixel(x + 1, y) for layer in self.layers])
        ny = sum([layer.get_pixel(x, y + 1) for layer in self.layers])

        slope = math.sqrt((nx - height) ** 2 + (ny - height) ** 2)

        v = Cell(height / self.max_height, (x, y), Material.Grass, moisture=self.moisture_noise.get_pixel(x, y))
        for func in self.modifiers:
            v = func(v, (x, y), self.config)

        # convert back to height in m
        v.height = v.height * self.max_height

        biome = v.biome()

        v.material = biome.material_at(v, slope)

        return v

    def get_chunk(self, x0, y0, x1, y1):
        rows = []

        for x in range(x0, x1):
            row = []
            for y in range(y0, y1):
                row.append(self.get_pixel(x, y))

            rows.append(row)

        return rows

    def get_trees(self, x0, y0, x1, y1):
        trees = []

        # get trees from each biome type

        for biome_cls in Biomes:
            biome = biome_cls()
            for tree in biome(x0, y0, x1, y1):
                if self.get_pixel(tree.x, tree.y).biome == biome_cls:
                    trees.append(tree)

        i = 0
        while i < len(trees):
            tree = trees[i]

            if tree.valid(self.get_pixel(tree.x, tree.y)):
                i += 1
            else:
                del trees[i]

        return trees
