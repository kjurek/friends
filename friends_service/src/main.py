from fastapi import FastAPI, Response, Depends, Path, status
from sqlalchemy.orm import Session

from .db.database import engine, get_db
from .db import models, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/friends/{user_id}", status_code=status.HTTP_200_OK)
async def get_friends(user_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    return crud.get_friends(db, user_id)


@app.post("/friends/{user_id}/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_friend(user_id: int = Path(..., ge=0), friend_id: int = Path(..., ge=0),
                     db: Session = Depends(get_db)):
    crud.add_friend(db, user_id, friend_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/friends/{user_id}/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(user_id: int = Path(..., ge=0), friend_id: int = Path(..., ge=0),
                        db: Session = Depends(get_db)):
    crud.remove_friend(db, user_id, friend_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
