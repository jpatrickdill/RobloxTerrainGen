from terrain import Terrain
from terrain.modifiers import circle_island

from PIL import Image

seed = 1

terr = Terrain(seed, (2000, 2000), 256, modifier=circle_island())

img = Image.new("RGB", (500, 500))

pix = img.load()

for x in range(0, 500):
    for y in range(0, 500):
        alt = terr.get_pixel(x*4-1000, y*4-1000).height

        pix[x, y] = (int(alt*255),)*3

    if x%100 == 0:
        print(x)

img.save("heightmap.jpg")
