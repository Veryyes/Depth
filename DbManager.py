from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Song import Base

from Song import SongEntry


class DbManager:
    def __init__(self, sqlite_db_path):
        self.url = "sqlite:///{}".format(sqlite_db_path)
        self.engine = create_engine(self.url)
        self.connection = None
        self.session = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def connect(self):
        self.connection = self.engine.connect()
        session = sessionmaker(self.engine)
        self.session = session()
        Base.metadata.create_all(self.engine)

    def close(self):
        self.session.commit()
        self.session.close()
        self.connection.close()
        self.session = None

    def get_all_songs(self):
        return self.session.query(SongEntry).all()

    def get_song_by_id(self, id):
        return self.session.query(SongEntry).filter(SongEntry.id == id).one()

    def get_songs_by_name(self, name):
        return self.session.query(SongEntry).filter(SongEntry.title == name).all()

    def get_songs_by_artist(self, name):
        return self.session.query(SongEntry).filter(SongEntry.artist == name).all()
