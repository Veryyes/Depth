from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Song import SongEntry

Base = declarative_base()
app = Flask(__name__)

class DbManager:
    def __init__(self, sqlite_db_path):
        self.url = "sqlite:///{}".format(sqlite_db_path)
        self.engine = create_engine(self.url)
        self.session = None
        Base.metadata.create_all(engine)

    def connect(self):
        self.engine.connect()
        session = sessionmaker(bind=self.engine)
        self.session = Session()

    @app.route('/api/songs', methods=['GET'])
    def get_all_songs(self):
        return  self.session.query(SongEntry.title).all()

    @app.route('/', methods=['GET'])
    def get_songs_by_name(self, name):
        return self.session.query(SongEntry).filter(SongEntry.title == name).all()

    @app.route('/', methods=['GET'])
    def get_songs_by_artist(self, name):
        return self.session.query(SongEntry).filter(SongEntry.artist == name).all()
