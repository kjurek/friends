import pytest

from fastapi import status
from itertools import count
from unittest import mock


def test_invalid_path_returns_404(test_client):
    response = test_client.get("/invalid")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


@mock.patch("src.main.handlers")
def test_get_friends_returns_code_200_with_empty_list(mock_handlers, test_client):
    mock_handlers.get_friends.return_value = []
    user_id = 1
    response = test_client.get(f"/friends/{user_id}")

    mock_handlers.get_friends.assert_called_once_with(mock.ANY, user_id)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@mock.patch("src.main.handlers")
def test_get_friends_returns_code_200_with_friends_in_response(mock_handlers, test_client):
    gen_id = count()
    friends = [str(next(gen_id)) for i in range(10)]
    mock_handlers.get_friends.return_value = friends
    user_id = next(gen_id)
    response = test_client.get(f"/friends/{user_id}")

    mock_handlers.get_friends.assert_called_once_with(mock.ANY, user_id)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == friends


@pytest.mark.parametrize("user_id, expected_response", [
    (-1, {'detail': [{'loc': ['path', 'user_id'], 'msg': 'ensure this value is greater than or equal to 0',
                      'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]}),
    ("AAA", {'detail': [{'loc': ['path', 'user_id'],
                         'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}),
])
@mock.patch("src.main.handlers")
def test_get_friends_with_invalid_id_returns_code_422(mock_handlers, test_client, user_id, expected_response):
    response = test_client.get(f"/friends/{user_id}")

    mock_handlers.get_friends.assert_not_called()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == expected_response


@mock.patch("src.main.handlers")
def test_add_friend_returns_code_204(mock_handlers, test_client):
    user_id, friend_id = 0, 1
    response = test_client.post(f"/friends/{user_id}/{friend_id}")

    mock_handlers.add_friend.assert_called_once_with(mock.ANY, user_id, friend_id)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("user_id, friend_id, expected_response", [
    (-1, 0, {'detail': [{'loc': ['path', 'user_id'], 'msg': 'ensure this value is greater than or equal to 0',
                         'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]}),
    (0, -1, {'detail': [{'loc': ['path', 'friend_id'], 'msg': 'ensure this value is greater than or equal to 0',
                         'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]}),
    ("AAA", 0, {'detail': [{'loc': ['path', 'user_id'],
                            'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}),
    (0, "AAA", {'detail': [{'loc': ['path', 'friend_id'],
                            'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]})
])
@mock.patch("src.main.handlers")
def test_add_friend_with_invalid_id_returns_code_422(mock_handlers, test_client, user_id, friend_id, expected_response):
    response = test_client.post(f"/friends/{user_id}/{friend_id}")

    mock_handlers.add_friend.assert_not_called()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == expected_response


@mock.patch("src.main.handlers")
def test_remove_friend_returns_code_204(mock_handlers, test_client):
    user_id, friend_id = 0, 1
    response = test_client.delete(f"/friends/{user_id}/{friend_id}")

    mock_handlers.remove_friend.assert_called_once_with(mock.ANY, user_id, friend_id)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("user_id, friend_id, expected_response", [
    (-1, 0, {'detail': [{'loc': ['path', 'user_id'], 'msg': 'ensure this value is greater than or equal to 0',
                         'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]}),
    (0, -1, {'detail': [{'loc': ['path', 'friend_id'], 'msg': 'ensure this value is greater than or equal to 0',
                         'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]}),
    ("AAA", 0, {'detail': [{'loc': ['path', 'user_id'],
                            'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]}),
    (0, "AAA", {'detail': [{'loc': ['path', 'friend_id'],
                            'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]})
])
@mock.patch("src.main.handlers")
def test_remove_friend_with_invalid_id_returns_code_422(mock_handlers, test_client, user_id, friend_id, expected_response):
    response = test_client.delete(f"/friends/{user_id}/{friend_id}")

    mock_handlers.remove_friend.assert_not_called()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == expected_response
