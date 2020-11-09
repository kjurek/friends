from fastapi import FastAPI, Depends, Path
from sqlalchemy.orm import Session

from .db.database import engine, get_db
from .db import models, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

USER_ID_PATH = Path(..., title="Non-negative integer which identifies the user", ge=0)
FRIEND_ID_PATH = Path(..., title="Non-negative integer which identifies users friend", ge=0)

@app.get("/friends/{user_id}")
async def get_friends(user_id: int = USER_ID_PATH, db: Session = Depends(get_db)):
    return crud.get_friends(db, user_id)


@app.post("/friends/{user_id}/{friend_id}")
async def add_friend(user_id: int = USER_ID_PATH, friend_id: int = FRIEND_ID_PATH,
                     db: Session = Depends(get_db)):
    crud.add_friend(db, user_id, friend_id)


@app.delete("/friends/{user_id}/{friend_id}")
async def remove_friend(user_id: int = USER_ID_PATH, friend_id: int = FRIEND_ID_PATH,
                        db: Session = Depends(get_db)):
    crud.remove_friend(db, user_id, friend_id)
