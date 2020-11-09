from sqlalchemy import Column, Integer

from .database import Base


class Friendship(Base):
    __tablename__ = "friendships"
    user_id = Column(Integer, primary_key=True)
    friend_id = Column(Integer, primary_key=True)
