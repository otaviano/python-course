from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://rootuser:securepassword@mongodb:27017")
database = client["personapi_db"]
items_collection = database["persons"]

async def close_connection():
    client.close()