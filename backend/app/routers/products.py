import logging

from typing import Literal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    Response,
)

from redis import Redis
from redis.exceptions import RedisError

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.product import (
    CPUDetailsResponse,
    GPUDetailsResponse,
    CategoryResponse,
    ProductDetailResponse,
    ProductListResponse,
    ProductResponse,
)

from app.services.product import get_product, get_products
from app.services.redis import get_redis, REDIS_CACHE_TTL

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

def get_db():
    with SessionLocal() as session:
        yield session

def get_cached_response(
    redis: Redis | None,
    cache_key: str,
    response_model
):
    if redis is None:
        return None
    
    try:
        cached_data = redis.get(cache_key)

        if cached_data:
            return response_model.model_validate_json(cached_data)
    except (RedisError, ValueError):
        logger.exception(
            "Redis cache retrieval failed %s",
            cache_key
        )

        try:
            redis.delete(cache_key)
        except RedisError:
            pass

    return None

def set_cached_response(
    redis: Redis | None,
    cache_key: str,
    response_model
):
    if redis is None:
        return
    
    try:
        redis.setex(
            cache_key,
            REDIS_CACHE_TTL,
            response_model.model_dump_json()
        )
    except RedisError:
        logger.exception(
            "Redis cache storage failed: %s",
            cache_key
        )

@router.get(
    "",
    response_model=ProductListResponse,
)
def list_products(
    response: Response,
    limit: int=Query(default=20, ge=1, le=100),
    offset: int=Query(default=0, ge=0),
    search: str | None=Query(default=None, max_length=100),
    category: Literal["CPU", "GPU"] | None=Query(default=None),
    session: Session = Depends(get_db),
    redis: Redis | None = Depends(get_redis)
) -> ProductListResponse:
    cache_key = (
        f"products:v1:"
        f"limit={limit}"
        f"offset={offset}"
        f"search={search or ''}:"
        f"category={category or ''}"
    )

    cached_result = get_cached_response(
        redis,
        cache_key,
        ProductListResponse
    )

    if cached_result is not None:
        response.headers["X-Cache"] = "HIT"
        return cached_result

    items, total = get_products(
        session,
        limit=limit,
        offset=offset,
        search=search,
        category=category
    )
    
    result = ProductListResponse(
        items=[
            ProductResponse.model_validate(item)
            for item in items 
        ],
        total=total,
        limit=limit,
        offset=offset
    )

    set_cached_response(
        redis,
        cache_key,
        result
    )

    response.headers["X-Cache"] = "MISS"

    return result

@router.get(
    "/{product_id}",
    response_model=ProductDetailResponse,
)
def get_product_by_id(
    response: Response,
    product_id: int,
    session: Session = Depends(get_db),
    redis: Redis | None = Depends(get_redis)
) -> ProductDetailResponse:
    cache_key = (
        f"products:v1:id={product_id}"
    )

    cached_result = get_cached_response(
        redis,
        cache_key,
        ProductDetailResponse
    )

    if cached_result is not None:
        response.headers["X-Cache"] = "HIT"
        return cached_result

    product = get_product(session, product_id)
    
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if product.cpu:
        details = CPUDetailsResponse.model_validate(product.cpu)
    elif product.gpu:
        details = GPUDetailsResponse.model_validate(product.gpu)
    else:
        details = None

    result = ProductDetailResponse(
        id=product.id,
        name=product.name,
        unit_price=product.unit_price,
        active=product.active,
        category=CategoryResponse.model_validate(product.category),
        details=details,
    )

    set_cached_response(
        redis,
        cache_key,
        result
    )

    response.headers["X-Cache"] = "MISS"

    return result