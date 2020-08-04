import os
import struct

from Song import Song

'''
Represents a lyrics mapping project
'''
class Project:
    def __init__(self):
        self.filename = None
        self.song_title = ""


    @staticmethod
    def load(filename):
        self.filename = filename
        if os.path.exists(filename) and os.path.isfile(filename):
            with open(filename, 'rb') as f:

        # zhu lee, do the thing!!
                
            

    def save(self):
        pass