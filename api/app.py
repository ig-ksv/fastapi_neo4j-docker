from fastapi import FastAPI

from api.daos.db_connector import neo4j_driver
from api.services.employee_service import EmployeeService
from api.models.employee import Employee


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    neo4j_driver.open_connection()


@app.on_event("shutdown")
def shutdown_event():
    neo4j_driver.close_connection()


@app.get("/get_employee")
async def get_employee(id: int):
    employee_service = EmployeeService()
    new_employee = employee_service.get_employee(id)
    return new_employee


@app.get("/find_employees")
async def get_employee(name: str = None, surname: str = None):
    parameters = {"name": name if name else '""',
                  "surname": surname if surname else '""'}
    employee_service = EmployeeService()
    new_employee = employee_service.find_employees(parameters)
    return new_employee


@app.post("/add_employee")
async def add_employee(employee: Employee):
    employee_service = EmployeeService()
    new_employee = employee_service.add_employee(employee)
    return new_employee

