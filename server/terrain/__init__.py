from flask import Blueprint, request, jsonify
import sys

sys.path.append("./../../")

from terrain import Terrain
from terrain.modifiers import circle_island

terrain_bp = Blueprint("terrain", __name__)


@terrain_bp.route("/chunk")
def get_chunk():
    seed = int(request.args["seed"])
    x0 = int(request.args["x0"])
    y0 = int(request.args["y0"])
    x1 = int(request.args["x1"])
    y1 = int(request.args["y1"])

    terr = Terrain(seed, (2000, 2000), 256, modifier=circle_island())

    chunk = terr.get_chunk(x0, y0, x1, y1)

    json_chunk = []

    for row in chunk:
        n_row = []

        for cell in row:
            n_row.append(cell.json())

        json_chunk.append(n_row)

    return jsonify(json_chunk)
