from abc import ABC, abstractmethod
import os

class Settings(ABC):
    @property
    @abstractmethod
    def mongo_connection(self) -> str:
        pass
    @property
    @abstractmethod
    def mongo_database(self) -> str:
        pass
    @property
    @abstractmethod
    def mongo_collection(self) -> str:
        pass

    @property
    @abstractmethod
    def debug(self) -> bool:
        pass

    def log_config(self):
        print(f"Running with DEBUG={self.debug}")
        pass

class DevelopmentSettings(Settings):
    def __init__(self):
        self._mongo_connection = "mongodb://rootuser:securepassword@mongodb:27017"
        self._mongo_database_name = 'personapi_db'
        self._mongo_collection_name = 'persons'

    @property
    def mongo_connection(self) -> str:
        return self._mongo_connection
    
    @property
    def mongo_database(self) -> str:
        return self._mongo_database_name
    
    @property
    def mongo_collection(self) -> str:
        return self._mongo_collection_name

    @property
    def debug(self):
        return True

class ProductionSettings(Settings):
    def __init__(self):
        self._mongo_connection = os.environ.get("PROD_DB_URL")
        self._mongo_database_name = 'personapi_db'
        self._mongo_collection_name = 'persons'

    @property
    def mongo_connection(self) -> str:
        return self._mongo_connection
    
    @property
    def mongo_database(self) -> str:
        return self._mongo_database_name
    
    @property
    def mongo_collection(self) -> str:
        return self._mongo_collection_name

    @property
    def debug(self):
        return True
