from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from redis_client import init_redis, close_redis

app = FastAPI(on_startup=[init_redis], on_shutdown=[close_redis])

class User(BaseModel):
    login: str
    password: str

def get_redis(request: Request):
    return request.app.state.redis

@app.post("/register")
async def register(u: User, r = Depends(get_redis)):
    await r.hset(f"user:{u.login}", mapping=u.dict())
    return {"login": u.login}

@app.post("/login")
async def login(u: User, r = Depends(get_redis)):
    data = await r.hgetall(f"user:{u.login}")
    if not data or data.get("password") != u.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "OK"}

@app.get("/users")
async def get_users(r = Depends(get_redis)):
    keys = await r.keys("user:*")
    return [await r.hgetall(k) for k in keys]
