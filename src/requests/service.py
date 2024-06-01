from sqlalchemy.orm import Session
from ..models import Solicitud, Status, Asignacion, Grimorio
from .schemas import SolicitudCreate, SolicitudUpdate
from ..logger import logger, APIException
import random

def get_solicitud(db: Session, solicitud_id: int):
    return db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()

def get_solicitud_by_identificacion(db: Session, identificacion: str):
    return db.query(Solicitud).filter(Solicitud.identificacion == identificacion).first()

def get_solicitudes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Solicitud).offset(skip).limit(limit).all()

def create_solicitud(db: Session, solicitud: SolicitudCreate):
    try: 
        db_solicitud = Solicitud(**solicitud.dict(), status_id=1)
        db.add(db_solicitud)
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud
    except APIException as e:
        db.rollback()
        logger.error(f"APIException: {e.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create solicitud: {e}")
        raise APIException(status_code=500, detail="Failed to create solicitud")

def update_solicitud(db: Session, solicitud_id: int, solicitud: SolicitudUpdate):
    try:
        db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if not db_solicitud:
            raise APIException(status_code=404, detail="Solicitud not found")
        
        for key, value in solicitud.dict().items():
            setattr(db_solicitud, key, value)
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud
    except APIException as e:
        db.rollback()
        logger.error(f"APIException: {e.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update solicitud: {e}")
        raise APIException(status_code=500, detail="Failed to update solicitud")

def delete_solicitud(db: Session, solicitud_id: int):
    try:
        db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if not db_solicitud:
            raise APIException(status_code=404, detail="Solicitud not found")
        
        db.delete(db_solicitud)
        db.commit()
        return db_solicitud
    except APIException as e:
        db.rollback()
        logger.error(f"APIException: {e.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete solicitud: {e}")
        raise APIException(status_code=500, detail="Failed to delete solicitud")

def assign_grimorio(db: Session, solicitud_id: int):
    try:
        db_solicitud = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if not db_solicitud:
            raise APIException(status_code=404, detail="Solicitud not found")
        
        grimorios = db.query(Grimorio).all()
        if not grimorios:
            raise APIException(status_code=400, detail="No grimoires available")
        
        grimorio = random.choice(grimorios)
        asignacion = Asignacion(solicitud_id=solicitud_id, grimorio_id=grimorio.id)
        db.add(asignacion)
        db.commit()
        db.refresh(asignacion)
        return asignacion
    except APIException as e:
        db.rollback()
        logger.error(f"APIException: {e.detail}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to assign grimorio: {e}")
        raise APIException(status_code=500, detail="Failed to assign grimorio")
