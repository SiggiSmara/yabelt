import os
import pyodbc
from sqlalchemy import create_engine, URL
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from pathlib import Path

my_env_path = Path(".env")
if my_env_path.is_file:
    load_dotenv(my_env_path)
    print("local .env loaded")


url_object = URL.create(
    "mssql+pyodbc",
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    port=os.environ.get("DB_PORT"),
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "autocommit": "True",
    }
)

pyodbc.pooling = False
engine = create_engine(url_object).execution_options(
    isolation_level="AUTOCOMMIT"
)

# Base = declarative_base()
class Base(DeclarativeBase):
    pass

def get_session():
    with Session(engine) as session:
        yield session
    