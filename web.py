from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from database import Engine
from sqlmodel import select,Session
from chat_Models import Message, User, Group
class connectionmanager:
    def __init__(self):
        self.active_connections: dict[int,WebSocket]={}

    async def connect(self,websocket:WebSocket,user_id:int):
        await websocket.accept()
        self.active_connections[user_id]=websocket

    async def disconnect(self,user_id:int):
        self.active_connections.pop(user_id,None)


    async def send_message(self,message:str,user_id:int):
        user_active=self.active_connections.get(user_id)
        if user_active:
            await user_active.send(message)

    async def broadcast(self,message:str,group_id:int):
        with Session(Engine) as session:
            users_in_group=session.exec(select(User).join(Group,User.id==Group.id).where(Group.id==group_id)).all()

            for user in users_in_group:
                if user.id in self.active_connections:
                    await self.active_connections[user.id].send_text(message)
manager=connectionmanager()





