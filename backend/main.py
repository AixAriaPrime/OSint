from __future__ import annotations

import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.cache import close_redis
from app.config import settings
from app.router import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_redis()


app = FastAPI(
    title="OmniTrace OSINT API",
    description="Ethical open-source intelligence aggregation platform.",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
