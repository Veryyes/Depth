from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from Song import Base

from Song import SongEntry

# Base = declarative_base()
# metadata = MetaData()

class DbManager:
    def __init__(self, sqlite_db_path):
        self.url = "sqlite:///{}".format(sqlite_db_path)
        self.engine = create_engine(self.url)
        self.session = None
        

    def connect(self):
        self.engine.connect()
        Session = sessionmaker(self.engine)
        #Session.configure(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def get_all_songs(self):
        return  self.session.query(SongEntry.title).all()

    def get_songs_by_name(self, name):
        return self.session.query(SongEntry).filter(SongEntry.title == name).all()
    
    def get_songs_by_artist(self, name):
        return self.session.query(SongEntry).filter(SongEntry.artist == name).all()
    
    
