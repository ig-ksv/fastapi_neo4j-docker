from typing import Optional, Dict
from datetime import date

from pydantic import BaseModel

SKILL_LABELS = {
    "base_label": ["Skill"],
    "skill_type_label": ["Soft", "Hard"],
    "all": ["ProgramLanguage", "Framework", "Library", "Technology", "Script", "DBMS", "CloudService", "Platform"]
}


def get_label_type(label):
    for label_type, labels in SKILL_LABELS.items():
        if label in labels:
            return label_type
    return None


class SKillIn(BaseModel):
    name: str
    description: Optional[str]
    labels: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Python",
                "description": "program language",
                "labels": {
                    "skill_type_label": "Hard",
                    "all": "ProgramLanguage"
                }
            }
        }


class SKillOut(BaseModel):
    custom_id: str
    name: str
    description: Optional[str]
    labels: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "custom_id": "1097123798123679",
                "name": "Python",
                "description": "program language",
                "labels": {
                    "skill_type_label": "Hard",
                    "all": "ProgramLanguage"
                }
            }
        }