from datetime import date

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    firstname: str
    surname: str
    job: str
    phoneno: str
    emailId: str
    education: int
    state: int
    dob: date
    joindate: date


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    EmpId: int
