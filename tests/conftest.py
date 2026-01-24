import pytest
from unittest.mock import MagicMock, patch, AsyncMock


@pytest.fixture(scope="session", autouse=True)
def mock_motor_client():
    """Mock the motor client for all integration tests"""
    with patch('motor.motor_asyncio.AsyncIOMotorClient') as mock_client_class:
        mock_client = MagicMock()
        mock_database = MagicMock()
        mock_collection = MagicMock()
        
        mock_client_class.return_value = mock_client
        mock_client.__getitem__.return_value = mock_database
        mock_database.__getitem__.return_value = mock_collection
        
        # Set up async mock behaviors
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="507f1f77bcf86cd799439011"))
        mock_collection.find_one = AsyncMock(return_value=None)
        mock_collection.find = MagicMock(return_value=MagicMock())
        mock_collection.find.return_value.to_list = AsyncMock(return_value=[])
        
        yield