from flask import Flask , request, send_from_directory
from DbManager import DbManager
import json
from pathlib import Path
import os

static_resources = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depth-ui", "build")
app = Flask(__name__, static_folder=static_resources)

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
    print(resource_dir)
    if os.path.exists(resource_dir):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/search')
def search():
    title = request.args.get("title")
    print(title)
    manager = DbManager(DB)
    manager.connect()
    songs = manager.get_songs_by_name(title)
    songs = [s.to_dict() for s in songs]
    return json.dumps(songs)

@app.route('/api/songs')
def songs():
    manager = DbManager(DB)
    manager.connect()
    songs = manager.get_all_songs()
    songs = [s.to_dict() for s in songs]
    return json.dumps(songs)

if __name__ == "__main__":
    setup()
    app.run(debug=True)
