from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Union
from models.address import Address

class Person(BaseModel):
    id: str
    name: str
    age: int
    address: Union[Address, None] = None
    is_pep: bool