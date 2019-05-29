from terrain import Terrain
from terrain.modifiers import circle_island

from PIL import Image

seed = 1

config = {
    "layers": [
        {
            "seed": 1,
            "scale": 500,
            "height": 350
        },
        {
            "seed": 34,
            "scale": 100,
            "height": 70
        },
        {
            "seed": 66,
            "scale": 33,
            "height": 10
        }
    ],

    "dimensions": [2000, 2000],

}

terr = Terrain.from_config(config)
terr.add_modifier(circle_island())

img = Image.new("RGB", (500, 500))

pix = img.load()

for x in range(0, 500):
    for y in range(0, 500):
        alt = terr.get_pixel(x * 4 - 1000, y * 4 - 1000).height

        pix[x, y] = (int((alt / terr.max_height) * 255),) * 3

    if x % 100 == 0:
        print(x)

img.save("heightmap.jpg")
