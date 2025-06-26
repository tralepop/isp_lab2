from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import async_session
from models import User
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    login: str
    password: str

async def get_session():
    async with async_session() as s:
        yield s

@app.post("/register")
async def register(u: UserCreate, s: AsyncSession = Depends(get_session)):
    user = User(login=u.login, password=u.password)
    s.add(user)
    await s.commit()
    return {"id": user.id, "login": user.login}

@app.post("/login")
async def login(u: UserCreate, s: AsyncSession = Depends(get_session)):
    q = await s.execute(select(User).where(User.login == u.login))
    user = q.scalar_one_or_none()
    if not user or user.password != u.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Logged in"}

@app.get("/users")
async def get_all(s: AsyncSession = Depends(get_session)):
    q = await s.execute(select(User))
    return q.scalars().all()
