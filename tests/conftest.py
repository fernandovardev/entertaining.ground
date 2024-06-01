import random
import string
from fastapi.testclient import TestClient
from src.main import app
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from src.database import Base
import pytest

SQLALCHEMY_DATABASE_TEST_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

client = TestClient(app)

Base.metadata.create_all(bind=test_engine)

@pytest.fixture(scope="function")
def setup_db():
    db = TestSessionLocal()
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
