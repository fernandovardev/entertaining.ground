from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from ..logger import logger

correct_riddle_answer = "42"

def validate_riddle_answer(answer: str):
    logger.info(f"Riddle answer received: {answer}")
    if answer == correct_riddle_answer:
        logger.info("Riddle solved correctly")
        return True
    else:
        logger.warning("Incorrect riddle answer")
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Respuesta incorrecta, intenta de nuevo.")
