from pydantic import BaseModel


class Education(BaseModel):
    eduId: int
    education: str
