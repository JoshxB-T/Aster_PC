import logging
import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.router import api_router
from app.services.redis import (
    create_redis_client,
    close_redis
)

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Redis connection...")

    redis_client = create_redis_client()
    app.state.redis = None
    
    try:
        redis_client.ping()
        app.state.redis = redis_client

        logger.info(
            "Redis connection established"
        )
    except:
        logger.exception(
            "Redis unavailable. Continuing without cache."
        )

        close_redis(redis_client)

        app.state.redis = None

    yield

    close_redis(app.state.redis)
    
    logger.info(
        "Redis connection closed"
    )

app = FastAPI(
    title="Aster Systems API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
