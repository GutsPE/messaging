import os
from dotenv import load_dotenv

load_dotenv()


class BasicConfig:
    def __init__(self):
        self.MONGODB_URL = os.getenv("MONGODB_URL") # TODO Validar Base de datos no relacional
        self.DATABASE_NAME = os.getenv("DATABASE_NAME")


database_config = BasicConfig()