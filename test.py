from terrain import Terrain
from terrain.terrain import Layer


terr = Terrain((2000, 2000), 16, 0, None)
terr.add_layer(Layer(123, 1000, 200))

print(terr.get_pixel(0, 0))

print(terr.get_trees(0, 0, 100, 100))
