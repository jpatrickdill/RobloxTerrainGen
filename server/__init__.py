from flask import Flask
from server.terrain import terrain_bp

app = Flask(__name__)

app.register_blueprint(terrain_bp, url_prefix="/terrain")
