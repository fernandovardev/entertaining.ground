from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from .affinities.router import router as affinities_router
from .grimoires.router import router as grimoires_router
from .requests.router import router as requests_router
from .deps import create_tables_and_load_data
import json

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables_and_load_data()

app.include_router(affinities_router, prefix="/api")
app.include_router(grimoires_router, prefix="/api")
app.include_router(requests_router, prefix="/api")
