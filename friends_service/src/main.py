from collections import defaultdict
from fastapi import FastAPI
import uuid

app = FastAPI()

db_users = dict()
db_friends = defaultdict(set)


@app.get("/friends/{user_id}")
async def get_friends(user_id: uuid.UUID):
    if user_id in db_users and user_id in db_friends:
        return [{friend_id: db_users[friend_id]
                 for friend_id in db_friends[user_id]}]
    return []


@app.post("/friends/{user_id}")
async def add_friend(user_id: uuid.UUID, friend_id: uuid.UUID):
    if user_id in db_users and friend_id in db_users:
        db_friends[user_id].add(friend_id)
        db_friends[friend_id].add(user_id)
    return {}


@app.delete("/friends/{user_id}")
async def remove_friend(user_id: uuid.UUID, friend_id: uuid.UUID):
    if user_id in db_users and friend_id in db_users:
        db_friends[user_id].remove(friend_id)
        db_friends[friend_id].remove(user_id)
    return {}


@app.post("/users/{user}")
async def create_user(user: str):
    if user not in db_users.values():
        db_users[uuid.uuid4()] = user
    return {}


@app.get("/users")
async def get_users():
    return db_users
