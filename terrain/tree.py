import terrain


class Tree(object):
    type_ = ""

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.seed = (x << 16) + y

    def valid(self, cell):
        return True

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

    def valid(self, cell):
        if cell.material != terrain.Material.Sand:
            return False

        return True


class Oak(Tree):
    type_ = "Oak"

    def valid(self, cell):
        if cell.material != terrain.Material.Grass:
            return False

        return True


class Pine(Tree):
    type_ = "Pine"

    def valid(self, cell):
        if cell.material not in [terrain.Material.Snow, terrain.Material.Grass] or cell.height < 200:
            return False

        return True
