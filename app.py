from flask import Flask , request, send_from_directory, abort
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
    if os.path.exists(resource_dir):
        return send_from_directory(app.static_folder, path)
    else:
        abort(404)

@app.route('/api/search/title')
def search_title():
    title = request.args.get("title")
    print(title)
    manager = DbManager(DB)
    manager.connect()
    songs = manager.get_songs_by_name(title)
    songs = [s.to_dict() for s in songs]
    return json.dumps(songs)

@app.route('/api/search/artist')
def search_artist():
    artist = request.args.get("artist")
    print(artist)
    manager = DbManager(DB)
    manager.connect()
    songs = manager.get_songs_by_artist(artist)
    songs = [s.to_dict() for s in songs]
    return json.dumps(songs)

@app.route('/api/songs')
def songs():
    manager = DbManager(DB)
    manager.connect()
    songs = manager.get_all_songs()
    songs = [s.to_dict() for s in songs]
    return json.dumps(songs)

@app.route('/api/songs/mp3/<path:mp3>')
def download_mp3(mp3):
    mp3path = os.path.join(static_resources,mp3)
    print("mp3 path: "+mp3path)
    print("static resource: "+static_resources)
    if os.path.exists(mp3path):
        return send_from_directory(static_resources,mp3)
    else:
        abort(404)

@app.route('/api/songs/lyrics/<path:lyric>')
def download_lyric(lyric):
    lyricpath = os.path.join(static_resources,lyric)
    print("mp3 path: "+lyricpath)
    print("static resource: "+static_resources)
    if os.path.exists(lyricpath):
        return send_from_directory(static_resources,lyric)
    else:
        abort(404)

if __name__ == "__main__":
    setup()
    app.run(debug=True)
