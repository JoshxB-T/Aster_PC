import os
import logging

from dotenv import load_dotenv
from fastapi import Request
from redis import Redis
from redis.exceptions import RedisError

load_dotenv()

logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_CACHE_TTL = int(os.getenv("REDIS_CACHE_TTL", "60"))

def create_redis_client() -> Redis:
    return Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
        health_check_interval=30
    )

def get_redis(request: Request) -> Redis | None:
    return request.app.state.redis

def close_redis(client: Redis | None) -> None:
    if client is not None:
        client.close()

def invalidate_product_cache(
    client: Redis | None,
    product_id: int | None = None
) -> None:
    if client is None:
        return

    try:
        # Remove all product list variations
        keys = list(
            client.scan_iter("products:v1:*")
        )

        if keys:
            client.delete(*keys)

    except RedisError:
        logger.exception(
            "Product cache invalidation failed"
        )