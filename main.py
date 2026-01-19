from fastapi import FastAPI
from features.create_person.create_person_command_handler import CreatePersonCommandHandler
from features.create_person.create_person_command import CreatePersonCommand

app = FastAPI()
mock_db = {}

@app.get("/")
def read_root():
    return {"Message": "Hello, World! asdasd"}

@app.get("/person/{item_id}")
async def read_item(item_id: str):
    ...
  
    return {"error": "Item not found"}

@app.get("/person/")
async def read_items():
    ...
    

@app.post("/person/", status_code=201)
async def create_item(cmd: CreatePersonCommand):
    handler = CreatePersonCommandHandler(mock_db)
    user_id = await handler.handle_create_person(cmd)
    return user_id
