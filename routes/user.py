from fastapi import APIRouter, HTTPException, status
from config.db import conn
from models.user import users
from schemas.user import User
from typing import List

user = APIRouter()

@user.get("/users", response_model=List[User], tags=["Users"])
def get_all_users():
    try:
        return conn.execute(users.select()).fetchall()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.commit()

@user.post("/users", response_model=User, tags=["Users"])
def create_user(user: User):
    try:
        new_user = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "password": user.password}
        result = conn.execute(users.insert().values(new_user))
        return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.commit()

@user.get("/users/{id}", response_model=User, tags=["Users"])
def get_user(id: int):
    try:
        user = conn.execute(users.select().where(users.c.id == id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.commit()

@user.put("/users/{id}", response_model=User, tags=["Users"])
def update_user(id: int, user: User):
    try:
        conn.execute(users.update().where(users.c.id == id).values(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password))
        return conn.execute(users.select().where(users.c.id == id)).first()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.commit()

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: int):
    try:
        deleted = conn.execute(users.delete().where(users.c.id == id))
        if deleted.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return {"message": "User with id {} deleted successfully!".format(id)}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.commit()
