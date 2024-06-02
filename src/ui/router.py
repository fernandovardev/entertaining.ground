from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..logger import logger, APIException
from .riddle_service import validate_riddle_answer
from src.database import get_db
from ..deps import has_solved_riddle
from src.grimoires import service as grimoire_services
from src.requests import service as request_services
router = APIRouter()
templates = Jinja2Templates(directory="src/ui/templates")

@router.get("/", summary="Welcome to the Project", response_class=HTMLResponse)
async def welcome(request: Request):
    logger.info("Accessed the welcome page")
    return templates.TemplateResponse("welcome.html", {"request": request})

@router.get("/riddle", summary="Riddle Authentication", response_class=HTMLResponse)
async def riddle_form(request: Request):
    logger.info("Accessed the riddle form page")
    return templates.TemplateResponse("riddle_form.html", {"request": request})

@router.post("/riddle", summary="Riddle Authentication", response_class=HTMLResponse)
async def solve_riddle(request: Request, answer: str = Form(...)):
    if validate_riddle_answer(answer):
        request.session["riddle_solved"] = True
        logger.info("Riddle solved correctly")
        return templates.TemplateResponse("success.html", {"request": request})
    else:
        logger.info("Riddle answer incorrect")
        return RedirectResponse(url="/riddle-fail", status_code=303)

@router.get("/riddle-fail", summary="Riddle Failure", response_class=HTMLResponse)
async def riddle_fail(request: Request):
    logger.info("Accessed the riddle fail page")
    return templates.TemplateResponse("riddle_fail.html", {"request": request})

@router.get("/secure", summary="Secure Page", response_class=HTMLResponse)
async def secure_page(request: Request, solved: bool = Depends(has_solved_riddle)):
    logger.info("Accessed the secure page")
    return templates.TemplateResponse("secure.html", {"request": request})

@router.get("/congratulations/{solicitud_id}", summary="Congratulations Page", response_class=HTMLResponse)
async def congratulations(request: Request, solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = request_services.get_solicitud(db, solicitud_id=solicitud_id)
    if not solicitud:
        raise APIException(status_code=404, detail="Solicitud no encontrada")
    
    grimorio = grimoire_services.get_grimorio_by_solicitud_id(db, solicitud_id=solicitud_id)
    return templates.TemplateResponse("congratulations.html", {"request": request, "solicitud": solicitud, "grimorio": grimorio})
