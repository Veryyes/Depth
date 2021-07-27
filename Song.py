from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class SongEntry(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    artist = Column(Text)
    genre = relationship("GenreEntry")
    genre_id=Column(Integer,ForeignKey("genres.id"))
    rating = Column(Float)
    lyrics_path = Column(Text)
    file_name = Column(Text)

    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "artist":self.artist,
            "genre": "" if self.genre is None else self.genre.name,
            "rating":self.rating,
            "file_name": self.file_name,
            "lyrics_path": self.lyrics_path
        }


class GenreEntry(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
