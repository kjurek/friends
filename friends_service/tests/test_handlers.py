from unittest import mock

from src import handlers


@mock.patch("src.handlers.redis_cache")
@mock.patch("src.handlers.crud")
def test_add_friend(mock_crud, mock_redis_cache, database):
    mock_crud.add_friend.return_value = True
    assert handlers.add_friend(database, 0, 1) is True
    mock_redis_cache.delete.assert_called_once_with([0, 1])
    mock_crud.add_friend.assert_called_once_with(database, 0, 1)


@mock.patch("src.handlers.redis_cache")
@mock.patch("src.handlers.crud")
def test_remove_friend(mock_crud, mock_redis_cache, database):
    mock_crud.remove_friend.return_value = True
    assert handlers.remove_friend(database, 0, 1) is True
    mock_crud.remove_friend.assert_called_once_with(database, 0, 1)
    mock_redis_cache.delete.assert_called_once_with([0, 1])


@mock.patch("src.handlers.redis_cache")
@mock.patch("src.handlers.crud")
def test_get_friends_not_cached(mock_crud, mock_redis_cache, database):
    mock_crud.get_friends.return_value = [1, 2, 3, 4]
    mock_redis_cache.read.return_value = None
    assert handlers.get_friends(database, 0) == [1, 2, 3, 4]
    mock_redis_cache.read.assert_called_once_with(0)
    mock_crud.get_friends.assert_called_once_with(database, 0)
    mock_redis_cache.write.assert_called_once_with(0, [1, 2, 3, 4])


@mock.patch("src.handlers.redis_cache")
@mock.patch("src.handlers.crud")
def test_get_friends_cached(mock_crud, mock_redis_cache, database):
    mock_redis_cache.read.return_value = [1, 2, 3, 4]
    assert handlers.get_friends(database, 0) == [1, 2, 3, 4]
    mock_redis_cache.read.assert_called_once_with(0)
    mock_crud.get_friends.assert_not_called()
    mock_redis_cache.write.assert_not_called()
