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
        # zhu lee, do the thing!!
        if os.path.exists(filename) and os.path.isfile(filename):
            with open(filename, 'rb') as f:
                magic = f.read(3)
                if magic != b"DPT":
                    return False, "Magic is Wrong"
                
                self.song_title = str(f.read(256), encoding='utf-8')
                self.artist = str(f.read(128), encoding='utf-8')
                # unsigned short - uint16
                self.genre = Song.parseGenreID(struct.unpack("<H",f.read(2)))
                # unsigned int - uint32
                self.uuid = struct.unpack("<I", f.read(4))
                # unsigned short - uint16
                self.num_lines = struct.unpack("<H", f.read(2))

                # TODO the rest of the file. What does it look like fuck
            

    def save(self):
        pass