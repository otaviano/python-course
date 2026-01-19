from pydantic import BaseModel

class CreatePersonCommand(BaseModel):
    name: str
    age: int
    street: str
    number: int
    neighbor: str
    city: str
    is_pep: bool
    