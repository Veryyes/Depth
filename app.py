from flask import Flask , request
from DbManager import DbManager
import json
app = Flask(__name__)
DB = "C:\\Users\\Julian\\Downloads\\Karaoke App\\Depth.DB"


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
    app.run(debug=True)

