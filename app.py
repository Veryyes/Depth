from pathlib import Path
import os

from flask import Flask , send_from_directory, abort
from DbManager import DbManager

from configuration import *
from api import api
from Lobby import Lobby_Manager

app = Flask(__name__, static_folder=STATIC_RESOURCES)
app.register_blueprint(api)

# DB = None
def setup():
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    Lobby_Manager.start()

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
