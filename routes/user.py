from fastapi import APIRouter, HTTPException, status
from config.db import conn
from models.user import users
from schemas.user import User
from typing import List

user = APIRouter()

@user.get("/users", response_model=List[User], tags=["Users"])
def get_all_users():
    return conn.execute(users.select()).fetchall()

@user.post("/users", response_model=User, tags=["Users"])
def create_user(user: User):
    new_user = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "password": user.password}
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get("/users/{id}", response_model=User, tags=["Users"])
def get_user(id: int):
    user = conn.execute(users.select().where(users.c.id == id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

@user.put("/users/{id}", response_model=User, tags=["Users"])
def update_user(id: int, user: User):
    conn.execute(users.update().where(users.c.id == id).values(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password))
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: int):
    deleted = conn.execute(users.delete().where(users.c.id == id))
    if deleted.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": "User with id {} deleted successfully!".format(id)}