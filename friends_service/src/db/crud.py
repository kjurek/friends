from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List

from . import models


def friendship_query(db: Session, user_id: int, friend_id: int):
    return db.query(models.Friendship)\
             .filter(and_(models.Friendship.user_id == user_id,
                          models.Friendship.friend_id == friend_id))


def add_friend(db: Session, user_id: int, friend_id: int) -> bool:
    if user_id == friend_id:
        return False

    if friendship_query(db, user_id, friend_id).count() > 0:
        return False

    friendships = [
        models.Friendship(user_id=user_id, friend_id=friend_id),
        models.Friendship(user_id=friend_id, friend_id=user_id)
    ]
    try:
        db.add_all(friendships)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    else:
        return True


def remove_friend(db: Session, user_id: int, friend_id: int) -> bool:
    if user_id == friend_id:
        return False

    rows_deleted = 0
    try:
        rows_deleted += friendship_query(db, user_id, friend_id).delete()
        rows_deleted += friendship_query(db, friend_id, user_id).delete()
        if rows_deleted > 0:
            db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    else:
        return rows_deleted > 0


def get_friends(db: Session, user_id: int) -> List[int]:
    friendhips = db.query(models.Friendship).filter(models.Friendship.user_id == user_id).all()
    return [friendship.friend_id for friendship in friendhips]
