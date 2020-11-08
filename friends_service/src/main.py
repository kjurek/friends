from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uuid

from db.database import engine, get_db
from db import models, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/friends/{user_id}")
async def get_friends(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.get_friends(db, user_id)


@app.post("/friends/{user_id}/{friend_id}")
async def add_friend(user_id: uuid.UUID, friend_id: uuid.UUID, db: Session = Depends(get_db)):
    crud.add_friend(db, user_id, friend_id)


@app.delete("/friends/{user_id}/{friend_id}")
async def remove_friend(user_id: uuid.UUID, friend_id: uuid.UUID, db: Session = Depends(get_db)):
    crud.remove_friend(db, user_id, friend_id)
