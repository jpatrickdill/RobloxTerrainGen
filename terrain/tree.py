class Tree(object):
    type_ = ""
    diameter = 10 / 4

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.seed = (x << 16) + y

    def valid(self, cell):
        return True if cell.height > 12 else False

    def json(self, cell):
        return {
            "seed": self.seed,
            "class": self.type_,
            "pos": [self.x, cell.height, self.y]
        }

    def __repr__(self):
        return "Tree({}, {}, {})".format(self.x, self.y, self.type_)


class Palm(Tree):
    type_ = "Palm"
    diameter = 30 / 4


class QuakingAspen(Tree):
    type_ = "QuakingAspen"
    diameter = 30 / 4


class Oak(Tree):
    type_ = "Oak"
    diameter = 75 / 4


class Sycamore(Tree):
    type_ = "AmericanSycamore"
    diameter = 60 / 4


class Maple(Tree):
    type_ = "Maple"
    diameter = 60 / 4


class VineMaple(Tree):
    type_ = "VineMaple"
    diameter = 67 / 4


class Redwood(Tree):
    type_ = "Redwood"
    diameter = 50 / 4


class CoastalDouglasFir(Tree):
    type_ = "CoastalDouglasFir"
    diameter = 50 / 4


class NorthernConifer(Tree):
    type_ = "NorthernConifer"
    diameter = 60 / 4


class Pine(Tree):
    type_ = "Pine"
    diameter = 50 / 4


class Cactus(Tree):
    type_ = "Cactus"
    diameter = 6 / 4
