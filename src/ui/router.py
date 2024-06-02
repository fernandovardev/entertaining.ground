from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..logger import logger
from .riddle_service import validate_riddle_answer
from ..deps import has_solved_riddle

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
