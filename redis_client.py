import aioredis
from environ import env_collection

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_url = env_collection['REDIS_URL']
        redis_client = await aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    return redis_client

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()

async def create(key: str, value: str):
    redis = await get_redis()
    await redis.set(key, value)

async def update(key: str, value: str):
    redis = await get_redis()
    if not await redis.exists(key):
        raise ValueError("Key does not exist")
    current_value = await redis.get(key)
    new_value = current_value + value
    await redis.set(key, new_value)

async def get(key: str):
    redis = await get_redis()
    if not await redis.exists(key):
        raise ValueError("Key does not exist")
    return await redis.get(key)

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
