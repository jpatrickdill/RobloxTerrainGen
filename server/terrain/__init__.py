from flask import Blueprint, request, Response
import sys

from jsonrpcserver import method, dispatch

sys.path.append("./../../")

from terrain import Terrain
from terrain.modifiers import circle_island


@method
def gen_chunk(config, x0, y0, x1, y1):
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

    return {
        "height": terr.max_height,
        "water_level": terr.water_level,
        "chunk": json_chunk,
        "trees": [tree.json(terr.get_pixel(tree.x, tree.y)) for tree in trees]
    }


terrain_bp = Blueprint("terrain", __name__)


@terrain_bp.route("/", methods=["POST"])
def index():
    req = request.get_data().decode()

    response = dispatch(req, trim_log_values=True)  # why the fuck should i have to tell it to trim the log values if
                                                    # it knows it's gonna break

    return Response(str(response), response.http_status, mimetype="application/json")
