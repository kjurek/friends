from pydantic import BaseModel
from typing import List


class GetFriendsResponse(BaseModel):
    user: int
    friends: List[int]
