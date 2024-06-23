from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Catlog(Base):
    __tablename__ = 'catlog'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    msg_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    reply_to = Column(Integer, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user = relationship('User', back_populates='catlogs')
    group = relationship('Group', back_populates='catlogs')

    def __init__(self, msg_id, text, timestamp, group_id, user_id, reply_to=None):
        self.msg_id = msg_id
        self.text = text
        self.timestamp = timestamp
        self.group_id = group_id
        self.user_id = user_id
        self.reply_to = reply_to

    def __repr__(self):
        return f"<Catlog(id={self.id}, msg_id={self.msg_id}, text='{self.text}', timestamp='{self.timestamp}', group_id={self.group_id}, user_id={self.user_id}, reply_to={self.reply_to})>"



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tg_user_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    is_bot = Column(Boolean, nullable=False)
    username = Column(String, nullable=True, default=None)
    join_date = Column(DateTime, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    catlogs = relationship('Catlog', back_populates='user')

    def __init__(self, tg_user_id, first_name, last_name=None, is_bot=False, username=None, join_date=None):
        self.tg_user_id = tg_user_id
        self.first_name = first_name
        self.last_name = last_name
        self.is_bot = is_bot
        self.username = username
        self.join_date = join_date

    def __repr__(self):
        return f"<User(id={self.id}, tg_user_id={self.tg_user_id}, first_name='{self.first_name}', last_name='{self.last_name}', is_bot={self.is_bot}, username='{self.username}', join_date='{self.join_date}')>"


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tg_group_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    chat_type = Column(String, nullable=False)
    username = Column(String, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    catlogs = relationship('Catlog', back_populates='group')


    def __init__(self, tg_group_id, title, chat_type, username=None):
        self.tg_group_id = tg_group_id
        self.title = title
        self.chat_type = chat_type
        self.username = username

    def __repr__(self):
        return f"<Group(id={self.id}, tg_group_id={self.tg_group_id}, title='{self.title}', chat_type='{self.chat_type}', username='{self.username}')>"