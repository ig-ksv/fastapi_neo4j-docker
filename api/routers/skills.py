import os
import shutil
from typing import List
from fastapi import APIRouter, File, UploadFile, Query

from api.daos.skill_dao import SkillDAO
from api.models.skill import SKillIn, SKillOut, SKILL_LABELS

router = APIRouter()
skill_dao = SkillDAO()


@router.get("/", response_model=List[SKillOut])
async def get_skills(name: str = None, labels: List[str] = Query(None)):
    params = {"name": name, "labels": labels}
    result = skill_dao.get_skills(params)
    return result


@router.get("/labels/")
async def get_skills_labels():
    return SKILL_LABELS


@router.post("/", response_model=SKillOut)
async def add_skills(e: SKillIn):
    result = skill_dao.add_skill(e)
    return result


@router.delete("/{custom_id}")
async def delete_skills(custom_id: str):
    result = skill_dao.delete_skill(custom_id)
    return result


@router.post("/import-csv/")
async def create_upload_file(file: UploadFile = File(...,
                                                     description="""Only accepts .csv files with next format: \n
                                                                    custom_id|name|description|LABELS \n
                                                                    92873496|Python|example description|ProgramLanguage \n \n
                                                                    check existing labels - '/labels'
                                                                 """)):
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "db", "import"))
    try:
        with open(os.path.join(file_path, file.filename), "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise Exception(f"File is invalid - {e}")
    else:
        result = skill_dao.upload_bulk_csv(file.filename)
        os.remove(os.path.join(file_path, file.filename))
    return result