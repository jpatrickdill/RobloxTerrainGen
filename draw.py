import math

from PIL import Image

from terrain import Terrain
from terrain.modifiers import circle_island


def octaves(seed, scale, height, octs):
    layers = []

    for o in range(octs):
        layers.append({
            "seed": seed,
            "scale": scale / (2 ** o),
            "height": math.ceil(height / (2 ** o))
        })

    return layers


config = {
    "layers": octaves(6969, 750, 300, 12),

    "dimensions": [5000, 5000],
    "water_level": 6

}

terr = Terrain.from_config(config)
terr.add_modifier(circle_island(0.3, 1))

img = Image.new("RGB", (500, 500))

pix = img.load()

for x in range(0, 500):
    for y in range(0, 500):
        alt = terr.get_pixel(x * 10 - 2500, y * 10 - 2500).height

        if alt <= terr.water_level:
            pix[x, y] = (0, 100, 255)

        else:
            pix[x, y] = (int((alt / terr.max_height) * 255),) * 3

    if x % 100 == 0:
        print(x)

img.save("heightmap.jpg")
