from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from . import models, database
from .affinities.router import router as affinities_router
from .grimoires.router import router as grimoires_router
from .requests.router import router as requests_router
from .deps import create_tables_and_load_data
from .logger import logger

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables_and_load_data()

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

app.include_router(affinities_router, prefix="/api")
app.include_router(grimoires_router, prefix="/api")
app.include_router(requests_router, prefix="/api")
