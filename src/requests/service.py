from sqlalchemy.orm import Session
from ..models import Solicitud, Grimorio, Asignacion, Status, AfinidadMagica
from .schemas import SolicitudCreate, SolicitudUpdate
from fastapi import HTTPException
import random
import logging
import os
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
        status_pending = db.query(Status).filter(Status.name == "PENDING").first()
        db_solicitud = Solicitud(**solicitud.dict(), status_id=status_pending.id)
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