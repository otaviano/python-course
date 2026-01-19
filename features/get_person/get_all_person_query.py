from pydantic import BaseModel

class GetAllPersonQuery(BaseModel):
    name: str = None