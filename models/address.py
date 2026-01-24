from uuid import uuid4
from pydantic import BaseModel, Field

class Address(BaseModel):
    id: str
    street: str = Field(min_length=1, max_length=200)
    number: int = Field(ge=1)
    neighbor: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
