
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
        return {
            "key": key,
            "value": value,
            "cache_hit": value is not None
        }
    except redis.RedisError:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable"
        )


@app.put("/cache/{key}")
def set_cache(key: str, value: str):
    try:
        redis_client.set(key, value, ex=3600)
        return {
            "key": key,
            "saved": True,
            "expires_in_seconds": 3600
        }
    except redis.RedisError:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable"
        )
