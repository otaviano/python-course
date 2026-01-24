from ast import List
from uuid import uuid4
from features.get_person.get_person_query import GetPersonQuery
from features.get_person.get_all_person_query import GetAllPersonQuery
from models.person import Person
from infra.person_repository import PersonRepository

class GetPersonQueryHandler:
    def __init__(self, repo: PersonRepository):
        self.repo = repo

    async def handle_get_person(self, query: GetPersonQuery) -> Person:
        person = await self.repo.get_by_id(query.id)

        return person
 
    async def handle_get_all_person(self, query: GetAllPersonQuery) -> List[Person]:
        people = await self.repo.get_all()

        return people
