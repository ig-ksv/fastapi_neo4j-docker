import os

from fastapi.testclient import TestClient
from api.app import app
from api.daos.db_connector import neo4j_driver
from api.daos.person_dao import PersonDAO
from api.models.person import PersonIn

client = TestClient(app)


class TestUM:
    @staticmethod
    def clear_db(tx):
        query = "match (n) detach delete n"
        tx.run(query)

    def setup_class(cls):
        neo4j_driver.uri = "bolt://localhost:8687"
        neo4j_driver.open_connection()
        cls.person_dao = PersonDAO()

    def teardown_class(cls):
        neo4j_driver.close_connection()

    def setup_method(self, test_method):
        pass

    def teardown_method(self):
        with neo4j_driver.driver.session() as session:
            session.write_transaction(self.clear_db)

    def test_get_persons_no_data(self):
        response = client.get("persons/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_persons(self):
        test_person_1 = PersonIn(name="Mark", surname="Doe", email="mark@gmail.com",
                                 date_of_birth="2020-10-10", labels={"role": "Employee", "department": "Production",
                                                                     "position": "QA", "status": "Active"})
        test_person_2 = PersonIn(name="Tom", surname="Doe", email="tom@gmail.com",
                                 date_of_birth="2020-10-10", labels={"role": "Employee", "department": "Production",
                                                                     "position": "QA", "status": "Active"})
        self.person_dao.add_person(test_person_1)
        self.person_dao.add_person(test_person_2)

        response = client.get("persons/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_persons_by_id_no_data(self):
        random_id = "20981237089712"
        response = client.get(f"persons/{random_id}")
        assert response.status_code == 200
        assert response.json() is None

    def test_get_persons_by_id(self):
        test_person_1 = PersonIn(name="Mark", surname="Doe", email="mark@gmail.com",
                                 date_of_birth="2020-10-10", labels={"role": "Employee", "department": "Production",
                                                                     "position": "QA", "status": "Active"})
        test_person_2 = PersonIn(name="Tom", surname="Doe", email="tom@gmail.com",
                                 date_of_birth="2020-10-10", labels={"role": "Employee", "department": "Production",
                                                                     "position": "QA", "status": "Active"})
        person_1 = self.person_dao.add_person(test_person_1)
        person_2 = self.person_dao.add_person(test_person_2)

        response_1 = client.get(f"persons/{person_1.get('custom_id')}")
        response_2 = client.get(f"persons/{person_2.get('custom_id')}")
        assert response_1.status_code == 200
        assert response_1.json()["name"] == test_person_1.name
        assert response_2.status_code == 200
        assert response_2.json()["name"] == test_person_2.name

    def test_add_person(self):
        test_person = {"name": "Mark", "surname":"Doe", "email": "mark@gmail.com", "date_of_birth": "2020-10-10",
                       "labels": {"role": "Employee", "department": "Production", "position": "QA", "status": "Active"}}

        response = client.post(f"persons/", json=test_person)
        assert response.status_code == 200
        assert response.json()["name"] == test_person["name"]

    def test_add_person_name_error(self):
        test_person = {"surname": "Doe", "email": "mark@gmail.com", "date_of_birth": "2020-10-10",
                       "labels": {"role": "Employee", "department": "Production", "position": "QA", "status": "Active"}}

        expected_error = {'detail': [{'loc': ['body', 'name'], 'msg': 'field required', 'type': 'value_error.missing'}]}

        response = client.post(f"persons/", json=test_person)
        assert response.status_code == 422
        assert response.json() == expected_error

    def test_add_person_surname_error(self):
        test_person = {"name": "Doe", "email": "mark@gmail.com", "date_of_birth": "2020-10-10",
                       "labels": {"role": "Employee", "department": "Production", "position": "QA", "status": "Active"}}

        expected_error = {'detail': [{'loc': ['body', 'surname'], 'msg': 'field required', 'type': 'value_error.missing'}]}

        response = client.post(f"persons/", json=test_person)
        assert response.status_code == 422
        assert response.json() == expected_error

    def test_add_person_date_error(self):
        test_person = {"name": "Mark", "surname": "Doe", "email": "mark@gmail.com",
                       "labels": {"role": "Employee", "department": "Production", "position": "QA", "status": "Active"}}

        expected_error = {'detail': [{'loc': ['body', 'date_of_birth'], 'msg': 'field required', 'type': 'value_error.missing'}]}

        response = client.post(f"persons/", json=test_person)
        assert response.status_code == 422
        assert response.json() == expected_error