from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routes import router
from .core.model_loader import load_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_model()
    yield


app = FastAPI(title="ML Model Deploy (FastAPI)", lifespan=lifespan)
app.include_router(router)
