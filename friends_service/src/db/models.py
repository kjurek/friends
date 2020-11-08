from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column

from .database import Base


class Friendship(Base):
    __tablename__ = "friendships"
    user_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    friend_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
