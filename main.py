from fastapi import FastAPI, Depends, Header, HTTPException, APIRouter
from database import create_db_tables
from chat_Models import User, Message, UserGroup, Group
from key import verify_token
from validate import Details, login
import bcrypt
from typing import Optional
from sqlmodel import select, Session
from database import Engine
from authentication import login_user, register_user, verify_user
import random
from fastapi.security import OAuth2PasswordBearer
from fastapi import WebSocket, WebSocketDisconnect, Form, Request
from fastapi.responses import RedirectResponse
from web import manager
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime

app = FastAPI()

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.add_middleware(SessionMiddleware, secret_key="Secret_Ra_Babu")


@app.on_event("startup")
def on_start():
    create_db_tables()
    print("All tables are created successfully")


@app.get("/")
async def root():
    return {"message": "app is working"}


@app.post("/register")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    new_user = register_user(name=username, email=email, plain_password=password)
    return RedirectResponse(url="/login.html", status_code=303)


@app.post("/login")
async def user_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    user = login_user(email=email, password=password)
    if not user:
        return RedirectResponse(url="/login.html", status_code=303)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard.html", status_code=303)


@app.get("/users")
async def get_all_users():
    with Session(Engine) as session:
        users = session.exec(select(User)).all()
    return users


@app.get("/protected")
async def protected_route(user_id: int):
    with Session(Engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not Exist")
    return {"message": "User authorized"}


@app.post("/create_group")
async def create_group(name: str):
    group_code = random.randint(100000, 999999)
    with Session(Engine) as session:
        exist = session.exec(select(Group).where(Group.code == group_code)).first()
        if exist:
            group_code = random.randint(100000, 999999)
        new_group = Group(name=name, code=group_code)
        session.add(new_group)
        session.commit()
        session.refresh(new_group)
    return {"Message": "Group_created"}


@app.get("/all_groups")
async def get_all_groups():
    with Session(Engine) as session:
        groups = session.exec(select(Group)).all()
    return groups


@app.post("/join_group")
async def join_group(group_code: int, user_id: int):
    with Session(Engine) as session:
        group = session.exec(select(Group).where(Group.code == group_code)).first()
        if not group:
            raise HTTPException(status_code=404, detail="NO Group Found")

        exist_already_in_group = session.exec(
            select(UserGroup).where(UserGroup.user_id == user_id, UserGroup.group_id == group.id)
        ).first()
        if exist_already_in_group:
            raise HTTPException(status_code=409, detail="Group Already Exist")

        user_group = UserGroup(user_id=user_id, group_id=group.id)
        session.add(user_group)
        session.commit()
        session.refresh(user_group)
    return {"Message": "Group Joined"}


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, user_id: int, group_id: int):
    try:
        user = verify_user(user_id)

        await manager.connect(websocket, user_id)

        with Session(Engine) as session:
            messages = session.exec(
                select(Message).where(Message.group_id == group_id).order_by(Message.timestamp)
            ).all()
            for message in messages:
                sender_name = message.sender.name
                await websocket.send_text(f"{sender_name}: {message.content}")

        while True:
            data = await websocket.receive_text()

            with Session(Engine) as session:
                message = Message(
                    content=data,
                    timestamp=datetime.utcnow(),
                    sender_id=user_id,
                    group_id=group_id
                )
                session.add(message)
                session.commit()
                await manager.broadcast(f"{user.name}: {data}", group_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print("Disconnected")
    except HTTPException:
        await websocket.close(code=1008)
