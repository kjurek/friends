from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
import uuid

from . import models


def friendships_query(db: Session, user_id: uuid.UUID, friend_id: uuid.UUID):
    return db.query(models.Friendship)\
             .filter(or_(and_(models.Friendship.user_id == user_id,
                              models.Friendship.friend_id == friend_id),
                         and_(models.Friendship.user_id == friend_id,
                              models.Friendship.friend_id == user_id)))


def add_friend(db: Session, user_id: uuid.UUID, friend_id: uuid.UUID) -> None:
    if user_id == friend_id:
        return

    friendships = friendships_query(db, user_id, friend_id).all()
    if friendships:
        return

    try:
        friendships = [
            models.Friendship(user_id=user_id, friend_id=friend_id),
            models.Friendship(user_id=friend_id, friend_id=user_id)
        ]
        db.add_all(friendships)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


def remove_friend(db: Session, user_id: uuid.UUID, friend_id: uuid.UUID) -> None:
    try:
        rows_deleted = friendships_query(db, user_id, friend_id).delete()
        if rows_deleted:
            db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


def get_friends(db: Session, user_id: uuid.UUID) -> List[models.Friendship]:
    friendhips = db.query(models.Friendship).filter(models.Friendship.user_id == user_id).all()
    return [friendship.friend_id for friendship in friendhips]
