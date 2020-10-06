import os
import shutil
from typing import List, Dict
from fastapi import APIRouter, File, UploadFile

from api.daos.relationship_dao import RelationshipDAO
from api.models.relationship import RelationshipIn, RelationshipOut

router = APIRouter()
relationship_dao = RelationshipDAO()


@router.post("/", response_model=RelationshipOut)
async def add_relationship(relationship: RelationshipIn):
    result = relationship_dao.add_relationship(relationship)
    return result


@router.post("/import-csv/")
async def create_upload_file(file: UploadFile = File(...,
                                                     description="""Only accepts .csv files with next format: \n
                                                                    start_node_id|role|end_node_id \n
                                                                    1234123|KNOW|13241234\n \n
                                                                    get existing node ids before
                                                                 """)):
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "db", "import"))
    try:
        with open(os.path.join(file_path, file.filename), "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise Exception(f"File is invalid - {e}")
    else:
        result = relationship_dao.upload_bulk_csv(file.filename)
        os.remove(os.path.join(file_path, file.filename))
    return result