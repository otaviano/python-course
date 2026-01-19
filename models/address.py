from uuid import uuid4
from pydantic import BaseModel, Field

class Address(BaseModel):
    id: str
    street: str
    number: int
    neighbor: str
    city: str
