from fastapi import FastAPI, Response, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.integrations import setup_sentry
from src.schemas import GetFriendsResponse
from src import handlers

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    setup_sentry(app)


@app.get("/friends/{user_id}", status_code=status.HTTP_200_OK, response_model=GetFriendsResponse)
async def get_friends(user_id: int = Path(..., ge=0, le=2147483647), db: Session = Depends(get_db)):
    return GetFriendsResponse(user=user_id, friends=handlers.get_friends(db, user_id))


@app.post("/friends/{user_id}/{friend_id}")
async def add_friend(user_id: int = Path(..., ge=0, le=2147483647),
                     friend_id: int = Path(..., ge=0, le=2147483647),
                     db: Session = Depends(get_db)):
    if user_id == friend_id:
        content = {
            "detail": [{
                "loc": ["path", "user_id"],
                "msg": f"user_id [{user_id}] cannot be the same as friend_id [{friend_id}]",
                "type": "value_error"
            }]
        }
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    handlers.add_friend(db, user_id, friend_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/friends/{user_id}/{friend_id}")
async def remove_friend(user_id: int = Path(..., ge=0, le=2147483647),
                        friend_id: int = Path(..., ge=0, le=2147483647),
                        db: Session = Depends(get_db)):
    if user_id == friend_id:
        content = {
            "detail": [{
                "loc": ["path", "user_id"],
                "msg": f"user_id [{user_id}] cannot be the same as friend_id [{friend_id}]",
                "type": "value_error"
            }]
        }
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    handlers.remove_friend(db, user_id, friend_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
