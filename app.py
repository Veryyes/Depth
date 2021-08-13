import json
from pathlib import Path
import os

from flask import Flask , request, send_from_directory, abort
from DbManager import DbManager

from api import api

static_resources = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depth-ui", "build")
app = Flask(__name__, static_folder=static_resources)
app.register_blueprint(api)

DB = None
def setup():
    docs_dir = os.path.join(str(Path.home()), "Documents")
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    global DB
    DB = os.path.join(docs_dir, "Depth.DB")

@app.route('/', defaults={'path': "index.html"})
@app.route('/<path:path>')
def index(path):
    resource_dir = os.path.join(app.static_folder, path)
    if os.path.exists(resource_dir):
        return send_from_directory(app.static_folder, path)
    else:
        abort(404)


if __name__ == "__main__":
    setup()
    app.run(debug=True)
