from flask import Blueprint, request

api = Blueprint('api', __name__)

# Lobby Support
@api.route('/api/lobby/create')
def create_lobby():
    '''
    Generates a UUID for a new lobby and a QR code to display on the response. Users trying to 
    join the lobby may scan the QR code to recieve a lobby token cookie.
    '''
    raise NotImplementedError

# Song Queuing
@api.route('/api/queue', methods=['GET', 'POST', 'DELETE'])
def song_queue():
    # lobby_token = request.cookies.get('lobby_token')
    if request.method == 'GET':
        args = request.args
        raise NotImplementedError
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

@api.route('/api/song/<int:id>/data')
def song_data(id):
    '''
    Queries the audio of a song given the id and streams it
    '''
    raise NotImplementedError

