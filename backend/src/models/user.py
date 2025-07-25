"""User models used by the API."""

from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4


class User(BaseModel):
    """Simple user model."""

    id: str
    username: str
    email: str


# In-memory store for users. This keeps the example lightweight and removes the
# dependency on Flask's SQLAlchemy extension which wasn't included in the
# project dependencies.
_USERS: List[User] = []


def get_users() -> List[User]:
    return list(_USERS)


def create_user(username: str, email: str) -> User:
    user = User(id=str(uuid4()), username=username, email=email)
    _USERS.append(user)
    return user


def get_user(user_id: str) -> Optional[User]:
    return next((u for u in _USERS if u.id == user_id), None)


def update_user(user_id: str, username: Optional[str], email: Optional[str]) -> Optional[User]:
    user = get_user(user_id)
    if user is None:
        return None
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    return user


def delete_user(user_id: str) -> bool:
    user = get_user(user_id)
    if user is None:
        return False
    _USERS.remove(user)
    return True
