from models.person import Person
from bson import ObjectId
from typing import Optional

class PersonRepository:
    def __init__(self, collection):
        self.collection = collection

    async def save(self, item: Person) -> str:
        item_dict = item.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(item_dict)
        return str(result.inserted_id)

    async def get_all(self) -> list[Person]:
        docs = await self.collection.find().to_list(length=None)
        return [Person(**{k: v for k, v in doc.items() if k != "_id"}) for doc in docs]
    

    async def get_by_id(self, id: str) -> Optional[Person]:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            return Person(**{k: v for k, v in doc.items() if k != "_id"})
        
        return None