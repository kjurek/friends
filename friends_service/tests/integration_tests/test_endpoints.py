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


def test_endpoints_with_non_existent_ids(test_client):
    response = test_client.delete("/friends/0/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = test_client.get("/friends/0")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = test_client.get("/friends/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_endpoints_with_already_existing_ids(test_client):
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
