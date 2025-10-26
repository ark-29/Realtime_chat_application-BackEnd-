from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__='users'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str
  #these are relationships
    #here Message is a table and sender is sender in Message class
    messages: List["Message"] = Relationship(back_populates="sender")
    groups: List["UserGroup"] = Relationship(back_populates="user")


class Group(SQLModel, table=True):
    __tablename__='chat_groups'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    code: int = Field(unique=True, index=True)

    messages: List["Message"] = Relationship(back_populates="group")
    users: List["UserGroup"] = Relationship(back_populates="group")


class UserGroup(SQLModel, table=True):
    __tablename__='user_groups'
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    group_id: int = Field(foreign_key="chat_groups.id")

    user: Optional["User"] = Relationship(back_populates="groups")
    group: Optional["Group"] = Relationship(back_populates="users")


class Message(SQLModel, table=True):
    __tablename__='messages'
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    sender_id: int = Field(foreign_key="users.id")
    group_id: int = Field(foreign_key="chat_groups.id")

    sender: Optional["User"] = Relationship(back_populates="messages")
    group: Optional["Group"] = Relationship(back_populates="messages")

