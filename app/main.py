from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Biblioteca de Jogos API",
    description="Aplicação Web e API REST de Catálogo de Jogos em Python 3.11+, FastAPI e SQLAlchemy 2.0",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)