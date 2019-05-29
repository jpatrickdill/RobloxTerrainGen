from opensimplex import OpenSimplex
from enum import Enum


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

    def json(self):
        return [self.height, self.material.value]


class Terrain(object):
    def __init__(self, seed, dimensions, height, moisture_seed=None, modifier=None):
        self.seed = seed
        self.moisture_seed = moisture_seed or seed

        self.modifiers = [modifier] if modifier else []

        self.dimensions = dimensions
        self.height = height
        self.bounds = [(-dimensions[0] / 2, -dimensions[1] / 2), (dimensions[0] / 2, dimensions[1] / 2)]

        self.simplex = OpenSimplex(seed)

    @property
    def config(self):
        return {
            "seed": self.seed,
            "moisture_seed": self.moisture_seed,

            "height": self.height,
            "dimensions": self.dimensions,
            "bounds": self.bounds
        }

    def add_modifier(self, func):
        self.modifiers.append(func)

    def get_pixel(self, x, y):
        v = Cell((self.simplex.noise2d(x / 150, y / 150) + 1) / 2, Material.Ground)

        for func in self.modifiers:
            v = func(v, (x, y), self.config)

        return v

    def get_chunk(self, x0, y0, x1, y1):
        rows = []

        for x in range(x0, x1):
            row = []
            for y in range(y0, y1):
                row.append(self.get_pixel(x, y))

            rows.append(row)

        return rows



