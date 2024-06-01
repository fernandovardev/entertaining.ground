from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from json import dumps
from . import models, database
from src.affinities.router import router as affinities_router
from src.grimoires.router import router as grimoires_router
from src.requests.router import router as requests_router
from src.ui.router import router as ui_router
from src.deps import create_tables_and_load_data
from src.logger import logger, APIException

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables_and_load_data()

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        request_body = await request.body()
        logger.info(f"Request body: {request_body.decode('utf-8')}")

        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_body_str = response_body.decode("utf-8")
        logger.info(f"Response body: {response_body_str}")
        new_response = Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))
        return new_response
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
        
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
    raise APIException(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"No se encontro el parámetro {missing_param}",
    )
    
app.include_router(affinities_router, prefix="/api")
app.include_router(grimoires_router, prefix="/api")
app.include_router(requests_router, prefix="/api")
app.include_router(ui_router, prefix="")
