from typing import List, Dict, Optional
from datetime import date


from pydantic import BaseModel, validator


class RelationshipOut(BaseModel):
    custom_id: str
    properties: Optional[Dict[str, str]] = None

    class Config:
        schema_extra = {
            "example": {
                "custom_id": "1097123798123679",
                "properties": {"years_of_experience": "2"}
            }
        }


class RelationshipIn(BaseModel):
    start_node_id: str
    start_node_labels: Optional[List[str]] = None
    end_node_id: str
    end_node_labels: Optional[List[str]] = None
    name: str
    params: Optional[Dict[str, str]] = None

    class Config:
        schema_extra = {
            "example": {
                "start_node_id": "asdkuh1239876",
                "start_node_labels": ["Person"],
                "end_node_id": "29481086230",
                "end_node_labels": ["Skill"],
                "name": "KNOWS",
                "params": {"years_of_experience": "2"}
            }
        }