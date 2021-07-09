from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, Float

Base = declarative_base()

class SongEntry(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    artist = Column(Text)
    # genre = relationship("GenreEntry")
    genre = Column(Text)
    rating = Column(Float)
    lyrics_path = Column(Text)

class GenreEntry(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
