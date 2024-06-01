from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_TEST_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, echo=True)
test_engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)