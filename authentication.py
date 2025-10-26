from fastapi import HTTPException
from passlib.context import CryptContext
from database import Engine
from chat_Models import User
from sqlmodel import select, Session
from key import create_token, verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    truncated = password.encode("utf-8")[:72].decode("utf-8", "ignore")
    return pwd_context.hash(truncated)

def verify_hash(plain_password: str, hash_password_str: str) -> bool:
    truncated = plain_password.encode("utf-8")[:72].decode("utf-8", "ignore")
    return pwd_context.verify(truncated, hash_password_str)

async def register_user(name: str, email: str, plain_password: str):
    with Session(Engine) as session:
        query = select(User).where(User.email == email)
        exist = session.exec(query).first()
        if exist:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(plain_password)

        new_user = User(name=name, email=email, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    return new_user

async def login_user(email: str, password: str):
    with Session(Engine) as session:
        query = select(User).where(User.email == email)
        user = session.exec(query).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid email")

        if not verify_hash(password, user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        token_data = {"user_id": user.id, "email": user.email}
        access_created_token = create_token(token_data)
        return {"access_token": access_created_token, "type": "bearer"}

async def verify_user(user_id: int):
    with Session(Engine) as session:
        query = select(User).where(User.id == user_id)
        user = session.exec(query).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
