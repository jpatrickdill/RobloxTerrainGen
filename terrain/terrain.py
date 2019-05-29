import math
from enum import Enum

from opensimplex import OpenSimplex


class Material(Enum):
    Plastic = 256
    Wood = 512
    Slate = 800
    Concrete = 816
    CorrodedMetal = 1040
    DiamondPlate = 1056
    Foil = 1072
    Grass = 1280
    Ice = 1536
    Marble = 784
    Granite = 832
    Brick = 848
    Pebble = 864
    Sand = 1296
    Fabric = 1312
    SmoothPlastic = 272
    Metal = 1088
    WoodPlanks = 528
    Cobblestone = 880
    Air = 1792
    Water = 2048
    Rock = 896
    Glacier = 1552
    Snow = 1328
    Sandstone = 912
    Mud = 1344
    Basalt = 788
    Ground = 1360
    CrackedLava = 804
    Neon = 288
    Glass = 1568
    Asphalt = 1376
    LeafyGrass = 1284
    Salt = 1392
    Limestone = 820
    Pavement = 836
    ForceField = 1584


class Cell(object):
    def __init__(self, height, material, moisture=1):
        self.height = height

        self.material = material
        self.moisture = moisture

    def __repr__(self):
        return "Cell({}, {}, moisture={})".format(self.height, self.material.name, self.moisture)

    def json(self, max_height=None):
        return [self.height / max_height if max_height else self.height, self.material.value]


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

        slope = math.sqrt((nx-height) ** 2 + (ny-height) ** 2)

        v = Cell(height / self.max_height, Material.Grass)
        for func in self.modifiers:
            v = func(v, (x, y), self.config)

        # convert back to height in m
        v.height = v.height * self.max_height

        altitude = v.height - self.water_level

        # determine material

        if altitude <= 6:  # beach
            mat = Material.Sand if slope <= 0.8 else Material.Sandstone
        elif 6 <= altitude <= self.max_height*0.6-14:  # grassy
            mat = Material.Grass if slope <= 1.125 else Material.Rock
        else:  # snow/mountain
            mat = Material.Snow if slope <= 0.63 else Material.Rock

        # initialize height as percentage for any modifier functions

        v.material = mat

        return v

    def get_chunk(self, x0, y0, x1, y1):
        rows = []

        for x in range(x0, x1):
            row = []
            for y in range(y0, y1):
                row.append(self.get_pixel(x, y))

            rows.append(row)

        return rows
