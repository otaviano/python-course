from functools import lru_cache
from fastapi import FastAPI, HTTPException, status, Depends
from features.create_person.create_person_command_handler import CreatePersonCommandHandler
from features.create_person.create_person_command import CreatePersonCommand
from features.get_person.get_all_person_query import GetAllPersonQuery
from features.get_person.get_person_query_handler import GetPersonQueryHandler    
from features.get_person.get_person_query import GetPersonQuery
from infra.person_repository import PersonRepository
from infra.database import Database
from settings import Settings, DevelopmentSettings, ProductionSettings

app = FastAPI()

@lru_cache
def get_settings() -> Settings:
    import os
    if os.getenv("ENV") == "production":
        return ProductionSettings()
    return DevelopmentSettings()

def get_database(settings: Settings = Depends(get_settings)) -> Database:
    return Database(settings)

def get_person_repository(db: Database = Depends(get_database)) -> PersonRepository:
    return PersonRepository(db.persons_collection)

def get_create_person_handler(repo: PersonRepository = Depends(get_person_repository)) -> CreatePersonCommandHandler:
    return CreatePersonCommandHandler(repo)

def get_get_person_handler(repo: PersonRepository = Depends(get_person_repository)) -> GetPersonQueryHandler:
    return GetPersonQueryHandler(repo)

@app.get("/")
def read_root():
    return {"Message": "healthy"}

@app.get("/person/{id}")
async def read_item(id: str, handler: GetPersonQueryHandler = Depends(get_get_person_handler)):
    query = GetPersonQuery(id=id)
    person = await handler.handle_get_person(query)
    
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id: '{id}' was not found")

    return person
    
@app.get("/person/")
async def read_items(handler: GetPersonQueryHandler = Depends(get_get_person_handler)):
    query = GetAllPersonQuery()
    people = await handler.handle_get_all_person(query)

    return people
    
@app.post("/person/", status_code=201)
async def create_item(cmd: CreatePersonCommand, handler: CreatePersonCommandHandler = Depends(get_create_person_handler)):
    id = await handler.handle_create_person(cmd)
    
    return id
