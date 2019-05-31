from flask import Blueprint, request, jsonify
import sys
import json

sys.path.append("./../../")

from terrain import Terrain
from terrain.modifiers import circle_island

terrain_bp = Blueprint("terrain", __name__)


@terrain_bp.route("/chunk")
def get_chunk():
    config = json.loads(request.args["config"])

    x0, y0 = int(request.args["x0"]), int(request.args["y0"])
    x1, y1 = int(request.args["x1"]), int(request.args["y1"])

    terr = Terrain.from_config(config)
    terr.add_modifier(circle_island())

    chunk = terr.get_chunk(x0, y0, x1, y1)

    json_chunk = []

    for row in chunk:
        n_row = []

        for cell in row:
            n_row.append(cell.json())

        json_chunk.append(n_row)

    trees = terr.get_trees(x0, y0, x1, y1)

    print(trees)

    return jsonify({
        "height": terr.max_height,
        "water_level": terr.water_level,
        "chunk": json_chunk,
        "trees": [tree.json(terr.get_pixel(tree.x, tree.y)) for tree in trees]
    })
