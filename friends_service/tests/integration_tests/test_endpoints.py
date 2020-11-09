from fastapi import status


def test_endpoints(test_client):
    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [1]

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [0]

    response = test_client.delete("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_non_existent_ids(test_client):
    response = test_client.delete("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_already_existing_ids(test_client):
    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [1]

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [0]

    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [1]

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [0]


def test_remove_reversed_friendship(test_client):
    response = test_client.post("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [1]

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [0]

    response = test_client.delete("friends/1/0")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_add_friend_with_userid_and_friend_id_equal_returns_code_422(test_client):
    response = test_client.post("/friends/0/0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"reason": "user_id [0] cannot be the same as friend_id [0]"}


def test_remove_friend_with_userid_and_friend_id_equal_returns_code_422(test_client):
    response = test_client.delete("/friends/0/0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"reason": "user_id [0] cannot be the same as friend_id [0]"}
