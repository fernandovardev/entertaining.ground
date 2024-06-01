import random
import string
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.database import *
import pytest

DATABASE_URL= "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from src.main import app, models


client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    db = SessionLocal()
    try:
        db.execute(text("INSERT INTO status (name) VALUES ('pending')"))
        db.execute(text("INSERT INTO afinidades_magicas (nombre) VALUES ('Fire')"))
        db.execute(text("INSERT INTO grimorios (tipo, rareza, peso) VALUES ('Trébol de cinco hojas', 'raro', 2)"))
        db.execute(text("""
            INSERT INTO solicitudes (nombre, apellido, identificacion, edad, afinidad_magica_id, status_id)
            VALUES ('Test', 'User', 'TEST123', 25, 1, 1)
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
