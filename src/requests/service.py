
from src.database import SessionLocal
from src.affinities.service import update_afinidad_magica, create_afinidad_magica
from src.grimoires.service import update_grimorio, create_grimorio
from src.affinities.schemas import AfinidadMagicaCreate
from src.grimoires.schemas import GrimorioCreate
from sqlalchemy.orm import Session
from ..models import Solicitud, Grimorio, Asignacion, StatusEnum, AfinidadMagica
from .schemas import SolicitudCreate, SolicitudUpdate
from fastapi import HTTPException
import random
import logging
from json import load
logger = logging.getLogger(__name__)

def get_solicitud(db: Session, solicitud_id: int):
    return db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()

def get_solicitud_by_identificacion(db: Session, identificacion: str):
    return db.query(Solicitud).filter(Solicitud.identificacion == identificacion).first()

def get_solicitudes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Solicitud).offset(skip).limit(limit).all()

def create_solicitud(db: Session, solicitud: SolicitudCreate):
    try:
        db_solicitud = Solicitud(**solicitud.dict(), status=StatusEnum.PENDING)
        db.add(db_solicitud)
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create solicitud: {e}")
        raise

def update_solicitud(db: Session, solicitud_id: int, solicitud: SolicitudUpdate):
    try:
        db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if db_solicitud:
            for key, value in solicitud.dict().items():
                setattr(db_solicitud, key, value)
            db.commit()
            db.refresh(db_solicitud)
        return db_solicitud
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update solicitud: {e}")
        raise

def delete_solicitud(db: Session, solicitud_id: int):
    try:
        db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if db_solicitud:
            db.delete(db_solicitud)
            db.commit()
        return db_solicitud
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete solicitud: {e}")
        raise

def assign_grimorio(db: Session, solicitud_id: int):
    try:
        db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if db_solicitud:
            grimorios = db.query(Grimorio).all()
            if not grimorios:
                raise HTTPException(status_code=400, detail="No grimoires available")
            grimorio = random.choice(grimorios)
            asignacion = Asignacion(solicitud_id=solicitud_id, grimorio_id=grimorio.id)
            db.add(asignacion)
            db.commit()
            db.refresh(asignacion)
        return asignacion
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to assign grimorio: {e}")
        raise


def load_initial_data():
    db = SessionLocal()
    try:
        with open('src/data/affinities.json') as affinities_file:
            affinities_data = load(affinities_file)
            for affinity_data in affinities_data:
                afinidad = db.query(AfinidadMagica).filter(AfinidadMagica.nombre == affinity_data["nombre"]).first()
                if afinidad:
                    update_afinidad_magica(db, afinidad.id, AfinidadMagicaCreate(**affinity_data))
                else:
                    create_afinidad_magica(db, AfinidadMagicaCreate(**affinity_data))
        
        with open('src/data/grimoires.json') as grimoires_file:
            grimoires_data = load(grimoires_file)
            for grimorio_data in grimoires_data:
                grimorio = db.query(Grimorio).filter(Grimorio.tipo == grimorio_data["tipo"]).first()
                if grimorio:
                    update_grimorio(db, grimorio.id, GrimorioCreate(**grimorio_data))
                else:
                    create_grimorio(db, GrimorioCreate(**grimorio_data))
    finally:
        db.close()