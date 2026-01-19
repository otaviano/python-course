from fastapi import FastAPI, HTTPException, status
from features.create_person.create_person_command_handler import CreatePersonCommandHandler
from features.create_person.create_person_command import CreatePersonCommand
from features.get_person.get_all_person_query import GetAllPersonQuery
from features.get_person.get_person_query_handler import GetPersonQueryHandler    
from features.get_person.get_person_query import GetPersonQuery
from models.person import Person

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message": "healthy"}

@app.get("/person/{id}")
async def read_item(id: str):
    query = GetPersonQuery(id=id)
    handler = GetPersonQueryHandler()
    person = await handler.handle_get_person(query)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id: '{id}' was not found"
        )

    return person
    
@app.get("/person/")
async def read_items():
    query = GetAllPersonQuery()
    handler = GetPersonQueryHandler()
    people = await handler.handle_get_all_person(query)

    return people
    
@app.post("/person/", status_code=201)
async def create_item(cmd: CreatePersonCommand):
    handler = CreatePersonCommandHandler()
    id = await handler.handle_create_person(cmd)
    
    return id
