# src/grimoires/service.py
from sqlalchemy.orm import Session
from ..models import Grimorio
from .schemas import GrimorioCreate, Grimorio as GrimorioSchema
import random

def get_grimorios(db: Session):
    return db.query(Grimorio).all()

def get_grimorio(db: Session, grimorio_id: int):
    return db.query(Grimorio).filter(Grimorio.id == grimorio_id).first()

def create_grimorio(db: Session, grimorio: GrimorioCreate):
    db_grimorio = Grimorio(**grimorio.dict())
    db.add(db_grimorio)
    db.commit()
    db.refresh(db_grimorio)
    return db_grimorio

def update_grimorio(db: Session, grimorio_id: int, grimorio_data: GrimorioCreate):
    grimorio = db.query(Grimorio).filter(Grimorio.id == grimorio_id).first()
    if grimorio:
        for key, value in grimorio_data.dict().items():
            setattr(grimorio, key, value)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(grimorio)
    return grimorio

