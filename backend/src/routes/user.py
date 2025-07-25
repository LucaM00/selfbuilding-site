from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from src.models.user import (
    User,
    create_user,
    delete_user,
    get_user,
    get_users,
    update_user,
)


class UserCreate(BaseModel):
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None


router = APIRouter()


@router.get("/users", response_model=List[User])
async def list_users() -> List[User]:
    return get_users()


@router.post("/users", response_model=User, status_code=201)
async def create_user_endpoint(payload: UserCreate) -> User:
    return create_user(payload.username, payload.email)


@router.get("/users/{user_id}", response_model=User)
async def get_user_endpoint(user_id: str) -> User:
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User)
async def update_user_endpoint(user_id: str, payload: UserUpdate) -> User:
    user = update_user(user_id, payload.username, payload.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=204)
async def delete_user_endpoint(user_id: str) -> None:
    if not delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return None
