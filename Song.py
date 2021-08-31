import os 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from configuration import READ_SIZE

Base = declarative_base()

class SongEntry(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    artist = Column(Text)
    genre = relationship("GenreEntry")
    genre_id = Column(Integer,ForeignKey("genres.id"))
    rating = Column(Float)
    lyrics_path = Column(Text) # Path to file containing lyrics data
    audio_path = Column(Text) # Path to audio file

    def lyrics_data(self):
        if not os.path.exists(self.lyrics_path):
            raise IOError("Lyrics File Does not Exist: {}".format(self.lyrics_path))

        with open(self.lyrics_path, 'r') as f:
            lyrics_data = f.read()
            
        return lyrics_data

    def audio_data(self):
        audio_path = self.audio_path
        return self._audio_data(audio_path)

    def _audio_data(self, audio_path):
        if not os.path.exists(audio_path):
            raise IOError("Audio File Does not Exist: {}".format(audio_path))

        with open(audio_path, 'rb') as f:
            audio_data = f.read(READ_SIZE)
            yield audio_data

            while not (audio_data is None):
                audio_data = f.read(READ_SIZE)
                yield audio_data
                
    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "artist":self.artist,
            "genre": "" if self.genre is None else self.genre.name,
            "rating":self.rating,
            "lyrics_path": self.lyrics_path,
            "audio_path": self.audio_path
        }


class GenreEntry(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
