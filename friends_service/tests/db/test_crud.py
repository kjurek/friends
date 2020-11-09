from collections import defaultdict

from src.db import crud, models


def get_all_friendships(database):
    friendships = database.query(models.Friendship).all()
    result = defaultdict(list)
    for friendship in friendships:
        result[friendship.user_id].append(friendship.friend_id)

    for user_id in result:
        result[user_id] = sorted(result[user_id])

    return result


def test_add_friend_one_friend(database):
    assert crud.add_friend(database, 0, 1) is True
    assert get_all_friendships(database) == {
        0: [1],
    }


def test_add_friend_friendship_with_self_takes_no_effect(database):
    assert crud.add_friend(database, 0, 0) is False
    assert database.query(models.Friendship).count() == 0


def test_add_friend_already_existing_friendship_takes_no_effect(database):
    database.add(models.Friendship(user_id=0, friend_id=1))
    database.commit()
    assert get_all_friendships(database) == {
        0: [1],
    }

    assert crud.add_friend(database, 0, 1) is False
    assert get_all_friendships(database) == {
        0: [1],
    }

    assert crud.add_friend(database, 1, 0) is False
    assert get_all_friendships(database) == {
        0: [1],
    }


def test_add_friend_multiple_friends(database):
    assert crud.add_friend(database, 0, 1) is True
    assert crud.add_friend(database, 0, 2) is True
    assert crud.add_friend(database, 1, 2) is True
    assert get_all_friendships(database) == {
        0: [1, 2],
        1: [2],
    }


def test_remove_friend_one_friend(database):
    database.add(models.Friendship(user_id=0, friend_id=1))
    database.commit()
    assert get_all_friendships(database) == {
        0: [1],
    }

    assert crud.remove_friend(database, 0, 1) is True
    assert database.query(models.Friendship).count() == 0


def test_remove_friend_non_existing_friendship(database):
    database.add(models.Friendship(user_id=0, friend_id=1))
    database.commit()
    assert get_all_friendships(database) == {
        0: [1],
    }

    assert crud.remove_friend(database, 0, 2) is False
    assert get_all_friendships(database) == {
        0: [1],
    }

    assert crud.remove_friend(database, 2, 0) is False
    assert get_all_friendships(database) == {
        0: [1],
    }


def test_remove_friend_multiple_friends(database):
    friendship_models = [
        models.Friendship(user_id=0, friend_id=1),
        models.Friendship(user_id=0, friend_id=2),
        models.Friendship(user_id=1, friend_id=2),
    ]
    database.add_all(friendship_models)
    database.commit()
    assert get_all_friendships(database) == {
        0: [1, 2],
        1: [2],
    }

    assert crud.remove_friend(database, 0, 1) is True
    assert get_all_friendships(database) == {
        0: [2],
        1: [2],
    }

    assert crud.remove_friend(database, 0, 2) is True
    assert get_all_friendships(database) == {
        1: [2],
    }

    assert crud.remove_friend(database, 2, 1) is True
    assert database.query(models.Friendship).count() == 0


def test_get_friends_one_friend(database):
    database.add(models.Friendship(user_id=0, friend_id=1))
    database.commit()
    assert get_all_friendships(database) == {
        0: [1],
    }
    assert crud.get_friends(database, 0) == [1]
    assert crud.get_friends(database, 1) == [0]


def test_get_friends_no_friends(database):
    assert database.query(models.Friendship).count() == 0
    assert crud.get_friends(database, 0) == []
    assert crud.get_friends(database, 1) == []


def test_get_friends_multiple_friends(database):
    friendship_models = [
        models.Friendship(user_id=0, friend_id=1),
        models.Friendship(user_id=0, friend_id=2),
        models.Friendship(user_id=1, friend_id=2),
    ]
    database.add_all(friendship_models)
    database.commit()
    assert get_all_friendships(database) == {
        0: [1, 2],
        1: [2],
    }
    assert sorted(crud.get_friends(database, 0)) == [1, 2]
    assert sorted(crud.get_friends(database, 1)) == [0, 2]
    assert sorted(crud.get_friends(database, 2)) == [0, 1]


def test_remove_friend_friendship_with_self_takes_no_effect(database):
    database.add(models.Friendship(user_id=0, friend_id=1))
    database.commit()
    assert get_all_friendships(database) == {
        0: [1],
    }

    assert crud.remove_friend(database, 0, 0) is False
    assert get_all_friendships(database) == {
        0: [1],
    }

    assert crud.remove_friend(database, 1, 1) is False
    assert get_all_friendships(database) == {
        0: [1],
    }
