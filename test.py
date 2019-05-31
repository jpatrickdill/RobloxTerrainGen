from terrain import Terrain
from terrain.terrain import Layer


terr = Terrain((5000, 5000), 16, 0, None)
terr.add_layer(Layer(123, 1000, 600))

print(terr.get_pixel(500, 300))

print(terr.get_trees(0, 0, 100, 100))
