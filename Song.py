import os

class Song:
    # TODO
    @staticmethod
    def parseGenreID(id):
        return ""

    def __init__(self, filename):
        self.filename = filename

        self.title = ""
        self.artist = ""
        self.genre = ""  
        self.rating = 0
        self.lyrics_mapping = []

        self.sound_path = ""

    def load(filename):
        self.filename = filename
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

            # TODO
            # CRC??

            # unsigned short - uint16
            self.num_lines = struct.unpack("<H", f.read(2))

            # TODO the rest of the file. What does it look like fuck

    def get_lyrics():
        pass

    def find_lyrics(String):
        pass

