import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from app.database import Base

user_chat = Table(
    'user_chat',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('chat_id', Integer, ForeignKey('chats.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    username = Column(String, unique=True, )
    chats = relationship('Chat', secondary=user_chat, back_populates='users')


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", secondary=user_chat, back_populates="chats")
    created_at = Column(DateTime, default=datetime.datetime.now())


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())
