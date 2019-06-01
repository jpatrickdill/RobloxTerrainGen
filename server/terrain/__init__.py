from flask import Blueprint, request, Response, jsonify
import sys
import threading
import json
from queue import Queue

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


def dispatch_and_keep_result(req, q):
    print(req)
    resp = dispatch(req)
    print("done")

    q.put(resp)


@terrain_bp.route("/", methods=["POST"])
def index():
    req = request.get_data().decode()
    js = json.loads(req)

    print(req)

    if type(js) == list:
        responses = Queue()
        threads = []
        for req2 in js:
            t = threading.Thread(target=dispatch_and_keep_result, args=(json.dumps(req2), responses))
            threads.append(t)

            t.start()

        [t.join() for t in threads]

        responses = list(responses.queue)
        responses = [response.deserialized() for response in responses]

        return jsonify(responses)

    else:
        response = dispatch(req)

        return Response(str(response), response.http_status, mimetype="application/json")
