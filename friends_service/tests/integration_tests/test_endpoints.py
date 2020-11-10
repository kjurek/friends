from fastapi import status


def test_endpoints(test_client):
    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 0, "friends": [1]}

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 1, "friends": [0]}

    response = test_client.delete("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 0, "friends": []}

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 1, "friends": []}


def test_non_existent_ids(test_client):
    response = test_client.delete("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 0, "friends": []}

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 1, "friends": []}


def test_big_ids(test_client):
    response = test_client.post("/friends/2147483647/2147483646")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/2147483647")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 2147483647, "friends": [2147483646]}


def test_invalid_ids(test_client):
    response = test_client.post("/friends/-1/1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.post("/friends/1/-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.get("/friends/-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.delete("/friends/-1/1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.delete("/friends/1/-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    max_int = 2147483647
    id_int_overflow = max_int + 1
    response = test_client.get(f"/friends/{id_int_overflow}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.post(f"/friends/{id_int_overflow}/1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.post(f"/friends/1/{id_int_overflow}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.delete(f"/friends/{id_int_overflow}/1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.delete(f"/friends/1/{id_int_overflow}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_already_existing_ids(test_client):
    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 0, "friends": [1]}

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 1, "friends": [0]}

    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 0, "friends": [1]}

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 1, "friends": [0]}


def test_remove_reversed_friendship(test_client):
    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 0, "friends": [1]}

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 1, "friends": [0]}

    response = test_client.delete("friends/1/0")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 0, "friends": []}

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": 1, "friends": []}


def test_add_friend_with_userid_and_friend_id_equal_returns_code_422(test_client):
    response = test_client.post("/friends/0/0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [{"loc": ["path", "user_id"],
                    "msg": "user_id [0] cannot be the same as friend_id [0]",
                    "type": "value_error"}]
    }


def test_remove_friend_with_userid_and_friend_id_equal_returns_code_422(test_client):
    response = test_client.delete("/friends/0/0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [{"loc": ["path", "user_id"],
                    "msg": "user_id [0] cannot be the same as friend_id [0]",
                    "type": "value_error"}]
    }
