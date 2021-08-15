from configuration import DB
import json

from flask import Blueprint, request, make_response, stream_with_context

from DbManager import DbManager

api = Blueprint('api', __name__)
from Lobby import Lobby_Manager

class DepthResponse:
    SUCC = "SUCCESS"
    ERROR = "ERROR"

    def __init__(self, type, message="", data=""):
        self.type = type
        self.message = message
        self.data = data

    def to_dict(self):
        response = dict()
        response['type'] = self.type
        response['message'] = self.message
        response['data'] = self.data
        return response

    def to_json(self):
        return json.dumps(self.to_dict())

INVALID_LOBBY_UUID_RES = (DepthResponse(DepthResponse.ERROR, message="Invalid Lobby UUID").to_json(), 400)

# Lobby Support
@api.route('/api/lobby/create')
def create_lobby():
    '''
    Generates a new lobby and returns the UUID of the newly created lobby
    sets the cookie "lobby_token" to the lobby UUID
    '''
    lobby = Lobby_Manager.create_lobby()
    if lobby is None:
        res = DepthResponse(DepthResponse.ERROR, message="Failed to create new lobby. Try again in a few seconds.").to_json(), 500
    else:
        res = DepthResponse(DepthResponse.SUCC, message="Successfully created a lobby", data=lobby.to_dict()).to_json(), 200

    resp = make_response(res)
    resp.set_cookie('lobby_token', lobby.uuid)
    return resp

# TODO Test
@api.route('/api/lobby/<str:lobby_uuid>')
def join_lobby(lobby_uuid): 
    '''
    "Joins" the lobby. i.e. sets the lobby_token cookie to the lobby uuid so future API requests are accepted
    '''
    lobby = Lobby_Manager.get_lobby(lobby_uuid)
    if lobby is None:
        return INVALID_LOBBY_UUID_RES

    res = DepthResponse(DepthResponse.SUCC, data=lobby.to_dict()).to_json(), 200
    resp = make_response(res)
    resp.set_cookie('lobby_token', lobby.uuid)
    return resp

# Song Queuing
@api.route('/api/queue', methods=['GET', 'POST', 'DELETE'])
def song_queue():
    lobby_token = request.cookies.get('lobby_token')

    # if not Lobby_Manager.lobby_exists(lobby_token):
    lobby = Lobby_Manager.get_lobby(lobby_token)
    if lobby is None:
        return INVALID_LOBBY_UUID_RES

    if request.method == 'GET': # TODO Test
        queue = lobby.song_queue.view()
        with DbManager(DB) as db:
            queue = [db.get_song_by_id(song_id).to_dict() for song_id in queue]
        
        return DepthResponse(DepthResponse.SUCC, data=queue).to_json(), 200

    elif request.method == 'POST': # TODO Test
        form = request.form
        song_ids = int(form['songs'])
        with DbManager(DB) as db:
            errors = []
            for song_id in song_ids:
                song = db.get_song_by_id(song_id)
                if song is None:
                    errors.append(song_id)
                else:
                    lobby.song_queue.put(song)
        
        if len(errors) == len(song_ids):
            return DepthResponse(DepthResponse.ERROR, message="Unable to queue songs", data=errors).to_json(), 300
        if len(errors) > 0:
            return DepthResponse(DepthResponse.SUCC, message="Unable to queue some songs", data=errors).to_json(), 200

        return DepthResponse(DepthResponse.SUCC, message="Songs queued").to_json(), 200

    elif request.method == 'DELETE':
        args = request.args
        raise NotImplementedError

# Song Searching
@api.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q')
    raise NotImplementedError

# Song Data
# TODO Test
@api.route('/api/song/<int:id>/metadata')
def song_metadata(id):
    '''
    Queries the metadata of a song given the id and returns it
    '''
    with DbManager(DB) as db:
        song = db.get_song_by_id(id)

    if song is None:
        return DepthResponse(DepthResponse.ERROR, message="Invalid song ID", data=id).to_json(), 300
    
    song_dict = song.to_dict()
    song_dict['lyrics_data'] = song.lyrics_data()
    # Good practice to not leak things about the filesystem to random users
    del song_dict['lyrics_path']
    del song_dict['audio_path']

    return DepthResponse(DepthResponse.SUCC, data=song_dict).to_json, 200

# TODO Test
@api.route('/api/song/<int:id>/data')
def song_data(id):
    '''
    Queries the audio of a song given the id and streams it
    '''
    with DbManager(DB) as db:
        song = db.get_song_by_id(id)

        if song is None:
            return DepthResponse(DepthResponse.ERROR, message="Invalid song ID", data=id).to_json(), 300
        
        return api.response_class(stream_with_context(song.audio_data()))