from typing import List, Dict, Optional
from datetime import date


from pydantic import BaseModel, validator

PERSON_LABELS = {
    "base_label": ["Person"],
    "role": ["Employee", "Contractor", "Consultant"],
    "department": ["Production", "Administration", "Sales", "Finance"],
    "position": ["SoftwareDeveloper", "QA", "DevOps", "OfficeAdministrator", "AccountExecutive",
                 "SalesOperationsManager", "FinancialAdvisor", "Financemanager"],
    "status": ["TrialPeriod", "Intern", "Former", "Active"]
}


def get_label_type(label):
    for label_type, labels in PERSON_LABELS.items():
        if label in labels:
            return label_type
    return None


class PersonOut(BaseModel):
    custom_id: str
    name: str
    surname: str
    email: str = None
    date_of_birth: date
    labels: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "custom_id": "1097123798123679",
                "name": "Tom",
                "email": "employee@gmail.com",
                "surname": "Doe",
                "date_of_birth": "2010-11-23",
                "labels": {
                    "role": "Employee",
                    "department": "Production",
                    "position": "SoftwareDeveloper",
                    "status": "Trial Period"
                }
            }
        }


class PersonIn(BaseModel):
    name: str
    surname: str
    email: str = None
    date_of_birth: date
    labels: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Tom",
                "surname": "Doe",
                "email": "employee@gmail.com",
                "date_of_birth": "2010-11-23",
                "labels": {
                    "role": "Employee",
                    "department": "Production",
                    "position": "SoftwareDeveloper",
                    "status": "TrialPeriod"
                }
            }
        }

    @validator("name")
    def name_validation(cls, v):
        result = v.strip()
        if len(result.split()) > 1:
            raise ValueError("Name must be a one word")
        return result.capitalize()

    @validator("surname")
    def surname_validation(cls, v):
        result = v.strip()
        if len(result.split()) > 1:
            raise ValueError("Surname must be a one word")
        return result.capitalize()

    @validator("email")
    def email_validation(cls, v):
        return v

    @validator("date_of_birth")
    def birth_date_validation(cls, v):
        # need to add validation
        return v

    @validator("labels")
    def labels_validation(cls, values):
        result = {}

        role = values.get("role")
        department = values.get("department")
        position = values.get("position")
        status = values.get("status")

        result["base_label"] = PERSON_LABELS["base_label"][0]
        result["role"] = cls.role_validation(role)
        result["department"] = cls.department_validation(department)
        result["position"] = cls.position_validation(position)
        result["status"] = cls.status_validation(status)

        return result

    @staticmethod
    def role_validation(role):
        if role not in PERSON_LABELS["role"]:
            raise ValueError("Invalid label - role")
        return role

    @staticmethod
    def department_validation(department):
        if department not in PERSON_LABELS["department"]:
            raise ValueError("Invalid label - department")
        return department

    @staticmethod
    def position_validation(position):
        if position not in PERSON_LABELS["position"]:
            raise ValueError("Invalid label - position")
        return position

    @staticmethod
    def status_validation(status):
        if status not in PERSON_LABELS["status"]:
            raise ValueError("Invalid label - status")
        return status
