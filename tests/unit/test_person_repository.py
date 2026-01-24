import pytest
from unittest.mock import AsyncMock, MagicMock
from models.person import Person
from models.address import Address
from infra.person_repository import PersonRepository
from bson import ObjectId


class TestPersonRepository:
    @pytest.fixture
    def mock_collection(self):
        """Create a mock MongoDB collection"""
        collection = AsyncMock()
        
        # Mock the find method to return a cursor mock directly (not as coroutine)
        cursor_mock = AsyncMock()
        collection.find = MagicMock(return_value=cursor_mock)
        
        return collection

    @pytest.fixture
    def person_repository(self, mock_collection):
        """Create PersonRepository with mocked collection"""
        return PersonRepository(mock_collection)

    @pytest.fixture
    def sample_person(self):
        """Create a sample Person for testing"""
        return Person(
            id="person-123",
            name="John Doe",
            age=30,
            address=Address(
                id="addr-123",
                street="Main Street",
                number=123,
                neighbor="Downtown",
                city="Test City"
            ),
            is_pep=False
        )

    @pytest.mark.asyncio
    async def test_save_person(self, person_repository, mock_collection, sample_person):
        """Test saving a person"""
        # Mock the insert_one result
        mock_result = MagicMock()
        mock_result.inserted_id = ObjectId("507f1f77bcf86cd799439011")
        mock_collection.insert_one.return_value = mock_result

        # Call save method
        result = await person_repository.save(sample_person)

        # Verify the call
        mock_collection.insert_one.assert_called_once()
        call_args = mock_collection.insert_one.call_args[0][0]

        # Check that the person data was passed correctly
        assert call_args["id"] == "person-123"
        assert call_args["name"] == "John Doe"
        assert call_args["age"] == 30
        assert call_args["is_pep"] is False
        assert "address" in call_args

        # Check return value
        assert result == "507f1f77bcf86cd799439011"

    @pytest.mark.asyncio
    async def test_get_all_persons(self, person_repository, mock_collection):
        """Test getting all persons"""
        # Mock documents from database
        mock_docs = [
            {
                "_id": ObjectId("507f1f77bcf86cd799439011"),
                "id": "person-1",
                "name": "John Doe",
                "age": 30,
                "is_pep": False
            },
            {
                "_id": ObjectId("507f1f77bcf86cd799439012"),
                "id": "person-2",
                "name": "Jane Smith",
                "age": 25,
                "is_pep": True
            }
        ]
        
        # Mock the find method to return a mock cursor
        mock_cursor = AsyncMock()
        mock_cursor.to_list.return_value = mock_docs
        mock_collection.find.return_value = mock_cursor

        # Call get_all method
        result = await person_repository.get_all()

        # Verify the call
        mock_collection.find.assert_called_once()
        mock_cursor.to_list.assert_called_once_with(length=None)

        # Check results
        assert len(result) == 2
        assert isinstance(result[0], Person)
        assert result[0].id == "person-1"
        assert result[0].name == "John Doe"
        assert result[1].id == "person-2"
        assert result[1].name == "Jane Smith"

    @pytest.mark.asyncio
    async def test_get_all_persons_empty(self, person_repository, mock_collection):
        """Test getting all persons when collection is empty"""
        mock_cursor = AsyncMock()
        mock_cursor.to_list.return_value = []
        mock_collection.find.return_value = mock_cursor
        
        result = await person_repository.get_all()
        assert result == []

    @pytest.mark.asyncio
    async def test_get_person_by_id_found(self, person_repository, mock_collection, sample_person):
        """Test getting a person by ID when found"""
        person_id = "507f1f77bcf86cd799439011"
        mock_doc = {
            "_id": ObjectId(person_id),
            "id": "person-123",
            "name": "John Doe",
            "age": 30,
            "is_pep": False
        }
        mock_collection.find_one.return_value = mock_doc

        # Call get_by_id method
        result = await person_repository.get_by_id(person_id)

        # Verify the call
        mock_collection.find_one.assert_called_once_with({"_id": ObjectId(person_id)})

        # Check result
        assert result is not None
        assert isinstance(result, Person)
        assert result.id == "person-123"
        assert result.name == "John Doe"

    @pytest.mark.asyncio
    async def test_get_person_by_id_not_found(self, person_repository, mock_collection):
        """Test getting a person by ID when not found"""
        person_id = "507f1f77bcf86cd799439011"
        mock_collection.find_one.return_value = None

        result = await person_repository.get_by_id(person_id)

        mock_collection.find_one.assert_called_once_with({"_id": ObjectId(person_id)})
        assert result is None

    @pytest.mark.asyncio
    async def test_get_person_by_id_with_address(self, person_repository, mock_collection):
        """Test getting a person by ID that has an address"""
        person_id = "507f1f77bcf86cd799439011"
        mock_doc = {
            "_id": ObjectId(person_id),
            "id": "person-123",
            "name": "John Doe",
            "age": 30,
            "address": {
                "id": "addr-123",
                "street": "Main Street",
                "number": 123,
                "neighbor": "Downtown",
                "city": "Test City"
            },
            "is_pep": False
        }
        mock_collection.find_one.return_value = mock_doc

        result = await person_repository.get_by_id(person_id)

        assert result is not None
        assert result.address is not None
        assert isinstance(result.address, Address)
        assert result.address.street == "Main Street"
        assert result.address.city == "Test City"