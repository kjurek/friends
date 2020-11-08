from src.main import app
from fastapi.testclient import TestClient
from unittest import mock
import uuid

client = TestClient(app)


def test_invalid_path_returns_404():
    response = client.get("/invalid")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


@mock.patch("src.main.FriendshipController")
def test_get_friends_returns_code_200_with_empty_response(mock_controller):
    mock_controller.return_value.get_friends.return_value = []

    user_id = uuid.uuid4()
    response = client.get(f"/friends/{user_id}")
    assert response.status_code == 200
    assert response.json() == []


@mock.patch("src.main.FriendshipController")
def test_get_friends_returns_code_200_with_friends_in_response(mock_controller):
    friends = [uuid.uuid4() for _ in range(10)]
    mock_controller.return_value.get_friends.return_value = friends

    user_id = uuid.uuid4()
    response = client.get(f"/friends/{user_id}")
    assert response.status_code == 200
    assert response.json() == [str(friend_id) for friend_id in friends]


@mock.patch("src.main.FriendshipController")
def test_get_friends_with_invalid_user_id_returns_code_422(mock_controller):
    user_id = "invalid user id"
    response = client.get(f"/friends/{user_id}")
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['path', 'user_id'],
                    'msg': 'value is not a valid uuid',
                    'type': 'type_error.uuid'}]
    }


@mock.patch("src.main.FriendshipController")
def test_add_friend_returns_code_200(mock_controller):
    user_id = uuid.uuid4()
    friend_id = uuid.uuid4()
    response = client.post(f"/friends/{user_id}/{friend_id}")
    assert response.status_code == 200
    assert response.json() is None


@mock.patch("src.main.FriendshipController")
def test_add_friend_with_invalid_user_id_returns_code_422(mock_controller):
    user_id = "Invalid user id"
    friend_id = uuid.uuid4()
    response = client.post(f"/friends/{user_id}/{friend_id}")
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['path', 'user_id'],
                    'msg': 'value is not a valid uuid',
                    'type': 'type_error.uuid'}]
    }


@mock.patch("src.main.FriendshipController")
def test_add_friend_with_invalid_friend_id_returns_code_422(mock_controller):
    user_id = uuid.uuid4()
    friend_id = "Invalid friend id"
    response = client.post(f"/friends/{user_id}/{friend_id}")
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['path', 'friend_id'],
                    'msg': 'value is not a valid uuid',
                    'type': 'type_error.uuid'}]
    }


@mock.patch("src.main.FriendshipController")
def test_remove_friend_returns_code_200(mock_controller):
    user_id = uuid.uuid4()
    friend_id = uuid.uuid4()
    response = client.delete(f"/friends/{user_id}/{friend_id}")
    assert response.status_code == 200
    assert response.json() is None


@mock.patch("src.main.FriendshipController")
def test_remove_friend_with_invalid_user_id_returns_code_422(mock_controller):
    user_id = "Invalid user id"
    friend_id = uuid.uuid4()
    response = client.delete(f"/friends/{user_id}/{friend_id}")
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['path', 'user_id'],
                    'msg': 'value is not a valid uuid',
                    'type': 'type_error.uuid'}]
    }


@mock.patch("src.main.FriendshipController")
def test_remove_friend_with_invalid_friend_id_returns_code_422(mock_controller):
    user_id = uuid.uuid4()
    friend_id = "Invalid friend id"
    response = client.delete(f"/friends/{user_id}/{friend_id}")
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['path', 'friend_id'],
                    'msg': 'value is not a valid uuid',
                    'type': 'type_error.uuid'}]
    }
