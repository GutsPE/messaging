from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.infrastructure.connection.sync_db.db_config.db_config import database_config


class Database:
    def __init__(self):
        self.DATABASE_URL = database_config.database_url
        connect_args = {"check_same_thread": False} if "sqlite" in self.DATABASE_URL else {}
        self.engine = create_engine(self.DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=10, pool_recycle=1800)
        self.session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.database = self.session()
        self.base = declarative_base()

    def get_db(self):
        try:
            yield self.database
        finally:
            self.database.close()

    def get_engine(self):
        return self.engine

    def database_connection_ping(self):
        try:
            with self.engine.connect():
                return True
        except OperationalError:
            return False


database_conn = Database()
