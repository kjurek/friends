from collections import defaultdict
import uuid

from src.db import crud, models


def get_all_friendships(database):
    friendships = database.query(models.Friendship).all()
    result = defaultdict(set)
    for friendship in friendships:
        result[friendship.user_id].add(friendship.friend_id)

    return result


def test_add_friend_one_friend(database):
    users = [uuid.uuid4(), uuid.uuid4()]
    crud.add_friend(database, users[0], users[1])

    assert database.query(models.Friendship).count() == 2
    assert get_all_friendships(database) == {
        users[0]: {users[1]},
        users[1]: {users[0]}
    }


def test_add_friend_friendship_with_self_takes_no_effect(database):
    user = uuid.uuid4()
    assert database.query(models.Friendship).count() == 0
    crud.add_friend(database, user, user)
    assert database.query(models.Friendship).count() == 0


def test_add_friend_already_existing_friendship(database):
    users = [uuid.uuid4(), uuid.uuid4()]
    friendship_models = [
        models.Friendship(user_id=users[0], friend_id=users[1]),
        models.Friendship(user_id=users[1], friend_id=users[0])
    ]
    database.add_all(friendship_models)
    database.commit()
    assert database.query(models.Friendship).count() == 2
    assert get_all_friendships(database) == {
        users[0]: {users[1]},
        users[1]: {users[0]},
    }

    crud.add_friend(database, users[0], users[1])
    assert database.query(models.Friendship).count() == 2
    assert get_all_friendships(database) == {
        users[0]: {users[1]},
        users[1]: {users[0]},
    }

    crud.add_friend(database, users[1], users[0])
    assert database.query(models.Friendship).count() == 2
    assert get_all_friendships(database) == {
        users[0]: {users[1]},
        users[1]: {users[0]},
    }


def test_add_friend_multiple_friends(database):
    users = [uuid.uuid4() for _ in range(5)]
    crud.add_friend(database, users[0], users[1])
    crud.add_friend(database, users[0], users[2])
    crud.add_friend(database, users[1], users[2])
    # user 3 and 4 have no friends

    assert database.query(models.Friendship).count() == 6
    assert get_all_friendships(database) == {
        users[0]: {users[1], users[2]},
        users[1]: {users[0], users[2]},
        users[2]: {users[0], users[1]},
    }


def test_remove_friend_one_friend(database):
    users = [uuid.uuid4(), uuid.uuid4()]
    crud.add_friend(database, users[0], users[1])

    assert database.query(models.Friendship).count() == 2
    crud.remove_friend(database, users[0], users[1])
    assert database.query(models.Friendship).count() == 0


def test_remove_friend_non_existing_friendship(database):
    users = [uuid.uuid4() for _ in range(3)]
    crud.add_friend(database, users[0], users[1])

    assert database.query(models.Friendship).count() == 2
    crud.remove_friend(database, users[0], users[2])

    assert database.query(models.Friendship).count() == 2
    assert get_all_friendships(database) == {
        users[0]: {users[1]},
        users[1]: {users[0]},
    }

    crud.remove_friend(database, users[2], users[0])
    assert database.query(models.Friendship).count() == 2
    assert get_all_friendships(database) == {
        users[0]: {users[1]},
        users[1]: {users[0]},
    }


def test_remove_friend_multiple_friends(database):
    users = [uuid.uuid4() for _ in range(5)]
    crud.add_friend(database, users[0], users[1])
    crud.add_friend(database, users[0], users[2])
    crud.add_friend(database, users[1], users[2])
    # user 3 and 4 have no friends

    assert database.query(models.Friendship).count() == 6
    crud.remove_friend(database, users[0], users[1])
    assert get_all_friendships(database) == {
        users[0]: {users[2]},
        users[1]: {users[2]},
        users[2]: {users[0], users[1]},
    }

    crud.remove_friend(database, users[0], users[2])
    assert get_all_friendships(database) == {
        users[1]: {users[2]},
        users[2]: {users[1]},
    }

    crud.remove_friend(database, users[2], users[1])
    assert get_all_friendships(database) == {}


def test_get_friends_one_friend(database):
    users = [uuid.uuid4(), uuid.uuid4()]
    crud.add_friend(database, users[0], users[1])
    assert database.query(models.Friendship).count() == 2

    assert crud.get_friends(database, users[0]) == [users[1]]
    assert crud.get_friends(database, users[1]) == [users[0]]


def test_get_friends_no_friends(database):
    users = [uuid.uuid4(), uuid.uuid4()]
    assert database.query(models.Friendship).count() == 0

    assert crud.get_friends(database, users[0]) == []
    assert crud.get_friends(database, users[1]) == []


def test_get_friends_multiple_friends(database):
    users = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    crud.add_friend(database, users[0], users[1])
    crud.add_friend(database, users[0], users[2])
    crud.add_friend(database, users[1], users[2])
    assert database.query(models.Friendship).count() == 6

    assert crud.get_friends(database, users[0]) == [users[1], users[2]]
    assert crud.get_friends(database, users[1]) == [users[0], users[2]]
    assert crud.get_friends(database, users[2]) == [users[0], users[1]]
