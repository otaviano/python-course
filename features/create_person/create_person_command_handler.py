from uuid import uuid4
from models.person import Person
from features.create_person.create_person_command import CreatePersonCommand
from infra.person_repository import PersonRepository

class CreatePersonCommandHandler:
    def __init__(self, repo: PersonRepository):
        self.repo = repo

    async def handle_create_person(self, cmd: CreatePersonCommand) -> str:
        person = Person(
            id=str(uuid4()),
            name=cmd.name,
            age=cmd.age,
            address={
                 "id": str(uuid4()),
                 "street": cmd.street,
                 "number": cmd.number,
                 "neighbor": cmd.neighbor,
                 "city": cmd.city
             },
            is_pep=cmd.is_pep
        )

        await self.repo.save(person)

        return person.id
 