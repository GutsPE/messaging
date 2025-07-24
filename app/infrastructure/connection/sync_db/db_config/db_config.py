import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.engine import URL

load_dotenv(find_dotenv())


class BasicConfig:
    def __init__(self):
        self.database_type = os.getenv("DB_TYPE", "sqlite")  # "sqlite" o "postgresql"
        
        if self.database_type == "sqlite":
            self.database_url = "sqlite:///./app.db"  # archivo en raíz del proyecto
        else:
            self.drivername = "postgresql+psycopg2" # TODO validar a que motor de base de datos se le apunta y el driver
            self.username = os.getenv("DB_USER")
            self.password = os.getenv("DB_PASSWORD")
            self.host = os.getenv("DB_HOST")
            self.port = os.getenv("DB_PORT")
            self.database = os.getenv("DB_NAME")
            self.database_url = URL.create(
                drivername=self.drivername,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )

database_config = BasicConfig()
