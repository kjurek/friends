import redis
from typing import Optional, List

from src.config.settings import REDIS_HOST, REDIS_PORT

redis_interface = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def read(user_id: int) -> Optional[List[int]]:
    cached_friends = redis_interface.get(user_id)
    if cached_friends is not None:
        cached_friends = list(cached_friends)

    return cached_friends


def write(user_id: int, friends: List[int]) -> None:
    redis_interface.set(user_id, bytes(friends))


def delete(user_ids: List[int]) -> None:
    if user_ids:
        redis_interface.delete(*user_ids)


def delete_all() -> None:
    redis_interface.flushall()
