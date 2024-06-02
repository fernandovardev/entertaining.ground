from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, Response, HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from starlette.middleware.sessions import SessionMiddleware
from . import models, database
from src.affinities.router import router as affinities_router
from src.grimoires.router import router as grimoires_router
from src.requests.router import router as requests_router
from src.ui.router import router as ui_router
from src.deps import create_tables_and_load_data, has_solved_riddle
from src.logger import logger, APIException
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/ui/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

@app.on_event("startup")
def on_startup():
    create_tables_and_load_data()


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    missing_param = exc.errors()[0]['loc'][-1]
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": f"No hay lugar en el mundo de la magia para alguien que no tiene {missing_param}"},
    )

app.include_router(affinities_router, prefix="/api")
app.include_router(grimoires_router, prefix="/api")
app.include_router(requests_router, prefix="/api")
app.include_router(ui_router, prefix="")
