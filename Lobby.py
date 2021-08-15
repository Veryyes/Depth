from datetime import datetime
from time import time
from threading import Thread, Lock
import uuid

class RWLock:
    '''
    Reading prefered Read-Write Lock
    '''
    def __init__(self):
        self.w_lock = Lock()
        self.r_lock = Lock()
        self.num_r = 0

    def r_acquire(self):
        self.r_lock.acquire()
        self.num_r += 1
        if self.num_r == 1:
            self.w_lock.acquire()
        self.r_lock.release()

    def r_release(self):
        self.r_lock.acquire()
        self.num_r -= 1
        if self.num_r == 0:
            self.w_lock.release()
        self.r_lock.release()

    def w_acquire(self):
        self.w_lock.acquire()

    def w_release(self):
        self.w_lock.release()

class SongQueue:
    '''
    Thread Safe Song Queue
    '''
    def __init__(self):
        self.queue_lock = RWLock()
        self.queue = list()
        self.size = 0

    def put(self, song):
        '''
        Inserts a item to the end of the queue
        '''
        self.queue_lock.w_acquire()
        self.queue.append(song)
        self.queue_lock.w_release()

    def get(self):
        '''
        Removes the first item off the queue and returns it
        :returns: the first item off the queue
        '''
        self.queue_lock.w_acquire()
        song = self.queue.pop(0)
        self.queue_lock.w_release()

        return song

    def peek(self):
        '''
        Get the first item off the queue without modifying the queue
        :returns: first item on the queue
        '''
        self.queue_lock.r_acquire()
        song = self.queue[0]
        self.queue_lock.r_release()
        return song

    def __len__(self):
        self.queue_lock.r_acquire()
        size = self.size
        self.queue_lock.r_release()

        return size

    def view(self):
        '''
        Returns a copy of the queue
        :returns: a copy of the queue
        '''
        self.queue_lock.r_acquire()
        queue = self.queue[:]
        self.queue_lock.r_release()
        
        return queue
  

class Lobby:
    def __init__(self, uuid):
        self.uuid = uuid
        self.created = datetime.now()
        self.song_queue = SongQueue()

        self.door_lock  = Lock()
        # Protected by self.door_lock
        self.participants = 0
        self.empty_time = time.time()

    def user_join(self):
        '''
        Threadsafe way to notify the lobby that a user has joined
        '''
        self.door_lock.acquire()
        self.participants += 1
        self.door_lock.release()

    def user_leave(self):
        '''
        Threadsafe way to notify the lobby that a user has left
        '''
        self.door_lock.acquire()
        self.participants -= 1
        if self.participants == 0:
            self.empty_time = time.time()
        self.door_lock.release()

    def is_empty(self):
        '''
        Threadsafe way to check if the lobby is empty
        :returns: True if no one is in the lobby
        '''
        self.door_lock.acquire()
        ret = self.participants == 0
        self.door_lock.release()

        return ret

    def to_dict(self):
        d = dict()
        d['uuid'] = self.uuid
        d['creation_date'] = str(self.created)
        d['song_queue'] = self.song_queue.view()

        return d


class LobbyManager(Thread):
    def __init__(self, timeout=15*60, check_interval=5):
        self.timeout=timeout
        self.check_interval = check_interval
        self.running = True

        self.lobbies_lock = Lock()
        self.lobbies = dict()

    def lobby_exists(self, lobby_uuid):
        '''
        Threadsafe check if a lobby exists by uuid
        :param lobby_uuid: the uuid of the lobby to check
        :returns: True if the lobby exists, false otherwise
        '''
        self.lobbies_lock.acquire()
        
        l = self.lobbies.get(lobby_uuid, None)

        self.lobbies_lock.release()

        return not (l is None)
    
    def get_lobby(self, lobby_uuid):
        '''
        Threadsafe gets a lobby based on uuid
        :param lobby_uuid: the uuid of the lobby to check
        :returns: a lobby
        '''
        return self.lobbies.get(lobby_uuid, None)

    def create_lobby(self, timeout=20):
        '''
        Threadsafe creation of a lobby with a unique UUID
        :param timeout: seconds before timing out and failing
        :returns: A successfully created lobby and None when one could not be created within the timeout
        '''
        if self.lobbies_lock.acquire(timeout=timeout):

            lobby_uuid = uuid.uuid4()
            while lobby_uuid in self.lobbies.keys():
                lobby_uuid = uuid.uuid4()
            
            l = Lobby(lobby_uuid)
            self.lobbies[lobby_uuid] = l

            self.lobbies_lock.release()
            return l

        return None

    def delete_lobby(self, lobby_uuid):
        '''
        Threadsafe deletion of a lobby with a given UUID
        :param uuid: The UUID of the lobby
        '''
        self.lobbies_lock.acquire()
        
        if self.lobby_exists(lobby_uuid):
            del self.lobbies[lobby_uuid]

        self.lobbies_lock.release()

    def stop(self):
        '''
        Stops the monitoring of lobbies
        '''
        self.running = False


    def run(self):
        '''
        Do not run directly, use LobbyManager.start() instead.
        Monitors the all the lobbies and deletes ones that have been empty for too long
        '''
        while(self.running):
            self.lobbies_lock.acquire()

            for lobby_uuid in self.lobbies.keys():
                lobby = self.lobbies[lobby_uuid]

                if lobby.is_empty() and time.time() - lobby.empty_time >= self.timeout:
                    del self.lobbies[lobby_uuid]

            self.lobbies_lock.release()

            time.sleep(self.check_interval)

Lobby_Manager = LobbyManager()