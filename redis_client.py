import aioredis
import os

redis = None

async def get_redis():
    global redis
    if redis is None:
        redis_url = os.getenv('REDIS_URL')
        redis = await aioredis.create_redis_pool(redis_url)
    return redis

async def close_redis():
    global redis
    if redis is not None:
        redis.close()
        await redis.wait_closed()
        redis = None

async def create(key: str, value: str):
    redis = await get_redis()
    await redis.set(key, value)

async def update(key: str, value: str):
    redis = await get_redis()
    if not await redis.exists(key):
        raise ValueError("Key does not exist")
    current_value = await redis.get(key, encoding='utf-8')
    new_value = current_value + value
    await redis.set(key, new_value)

async def get(key: str):
    redis = await get_redis()
    value = await redis.get(key, encoding='utf-8')
    if value is None:
        raise ValueError("Key does not exist")
    return value

async def clear(key: str):
    redis = await get_redis()
    if not await redis.exists(key):
        raise ValueError("Key does not exist")
    await redis.set(key, '')

async def delete(key: str):
    redis = await get_redis()
    if not await redis.exists(key):
        raise ValueError("Key does not exist")
    await redis.delete(key)
