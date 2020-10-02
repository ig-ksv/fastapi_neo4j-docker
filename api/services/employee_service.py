from api.daos.employee_dao import EmployeeDAO
from api.models.employee import Employee


class EmployeeService:
    def __init__(self):
        self.employee_dao = EmployeeDAO()

    def add_employee(self, employee: Employee):
        employee = self.employee_dao.add_employee(employee)
        return employee

    def get_employee(self, employee_id):
        employee = self.employee_dao.get_employee_by_id(employee_id)
        return employee

    def find_employees(self, params):
        employees = self.employee_dao.find_employees(params)
        return employees
