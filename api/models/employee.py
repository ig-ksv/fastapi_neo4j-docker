from typing import Optional
from datetime import date

from pydantic import BaseModel


class Employee(BaseModel):
    name: str
    surname: str
    birth_date: date
    start_day: Optional[date] = None
    sex: Optional[str] = None