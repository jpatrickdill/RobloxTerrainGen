class Tree(object):
    type_ = ""

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


class Oak(Tree):
    type_ = "Oak"


class Redwood(Tree):
    type_ = "Pine"
