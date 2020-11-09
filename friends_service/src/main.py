from fastapi import FastAPI, Response, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .db.database import engine, get_db
from .db import models
from .integrations import setup_sentry
from . import handlers

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/friends/{user_id}", status_code=status.HTTP_200_OK)
async def get_friends(user_id: int = Path(..., ge=0), db: Session = Depends(get_db)):
    return handlers.get_friends(db, user_id)


@app.post("/friends/{user_id}/{friend_id}")
async def add_friend(user_id: int = Path(..., ge=0), friend_id: int = Path(..., ge=0),
                     db: Session = Depends(get_db)):
    if user_id == friend_id:
        message = {"reason": f"user_id [{user_id}] cannot be the same as friend_id [{friend_id}]"}
        return JSONResponse(content=message,
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    handlers.add_friend(db, user_id, friend_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/friends/{user_id}/{friend_id}")
async def remove_friend(user_id: int = Path(..., ge=0), friend_id: int = Path(..., ge=0),
                        db: Session = Depends(get_db)):
    if user_id == friend_id:
        message = {"reason": f"user_id [{user_id}] cannot be the same as friend_id [{friend_id}]"}
        return JSONResponse(content=message,
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    handlers.remove_friend(db, user_id, friend_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app = setup_sentry(app)
