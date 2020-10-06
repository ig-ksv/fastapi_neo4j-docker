from api.daos.person_dao import PersonDAO
from api.models.person import PersonIn, PERSON_LABELS


class PersonService:
    def __init__(self):
        self.person_dao = PersonDAO()

    def add_person(self, person: PersonIn):
        new_person = self.person_dao.add_person(person)
        return new_person

    def get_person_by_id(self, person_id):
        person = self.person_dao.get_person_by_id(person_id)
        return person

    def delete_person(self, person_id):
        person = self.person_dao.delete_person(person_id)
        return person

    def get_persons(self, params):
        persons = self.person_dao.get_persons(params)
        return persons

    def update_person(self, person_id: str, updated_person: PersonIn):
        person = self.get_person_by_id(person_id)
        result = None
        if person:
            result = self.person_dao.update_person(person_id, updated_person, person)
        return result

    def upload_bulk_csv(self, file_name):
        result = self.person_dao.upload_bulk_csv(file_name)
        return result