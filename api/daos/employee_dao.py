from api.models.employee import Employee
from api.daos.db_connector import neo4j_driver


class EmployeeDAO:
    def add_employee(self, employee: Employee):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._add_and_return_employee, employee)
        return result

    @staticmethod
    def _add_and_return_employee(tx, employee: Employee):
        query = f"""
                    CREATE (e:Employee:{employee.sex}) 
                    SET e.name = '{employee.name}' 
                    SET e.surname = '{employee.surname}'
                    SET e.birth_date = '{employee.birth_date}'
                    RETURN e
                """
        result = tx.run(query)
        return result.single()[0]

    def get_employee_by_id(self, employee_id):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._get_employee_by_id, employee_id)
        return result

    @staticmethod
    def _get_employee_by_id(tx, employee_id):
        query = f"""
                    MATCH (e:Employee)
                    WHERE ID(e) = {employee_id}
                    RETURN e
                """
        result = tx.run(query)
        return result.data()[0].get("e")

    def find_employees(self, params):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._find_and_return_employees, params)
        return result

    @staticmethod
    def _find_and_return_employees(tx, params):
        name = params.get("name", "")
        surname = params.get("surname", "")
        query = f"""
                    MATCH (e:Employee)
                    WHERE e.name = {name} OR e.surname = {surname}
                    RETURN e
                """
        print(query)
        result = tx.run(query)
        return result.data()