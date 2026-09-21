from typing import List

from fastapi import APIRouter

from app.database import mysqldbaccess
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
def get_users():
    return mysqldbaccess.fetch_all("SELECT * FROM users")


@router.get("/{userId}", response_model=User)
def get_user(userId: int):
    return mysqldbaccess.fetch_one("SELECT * FROM users WHERE userId = %s", (userId,))


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    new_id = mysqldbaccess.execute(
        "INSERT INTO users (firstname, lastname, phoneno, emailId, username, password, createddate, lastlogin) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            user.firstname,
            user.lastname,
            user.phoneno,
            user.emailId,
            user.username,
            user.password,
            user.createddate,
            user.lastlogin,
        ),
    )
    return mysqldbaccess.fetch_one("SELECT * FROM users WHERE userId = %s", (new_id,))


@router.put("/{userId}", response_model=User)
def update_user(userId: int, user: UserUpdate):
    mysqldbaccess.execute(
        "UPDATE users SET firstname=%s, lastname=%s, phoneno=%s, emailId=%s, "
        "username=%s, password=%s, createddate=%s, lastlogin=%s WHERE userId=%s",
        (
            user.firstname,
            user.lastname,
            user.phoneno,
            user.emailId,
            user.username,
            user.password,
            user.createddate,
            user.lastlogin,
            userId,
        ),
    )
    return mysqldbaccess.fetch_one("SELECT * FROM users WHERE userId = %s", (userId,))


@router.delete("/{userId}", status_code=204)
def delete_user(userId: int):
    mysqldbaccess.execute("DELETE FROM users WHERE userId = %s", (userId,))
