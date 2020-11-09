from src.cache import redis_cache


def test_read():
    redis_cache.redis_interface.set(0, bytes([1, 2, 3, 4]))
    assert redis_cache.redis_interface.get(0) == bytes([1, 2, 3, 4])
    assert redis_cache.read(0) == [1, 2, 3, 4]


def test_write():
    redis_cache.write(0, [1, 2])
    assert redis_cache.redis_interface.get(0) == bytes([1, 2])


def test_delete():
    redis_cache.redis_interface.set(0, bytes([1, 2, 3, 4]))
    redis_cache.redis_interface.set(5, bytes([6, 7, 8]))
    redis_cache.redis_interface.set(15, bytes([16]))
    assert redis_cache.redis_interface.get(0) == bytes([1, 2, 3, 4])
    assert redis_cache.redis_interface.get(5) == bytes([6, 7, 8])
    assert redis_cache.redis_interface.get(15) == bytes([16])

    redis_cache.delete([0, 5])
    assert redis_cache.redis_interface.get(0) is None
    assert redis_cache.redis_interface.get(5) is None
    assert redis_cache.redis_interface.get(15) == bytes([16])


def test_delete_all():
    redis_cache.redis_interface.set(0, bytes([1, 2, 3, 4]))
    redis_cache.redis_interface.set(5, bytes([6, 7, 8]))
    assert redis_cache.redis_interface.get(0) == bytes([1, 2, 3, 4])
    assert redis_cache.redis_interface.get(5) == bytes([6, 7, 8])

    redis_cache.delete_all()
    assert redis_cache.redis_interface.get(0) is None
    assert redis_cache.redis_interface.get(5) is None
