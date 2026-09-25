from typing import List

from fastapi import APIRouter

from app.database import mysqldbaccess
from app.models.employee import Employee, EmployeeCreate, EmployeeUpdate, EmployeeWithDetails

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=List[Employee])
def get_employees():
    return mysqldbaccess.fetch_all("SELECT * FROM employee")


@router.get("/details", response_model=List[EmployeeWithDetails])
def get_employees_with_details():
    return mysqldbaccess.fetch_all(
        "SELECT e.*, s.statename, ed.education AS educationname "
        "FROM employee e "
        "INNER JOIN states s ON e.state = s.stateid "
        "INNER JOIN education ed ON e.education = ed.eduId"
    )


@router.get("/{EmpId}", response_model=Employee)
def get_employee(EmpId: int):
    return mysqldbaccess.fetch_one("SELECT * FROM employee WHERE EmpId = %s", (EmpId,))


@router.post("/", response_model=Employee, status_code=201)
def create_employee(employee: EmployeeCreate):
    new_id = mysqldbaccess.execute(
        "INSERT INTO employee (firstname, surname, job, phoneno, emailId, education, state, dob, joindate) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            employee.firstname,
            employee.surname,
            employee.job,
            employee.phoneno,
            employee.emailId,
            employee.education,
            employee.state,
            employee.dob,
            employee.joindate,
        ),
    )
    return mysqldbaccess.fetch_one("SELECT * FROM employee WHERE EmpId = %s", (new_id,))


@router.put("/{EmpId}", response_model=Employee)
def update_employee(EmpId: int, employee: EmployeeUpdate):
    mysqldbaccess.execute(
        "UPDATE employee SET firstname=%s, surname=%s, job=%s, phoneno=%s, emailId=%s, "
        "education=%s, state=%s, dob=%s, joindate=%s WHERE EmpId=%s",
        (
            employee.firstname,
            employee.surname,
            employee.job,
            employee.phoneno,
            employee.emailId,
            employee.education,
            employee.state,
            employee.dob,
            employee.joindate,
            EmpId,
        ),
    )
    return mysqldbaccess.fetch_one("SELECT * FROM employee WHERE EmpId = %s", (EmpId,))


@router.delete("/{EmpId}", status_code=204)
def delete_employee(EmpId: int):
    mysqldbaccess.execute("DELETE FROM employee WHERE EmpId = %s", (EmpId,))
