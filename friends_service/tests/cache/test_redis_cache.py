import json

from src.cache import redis_cache


def test_read():
    redis_cache.redis_interface.set(0, json.dumps([1, 2, 3, 4]))
    assert redis_cache.redis_interface.get(0).decode() == json.dumps([1, 2, 3, 4])
    assert redis_cache.read(0) == [1, 2, 3, 4]


def test_write():
    redis_cache.write(0, [1, 2])
    assert redis_cache.redis_interface.get(0).decode() == json.dumps([1, 2])


def test_write_read_big_numbers():
    max_int = 2147483647
    redis_cache.write(0, [max_int])
    redis_cache.write(max_int, [0])
    assert redis_cache.redis_interface.get(0).decode() == json.dumps([max_int])
    assert redis_cache.read(0) == [max_int]
    assert redis_cache.read(max_int) == [0]


def test_delete():
    redis_cache.redis_interface.set(0, json.dumps([1, 2, 3, 4]))
    redis_cache.redis_interface.set(5, json.dumps([6, 7, 8]))
    redis_cache.redis_interface.set(15, json.dumps([16]))
    assert redis_cache.redis_interface.get(0).decode() == json.dumps([1, 2, 3, 4])
    assert redis_cache.redis_interface.get(5).decode() == json.dumps([6, 7, 8])
    assert redis_cache.redis_interface.get(15).decode() == json.dumps([16])

    redis_cache.delete([0, 5])
    assert redis_cache.redis_interface.get(0) is None
    assert redis_cache.redis_interface.get(5) is None
    assert redis_cache.redis_interface.get(15).decode() == json.dumps([16])


def test_delete_all():
    redis_cache.redis_interface.set(0, json.dumps([1, 2, 3, 4]))
    redis_cache.redis_interface.set(5, json.dumps([6, 7, 8]))
    assert redis_cache.redis_interface.get(0).decode() == json.dumps([1, 2, 3, 4])
    assert redis_cache.redis_interface.get(5).decode() == json.dumps([6, 7, 8])

    redis_cache.delete_all()
    assert redis_cache.redis_interface.get(0) is None
    assert redis_cache.redis_interface.get(5) is None
