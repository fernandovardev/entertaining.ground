from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, service
from ..logger import logger, APIException

router = APIRouter()

@router.get("/afinidades/", response_model=list[schemas.AfinidadMagica])
def read_afinidades(db: Session = Depends(get_db)):
    logger.info("Request to fetch all afinidades magicas")
    try:
        return service.get_afinidades_magicas(db)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/afinidades/{afinidad_id}", response_model=schemas.AfinidadMagica)
def read_afinidad(afinidad_id: int, db: Session = Depends(get_db)):
    logger.info(f"Request to fetch afinidad magica with ID {afinidad_id}")
    try:
        db_afinidad = service.get_afinidad_magica(db, afinidad_id)
        if not db_afinidad:
            logger.warning(f"Afinidad magica con ID {afinidad_id} no encontrada")
            raise APIException(status_code=404, detail="Afinidad Mágica no encontrada")
        return db_afinidad
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/afinidades/", response_model=schemas.AfinidadMagica)
def create_afinidad(afinidad: schemas.AfinidadMagicaCreate, db: Session = Depends(get_db)):
    logger.info(f"Request to create afinidad with data: {afinidad}")
    try:
        return service.create_afinidad_magica(db, afinidad)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/afinidades/{afinidad_id}", response_model=schemas.AfinidadMagica)
def update_afinidad(afinidad_id: int, afinidad: schemas.AfinidadMagicaCreate, db: Session = Depends(get_db)):
    logger.info(f"Request to update afinidad magica with ID {afinidad_id} with data: {afinidad}")
    try:
        return service.update_afinidad_magica(db, afinidad_id, afinidad)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
