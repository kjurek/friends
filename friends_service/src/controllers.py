import uuid


class FriendshipController:
    def __init__(self, db):
        self.db = db

    def add_friend(self, user_id: uuid.UUID, friend_id: uuid.UUID) -> None:
        self.db[user_id].add(friend_id)
        self.db[friend_id].add(user_id)

    def remove_friend(self, user_id: uuid.UUID, friend_id: uuid.UUID) -> None:
        if user_id in self.db:
            self.db[user_id].remove(friend_id)

        if friend_id in self.db:
            self.db[friend_id].remove(user_id)

    def get_friends(self, user_id: uuid.UUID) -> list:
        return list(self.db[user_id])
