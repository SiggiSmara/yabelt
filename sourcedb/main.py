from fastapi import FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/set_dbtype")
async def set_source_dbtype(source_dbtype: str):
    """The input is a single parameter of the supported db types.
    See README for supported db types.
    Based on the input the correct db type for the source db is set.
    """
    return {"message": "Source db type set to {source_dbtype}"}


@app.post("/create_table_defs")
async def create_table_defs():
    """input is a json file that defines a list of database tables to be copied to destination db.
    Each table in the list defines it's location in the source db (table name, database name,
    and schema name, if schema is used), it also defines the .
    For each table in the list the create_one_table_def is called with the location
    parameters"""
    return {
        "message": "This is where you create the db structure and populate it with initial data"
    }


@app.post("/create_one_table_def")
async def create_one_table_def():
    """input contains the location parameters of one table.  They are used to reflect the corresponding
    database table in the source db via sqlalchemy. This in turn is used to generate the same named
    table in the destination db.  Source settings determine if the location in the destination db reflect
    the location in the source system or if it is defined there where the table should be located"""
    return {"message": "This is where you create each table definition"}


@app.post("/settings")
async def settings():
    """Input here is a json that determines if only inserts, updates or deletes should
    be actively saved in the destination db or any combination of the three.  The overall
    setting can be overwritten by specific table settings."""
    return {"message": "This is where you set your settings for insert/update/deletes"}


@app.post("/sync/{action}")
async def sync(action: str = "start"):
    """The input action is either 'start' or 'stop'. If the action is start the background process
    should be started.  If the action is stop the background process should be stopped."""
    return {"message": "This is where you start/stop the background process."}
