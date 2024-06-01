from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models import AfinidadMagica
from .schemas import AfinidadMagicaCreate
from ..logger import logger, APIException

def get_afinidades_magicas(db: Session):
    logger.info("Fetching all afinidades magicas from database")
    try:
        afinidades = db.query(AfinidadMagica).all()
        logger.info(f"Fetched {len(afinidades)} afinidades magicas")
        return afinidades
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener afinidades mágicas: {e}")
        raise APIException(status_code=500, detail="Error al obtener afinidades mágicas")

def get_afinidad_magica(db: Session, afinidad_id: int):
    logger.info(f"Fetching afinidad mágica with ID {afinidad_id}")
    try:
        afinidad = db.query(AfinidadMagica).filter(AfinidadMagica.id == afinidad_id).first()
        if not afinidad:
            logger.warning(f"Afinidad mágica with ID {afinidad_id} no encontrada")
            raise APIException(status_code=404, detail="Afinidad Mágica no encontrada")
        logger.info(f"Fetched afinidad mágica: {afinidad}")
        return afinidad
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener afinidad mágica con ID {afinidad_id}: {e}")
        raise APIException(status_code=500, detail="Error al obtener afinidad mágica")

def create_afinidad_magica(db: Session, afinidad: AfinidadMagicaCreate):
    logger.info(f"Creating new afinidad mágica with data: {afinidad}")
    db_afinidad = AfinidadMagica(**afinidad.dict())
    try:
        db.add(db_afinidad)
        db.commit()
        db.refresh(db_afinidad)
        logger.info(f"Created afinidad mágica: {db_afinidad}")
        return db_afinidad
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to create afinidad mágica due to IntegrityError: {e}")
        raise APIException(status_code=400, detail="Error al crear afinidad, la afinidad ya existe")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create afinidad mágica: {e}")
        raise APIException(status_code=500, detail="Error al crear afinidad")

def update_afinidad_magica(db: Session, afinidad_id: int, afinidad_data: AfinidadMagicaCreate):
    logger.info(f"Updating afinidad mágica with ID {afinidad_id} with data: {afinidad_data}")
    try:
        afinidad = db.query(AfinidadMagica).filter(AfinidadMagica.id == afinidad_id).first()
        if not afinidad:
            logger.warning(f"Afinidad mágica with ID {afinidad_id} no encontrada")
            raise APIException(status_code=404, detail="Afinidad Mágica no encontrada")

        for key, value in afinidad_data.dict().items():
            setattr(afinidad, key, value)

        db.commit()
        db.refresh(afinidad)
        logger.info(f"Updated afinidad mágica: {afinidad}")
        return afinidad
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to update afinidad mágica due to IntegrityError: {e}")
        raise APIException(status_code=400, detail="Error al actualizar afinidad, datos duplicados")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to update afinidad mágica: {e}")
        raise APIException(status_code=500, detail="Error al actualizar afinidad")
