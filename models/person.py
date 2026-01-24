from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Union
from models.address import Address

class Person(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    address: Union[Address, None] = None
    is_pep: bool