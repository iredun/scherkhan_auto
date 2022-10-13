from datetime import date
from typing import List

from pydantic import BaseModel

from scherkhan.models.car import Car


class User(BaseModel):
    pk: int
    username: str
    email: str
    phone: str
    first_name: str
    last_name: str
    patronymic: str
    gender: str
    birth_date: date
    locale: str
    time_zone: str
    driver_license: str
    is_verified: bool

    cars: List[Car] = []

    def __repr__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"
