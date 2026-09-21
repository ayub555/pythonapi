from pydantic import BaseModel


class State(BaseModel):
    stateid: int
    statename: str
