import aioredis
from environ import env_collection

redis = None

async def get_redis():
    global redis
    if redis is None:
        redis_url = env_collection['REDIS_URL']
        print(redis_url)
        redis = await aioredis.from_url(redis_url,)
    return redis

async def close_redis():
    global redis
    if redis is not None:
        await redis.close()
        await redis.connection_pool.disconnect()
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
