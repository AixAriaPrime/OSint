from __future__ import annotations

import json
import logging
from typing import Any, Optional

import redis.asyncio as aioredis

from .config import settings

logger = logging.getLogger(__name__)

_redis: Optional[aioredis.Redis] = None


async def get_redis() -> Optional[aioredis.Redis]:
    global _redis
    if _redis is None:
        try:
            _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
            await _redis.ping()
        except Exception as exc:
            logger.warning("Redis unavailable, caching disabled: %s", exc)
            _redis = None
    return _redis


async def cache_get(key: str) -> Optional[Any]:
    r = await get_redis()
    if r is None:
        return None
    try:
        value = await r.get(key)
        return json.loads(value) if value else None
    except Exception as exc:
        logger.warning("Cache get error: %s", exc)
        return None


async def cache_set(key: str, value: Any, ttl: int = settings.cache_ttl) -> None:
    r = await get_redis()
    if r is None:
        return
    try:
        await r.set(key, json.dumps(value), ex=ttl)
    except Exception as exc:
        logger.warning("Cache set error: %s", exc)


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None
