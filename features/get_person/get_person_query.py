from pydantic import BaseModel

class GetPersonQuery(BaseModel):
    id: str
