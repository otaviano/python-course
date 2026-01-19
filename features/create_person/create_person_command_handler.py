from uuid import uuid4
#from automapper import mapper
from models.person import Person
from features.create_person.create_person_command import CreatePersonCommand

class CreatePersonCommandHandler:
    def __init__(self, db):
        self.db = db

    async def handle_create_person(self, cmd: CreatePersonCommand) -> str:
        # person = mapper.to(Person).map(cmd).map_attr("address", {
        #     "id": str(uuid4()),
        #     "street": cmd.street,
        #     "number": cmd.number,
        #     "neighbor": cmd.neighbor,
        #     "city": cmd.city
        # }).execute()

        ... # Save person in mongo        
              
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

        return person.id
