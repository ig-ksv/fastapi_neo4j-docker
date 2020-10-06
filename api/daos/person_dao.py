import uuid

from api.models.person import PersonIn, PersonOut, get_label_type
from api.daos.db_connector import neo4j_driver


class PersonDAO:
    def add_person(self, person: PersonIn):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._add_and_return_person, person)
        return result

    @staticmethod
    def _add_and_return_person(tx, person: PersonIn):
        labels = [x for x in person.labels.values()]
        labels = ":".join(labels)
        custom_id = uuid.uuid4()
        query = f"""
                    CREATE (e:{labels}) 
                    SET e.name = '{person.name}' 
                    SET e.surname = '{person.surname}'
                    SET e.date_of_birth = '{person.date_of_birth}'
                    SET e.custom_id = '{custom_id}'
                    RETURN e
                """
        result = tx.run(query)
        person = result.single()[0]
        result = dict(person.items())
        result["labels"] = {get_label_type(label): label for label in list(person.labels)}
        return result

    def get_person_by_id(self, custom_id):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._get_person_by_id, custom_id)
        return result

    @staticmethod
    def _get_person_by_id(tx, custom_id):
        query = f"""
                    MATCH (e:Person)
                    WHERE e.custom_id = '{custom_id}'
                    RETURN e
                """
        result = tx.run(query).single()
        if result:
            person = result[0]
            result = dict(person.items())
            result["labels"] = {get_label_type(label): label for label in list(person.labels)}
            return result

    def delete_person(self, custom_id):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._delete_person, custom_id)
        return result

    @staticmethod
    def _delete_person(tx, custom_id):
        query = f"""
                    MATCH (e:Person)
                    WHERE e.custom_id = '{custom_id}'
                    detach delete e
                """
        result = tx.run(query)
        return result

    def get_persons(self, params):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._get_persons, params)
        return result

    @staticmethod
    def _get_persons(tx, params):
        name = params.get("name", '""')
        surname = params.get("surname", '""')
        email = params.get("email", '""')
        clause = ""
        if params.get("name") and params.get("surname") and params.get("email"):
            clause = f"WHERE e.name = {name} AND e.surname = {surname} AND e.email = {email}"
        elif params.get("name") and params.get("surname"):
            clause = f"WHERE e.name = {name} AND e.surname = {surname}"
        elif params.get("name") and params.get("email"):
            clause = f"WHERE e.name = {name} AND e.email = {email}"
        elif params.get("surname") and params.get("email"):
            clause = f"WHERE e.surname = {surname} AND e.email = {email}"
        elif params.get("name") or params.get("surname") or params.get("email"):
            clause = f"WHERE e.name = {name} OR e.surname = {surname} OR e.email = {email}"
        query = f"""
                    MATCH (e:Person)
                    {clause}
                    RETURN e
                """
        result = tx.run(query)
        result = result.value()
        items = [dict(node.items()) for node in result]
        for index, node in enumerate(result):
            items[index]["labels"] = {get_label_type(label): label for label in list(node.labels)}
        return items

    def update_person(self, person_id: str, new_person: PersonIn, person: PersonOut):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._update_persons, person_id, new_person, person)
        return result

    @staticmethod
    def _update_persons(tx, custom_id: str, new_person: PersonIn, person):
        new_person = new_person.dict()
        new_labels = new_person.pop("labels")

        clause = ""
        for key, value in new_person.items():
            clause += f"SET e.{key} = '{value}' "

        labels_clause = "REMOVE e"
        for key, value in person["labels"].items():
            labels_clause += f":{value}"

        new_labels_clause = "SET e"
        for key, value in new_labels.items():
            new_labels_clause += f":{value}"
        query = f"""
                    MATCH (e:Person)
                    WHERE e.custom_id = '{custom_id}'
                    SET e.custom_id = '{custom_id}'
                    {clause}
                    {labels_clause}
                    {new_labels_clause}
                    RETURN e
                """
        result = tx.run(query).single()
        if result:
            person = result[0]
            result = dict(person.items())
            result["labels"] = {get_label_type(label): label for label in list(person.labels)}
            return result

    def upload_bulk_csv(self, file_name: str):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._upload_bulk_csv, file_name)
        return result

    @staticmethod
    def _upload_bulk_csv(tx, file_name: str):
        query = f"""
                    CALL apoc.load.csv('{file_name}', {{sep: '|', mapping:{{LABELS: {{array:true, arraySep:','}}}}}}) 
                    YIELD map
                    CALL apoc.merge.node(['Person'] + map.LABELS, {{name: map.name, 
                                                       surname: map.surname, 
                                                       email: map.email}}, 
                                                     {{custom_id: map.custom_id,
                                                       name: map.name, 
                                                       surname: map.surname, 
                                                       email: map.email, 
                                                       date_of_birth: map.date_of_birth}})
                    YIELD node
                    RETURN count(*) as number
                 """
        try:
            result = tx.run(query)
        except Exception as e:
            raise Exception(f"Import failed -{e}")
        else:
            return f"Data has been successfully loaded - {result.single()['number']} rows"

