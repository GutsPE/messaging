import sys
import uvicorn

from pathlib import Path

from app.settings import app_constructor
from app.infrastructure.connection.sync_db.database import database_conn
from app.infrastructure.repositories.models.message_model import MessageModel

current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

app = app_constructor()

# Crear las tablas si no existen (esto ocurre una vez al inicio)
MessageModel.metadata.create_all(bind=database_conn.get_engine())

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8001)
