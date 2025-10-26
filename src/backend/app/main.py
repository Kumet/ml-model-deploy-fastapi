from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from .api.routes import router
from .core.logging_config import configure_logging
from .core.model_loader import load_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    configure_logging()
    structlog.get_logger(__name__).info("application_startup")
    load_model()
    yield
    structlog.get_logger(__name__).info("application_shutdown")


app = FastAPI(title="ML Model Deploy (FastAPI)", lifespan=lifespan)
app.include_router(router)
