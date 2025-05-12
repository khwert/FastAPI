from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from fastapi import FastAPI

DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost/learnFastAPI"
engine = create_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session