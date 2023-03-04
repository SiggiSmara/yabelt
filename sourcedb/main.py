from fastapi import FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/select_dbtype")
async def select_dbtype():
    return {"message": "This is where you select the db type to work with"}

@app.get("/createdb")
async def create_db():
    return {"message": "This is where you create the db structure and populate it with initial data"}

@app.get("/settings")
async def create_db():
    return {"message": "This is where you set your settings for insert/update/deletes"}

@app.get("/start")
async def create_db():
    return {"message": "This is where you start the background process that triggers the insert/update/deletes"}
