import json

from flask import Blueprint, request, make_response

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

    if not Lobby_Manager.lobby_exists(lobby_token):
        return INVALID_LOBBY_UUID_RES

    if request.method == 'GET':
        lobby = Lobby_Manager.get_lobby(lobby_token)
        queue = lobby.song_queue.view()
        queue = [_get_song_metadata(song_id).to_dict() for song_id in queue]
        
        return DepthResponse(DepthResponse.SUCC, data=queue).to_json(), 200
    elif request.method == 'POST':
        form = request.form
        raise NotImplementedError
    elif request.method == 'DELETE':
        args = request.args
        raise NotImplementedError

# Song Searching
@api.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q')
    raise NotImplementedError

# Song Data
@api.route('/api/song/<int:id>/metadata')
def song_metadata(id):
    '''
    Queries the metadata of a song given the id and returns it
    '''
    raise NotImplementedError

def _get_song_metadata(id):
    with DbManager as db:
        song = db.get_song_by_id(id)
    return song
    
    

@api.route('/api/song/<int:id>/data')
def song_data(id):
    '''
    Queries the audio of a song given the id and streams it
    '''
    raise NotImplementedError

def _get_song_data(id):
    pass