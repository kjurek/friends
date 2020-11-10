from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List

from src.db import models


def friendship_query(db: Session, user_id: int, friend_id: int):
    return db.query(models.Friendship)\
             .filter(and_(models.Friendship.user_id == user_id,
                          models.Friendship.friend_id == friend_id))


def add_friend(db: Session, user_id: int, friend_id: int) -> bool:
    if user_id == friend_id:
        return False

    if friendship_query(db, user_id, friend_id).count() > 0 or \
       friendship_query(db, friend_id, user_id).count() > 0:
        return False

    try:
        friendship = models.Friendship(user_id=user_id, friend_id=friend_id)
        db.add(friendship)
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
    friendships = db.query(models.Friendship).filter(models.Friendship.user_id == user_id).all()
    friendships_reversed = db.query(models.Friendship)\
                             .filter(models.Friendship.friend_id == user_id).all()
    friendships = [friendship.friend_id for friendship in friendships]
    friendships.extend([friendship.user_id for friendship in friendships_reversed])
    return friendships
