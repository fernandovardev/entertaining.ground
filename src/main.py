from fastapi import FastAPI
from .database import engine, Base, SessionLocal
from .affinities.router import router as affinities_router
from .grimoires.router import router as grimoires_router
from .requests.router import router as requests_router
from .requests.service import load_initial_data
import json

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(affinities_router, prefix="/api")
app.include_router(grimoires_router, prefix="/api")
app.include_router(requests_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    load_initial_data()
