import redis
from environ import env_collection

redisCli = None


async def get_redis():
    global redisCli
    if redisCli is None:
        redis_url = env_collection["REDIS_URL"]
        redisCli = await redis.from_url(redis_url)
    return redisCli


def close_redis():
    global redisCli
    if redisCli is not None:
        redisCli.close()
        redisCli = None


def create(key: str, value: str):
    redisCli = get_redis()
    redisCli.set(key, value)


def update(key: str, value: str):
    redisCli = get_redis()
    if not redisCli.exists(key):
        raise ValueError("Key does not exist")
    current_value = redisCli.get(key, encoding="utf-8")
    new_value = current_value + value
    redisCli.set(key, new_value)


def get(key: str):
    redisCli = get_redis()
    value = redisCli.get(key, encoding="utf-8")
    if value is None:
        raise ValueError("Key does not exist")
    return value


def clear(key: str):
    redisCli = get_redis()
    if not redisCli.exists(key):
        raise ValueError("Key does not exist")
    redisCli.set(key, "")


def delete(key: str):
    redisCli = get_redis()
    if not redisCli.exists(key):
        raise ValueError("Key does not exist")
    redisCli.delete(key)
