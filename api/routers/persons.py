import os
import shutil
from typing import List
from fastapi import APIRouter, File, UploadFile

from api.services.person_service import PersonService
from api.models.person import PersonIn, PersonOut, PERSON_LABELS

router = APIRouter()
person_service = PersonService()


@router.get("/", response_model=List[PersonOut])
async def get_persons(name: str = None, surname: str = None, email: str = None):
    params = {}
    if name:
        params["name"] = name
    if surname:
        params["surname"] = surname
    if email:
        params["email"] = email
    persons = person_service.get_persons(params)
    return persons


@router.get("/{person_id}", response_model=PersonOut)
async def get_persons(person_id: str):
    result = person_service.get_person_by_id(person_id)
    return result


@router.get("/labels/")
async def get_persons():
    return PERSON_LABELS


@router.post("/", response_model=PersonOut)
async def add_persons(e: PersonIn):
    result = person_service.add_person(e)
    return result


@router.delete("/{person_id}")
async def delete_persons(person_id: str):
    result = person_service.delete_person(person_id)
    return result


@router.put(
    path="/{person_id}",
    responses={403: {"description": "Operation forbidden"}},
    response_model=PersonOut
)
async def update_persons(person_id: str,  updated_person: PersonIn):
    result = person_service.update_person(person_id, updated_person)
    return result


@router.post("/import-csv/")
async def create_upload_file(file: UploadFile = File(...,
                                                     description="""Only accepts .csv files with next format: \n
                                                                    custom_id|name|surname|date_of_birth|email|LABELS \n
                                                                    28736248|Leroy|Li|2020-10-10|malfar@gmail.com|Employee, QA \n \n
                                                                    check existing labels - '/labels'
                                                                 """)):
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "db", "import"))
    try:
        with open(os.path.join(file_path, file.filename), "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise Exception(f"File is invalid - {e}")
    else:
        result = person_service.upload_bulk_csv(file.filename)
        os.remove(os.path.join(file_path, file.filename))
    return result
