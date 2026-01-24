from motor.motor_asyncio import AsyncIOMotorClient
from settings import Settings

class Database:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncIOMotorClient(settings.mongo_connection)
        self.database = self.client[settings.mongo_database]
        self.persons_collection = self.database[settings.mongo_collection]

    async def close_connection(self):
        self.client.close()

def get_database(settings: Settings):
    return Database(settings)