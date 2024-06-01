from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import IntegrityError
from json import load
from .database import engine, Base, SessionLocal
from .models import *
import os


def load_data_from_json(db, model_class, file_name):
    with open(file_name) as file:
        data_list = load(file)
        for data in data_list:
            instance = db.query(model_class).filter_by(**{key: data[key] for key in data.keys() if key in model_class.__table__.columns}).first()
            if not instance:
                db.add(model_class(**data))
    db.commit()
    

def create_tables_and_load_data():
    if not database_exists(engine.url):
        create_database(engine.url)
    
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        models_and_files = {
            Status: 'src/data/status.json',
            AfinidadMagica: 'src/data/affinities.json',
            Grimorio: 'src/data/grimoires.json'
        }
        
        for model, file_name in models_and_files.items():
            if os.path.exists(file_name):
                load_data_from_json(db, model, file_name)
        
        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close()