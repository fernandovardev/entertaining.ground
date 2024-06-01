import random
import string
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.main import app
from src.database import Base, SessionLocal
import pytest

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./test.db"))
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM asignaciones"))
        db.execute(text("DELETE FROM solicitudes"))
        db.execute(text("DELETE FROM grimorios"))
        db.execute(text("DELETE FROM afinidades_magicas"))
        db.execute(text("INSERT INTO afinidades_magicas (nombre) VALUES ('Fire')"))
        db.execute(text("INSERT INTO grimorios (tipo, rareza, peso) VALUES ('Trébol de cinco hojas', 'raro', 2)"))
        db.execute(text("""
            INSERT INTO solicitudes (nombre, apellido, identificacion, edad, afinidad_magica_id, status)
            VALUES ('Test', 'User', 'TEST123', 25, 1, 'pending')
        """))
        db.commit()
    except IntegrityError:
        db.rollback()
    yield db
    db.close()

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def random_int(start=1, end=100):
    return random.randint(start, end)
