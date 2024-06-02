import random
import string
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import pytest
from contextlib import contextmanager

# Append the path to the src module
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.database import get_db
from src.models import *
from src.main import app, models

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# Client fixture
@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# Database setup fixture
@pytest.fixture(scope="module")
def setup_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        if os.path.exists("./test.db"):
            os.remove("./test.db")

# Function fixture for setting up initial data
@pytest.fixture(scope="function", autouse=True)
def setup_test_data():
    db = SessionLocal()
    try:
        db.execute(text("INSERT INTO status (name) VALUES ('pending')"))
        db.execute(text("INSERT INTO status (name) VALUES ('accepted')"))
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

# Helper functions for random data generation
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def random_int(start=1, end=100):
    return random.randint(start, end)
