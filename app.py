from flask import Flask , request
from DbManager import DbManager
import json
from pathlib import Path
import os

app = Flask(__name__)

DB = None
def setup():
    docs_dir = os.path.join(str(Path.home()), "Documents")
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    global DB
    DB = os.path.join(docs_dir, "Depth.DB")

@app.route('/')
def index():
    return "Karaoke Home"

@app.route('/api/search')
def search():
    title = request.args.get("Title")
    print(title)
    manager = DbManager(DB)
    manager.connect()
    songs = manager.get_songs_by_name(title)
    songs = [s.to_dict() for s in songs]
    return json.dumps(songs)

if __name__ == "__main__":
    setup()
    app.run(debug=True)

