import redis.asyncio as redis

REDIS_URL = "redis://77.91.86.135:5540/0"
r = None

async def init_redis(app):
    global r
    r = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    app.state.redis = r

async def close_redis(app):
    await app.state.redis.close()
