from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, service
from ..logger import logger, APIException

router = APIRouter()

@router.get("/grimorios/", response_model=list[schemas.Grimorio])
def read_grimorios(db: Session = Depends(get_db)):
    logger.info("Request to fetch all grimorios")
    try:
        return service.get_grimorios(db)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/grimorios/{grimorio_id}", response_model=schemas.Grimorio)
def read_grimorio(grimorio_id: int, db: Session = Depends(get_db)):
    logger.info(f"Request to fetch grimorio with ID {grimorio_id}")
    try:
        db_grimorio = service.get_grimorio(db, grimorio_id)
        if not db_grimorio:
            logger.warning(f"Grimorio con ID {grimorio_id} no encontrado")
            raise APIException(status_code=404, detail="Grimorio no encontrado")
        return db_grimorio
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/grimorios/", response_model=schemas.Grimorio)
def create_grimorio(grimorio: schemas.GrimorioCreate, db: Session = Depends(get_db)):
    logger.info(f"Request to create grimorio with data: {grimorio}")
    try:
        return service.create_grimorio(db, grimorio)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/grimorios/{grimorio_id}", response_model=schemas.Grimorio)
def update_grimorio(grimorio_id: int, grimorio: schemas.GrimorioCreate, db: Session = Depends(get_db)):
    logger.info(f"Request to update grimorio with ID {grimorio_id} with data: {grimorio}")
    try:
        return service.update_grimorio(db, grimorio_id, grimorio)
    except APIException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
