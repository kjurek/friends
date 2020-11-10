from sqlalchemy.orm import Session
from typing import List

from src.cache import redis_cache
from src.db import crud


def add_friend(db: Session, user_id: int, friend_id: int) -> bool:
    redis_cache.delete([user_id, friend_id])
    return crud.add_friend(db, user_id, friend_id)


def remove_friend(db: Session, user_id: int, friend_id: int) -> bool:
    redis_cache.delete([user_id, friend_id])
    return crud.remove_friend(db, user_id, friend_id)


def get_friends(db: Session, user_id: int) -> List[int]:
    friends = redis_cache.read(user_id)
    if friends is None:
        friends = crud.get_friends(db, user_id)
        redis_cache.write(user_id, friends)
    return friends
