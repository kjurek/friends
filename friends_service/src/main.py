from collections import defaultdict
from fastapi import FastAPI
import uuid

from .controllers import FriendshipController

app = FastAPI()
db = defaultdict(set)


@app.get("/friends/{user_id}")
async def get_friends(user_id: uuid.UUID):
    return FriendshipController(db).get_friends(user_id)


@app.post("/friends/{user_id}/{friend_id}")
async def add_friend(user_id: uuid.UUID, friend_id: uuid.UUID):
    FriendshipController(db).add_friend(user_id, friend_id)


@app.delete("/friends/{user_id}/{friend_id}")
async def remove_friend(user_id: uuid.UUID, friend_id: uuid.UUID):
    FriendshipController(db).remove_friend(user_id, friend_id)
