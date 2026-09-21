from typing import List

from fastapi import APIRouter

from app.database import mysqldbaccess
from app.models.state import State

router = APIRouter(prefix="/states", tags=["States"])


@router.get("/", response_model=List[State])
def get_states():
    return mysqldbaccess.fetch_all("SELECT stateid, statename FROM states")


@router.get("/{stateid}", response_model=State)
def get_state(stateid: int):
    return mysqldbaccess.fetch_one(
        "SELECT stateid, statename FROM states WHERE stateid = %s", (stateid,)
    )
