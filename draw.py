import math

from PIL import Image

from terrain import Terrain, Material
from terrain.modifiers import circle_island

import threading

COLORS = {
    Material.Grass: (86, 125, 70),
    Material.Mud: (144, 108, 63),
    Material.Rock: (128, 132, 125),
    Material.Sand: (237, 201, 175),
    Material.Sandstone: (224, 160, 114),
    Material.Snow: (240, 240, 240)
}


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

img = Image.new("RGB", (250, 250))

pix = img.load()


def fill_column(x0, x1):
    for x in range(x0, x1):
        for y in range(0, 250):
            cell = terr.get_pixel(x * 10 - 2500, y * 10 - 2500)
            alt = cell.height

            if alt <= terr.water_level:
                pix[x, y] = (0, 100, 255)

            else:
                pix[x, y] = COLORS.get(cell.material, COLORS[Material.Grass])

    print("done")


threads = []

for x in range(0, 250, 10):
    th = threading.Thread(target=fill_column, args=(x, x + 10))
    th.start()

    threads.append(th)

    print(x)

for t in threads:
    t.join()

img.save("heightmap.png")
