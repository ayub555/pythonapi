from typing import List

from fastapi import APIRouter

from app.database import mysqldbaccess
from app.models.education import Education

router = APIRouter(prefix="/education", tags=["Education"])


@router.get("/", response_model=List[Education])
def get_education():
    return mysqldbaccess.fetch_all("SELECT eduId, education FROM education")


@router.get("/{eduId}", response_model=Education)
def get_education_by_id(eduId: int):
    return mysqldbaccess.fetch_one(
        "SELECT eduId, education FROM education WHERE eduId = %s", (eduId,)
    )
