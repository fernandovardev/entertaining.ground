from fastapi import FastApi

app = FastApi()

@app.get("/")
def index():
    return {"details": "Hola Mundo"}