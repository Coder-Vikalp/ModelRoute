
import os

import redis
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from app.logging_config import configure_logging, logger

configure_logging()
logger.info(
    "ModelRoute application initialized",
    extra={"event_type": "application_started"}
)
app = FastAPI(title="ModelRoute API")


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics"
)


@app.get("/")
def home():
    return {
        "project": "ModelRoute",
        "status": "running"
    }


@app.get("/health")
def health():
    try:
        redis_client.ping()
        return {
            "api": "healthy",
            "redis": "healthy"
        }
    except redis.RedisError:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable"
        )



@app.get("/cache/{key}")
def get_cache(key: str):
    try:
        value = redis_client.get(key)
        cache_hit = value is not None

        logger.info(
            "Cache lookup completed",
            extra={
                "event_type": "cache_lookup",
                "cache_status": "hit" if cache_hit else "miss",
            },
        )

        return {
            "key": key,
            "value": value,
            "cache_hit": cache_hit
        }

    except redis.RedisError:
        logger.exception(
            "Redis cache lookup failed",
            extra={
                "event_type": "cache_lookup_failed",
                "error_code": "REDIS_ERROR",
            },
        )
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable"
        )


@app.put("/cache/{key}")
def set_cache(key: str, value: str):
    try:
        redis_client.set(key, value, ex=3600)

        logger.info(
            "Cache value saved",
            extra={
                "event_type": "cache_write",
            },
        )

        return {
            "key": key,
            "saved": True,
            "expires_in_seconds": 3600
        }

    except redis.RedisError:
        logger.exception(
            "Redis cache write failed",
            extra={
                "event_type": "cache_write_failed",
                "error_code": "REDIS_ERROR",
            },
        )
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable"
        )

