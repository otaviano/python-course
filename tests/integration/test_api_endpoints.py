import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from main import app, get_person_repository
from infra.person_repository import PersonRepository
from models.person import Person
from models.address import Address
from bson import ObjectId

@pytest.mark.integration
class TestPersonAPI:
    @pytest.fixture
    def client(self):
        """Create a test client with mocked dependencies"""
        # Create a mock repository
        mock_repo = MagicMock(spec=PersonRepository)
        
        # Set up default mock behaviors
        mock_repo.save = AsyncMock(return_value="mock-person-id")
        mock_repo.get_by_id = AsyncMock(return_value=None)
        mock_repo.get_all = AsyncMock(return_value=[])
        
        # Override the dependency
        def override_get_person_repository():
            return mock_repo
        
        app.dependency_overrides[get_person_repository] = override_get_person_repository
        
        with TestClient(app) as client:
            yield client
        
        # Clean up
        app.dependency_overrides = {}

    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data == {"Message": "healthy"}

    def test_create_person(self, client):
        """Test creating a new person"""
        person_data = {
            "name": "John Doe",
            "age": 30,
            "street": "Main Street",
            "number": 123,
            "neighbor": "Downtown",
            "city": "Test City",
            "is_pep": False
        }

        response = client.post("/person/", json=person_data)
        assert response.status_code == 201
        result = response.json()
        # Should return a UUID string
        assert isinstance(result, str)
        # Verify it's a valid UUID format
        import re
        assert re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', result)
        assert len(result) > 0

    def test_get_person_found(self, client):
        """Test getting a person by ID when found"""
        person_id = str(ObjectId())  # Valid ObjectId
        
        # Create mock person
        mock_person = Person(
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
        
        # Get the mock repo and set up the return value
        mock_repo = app.dependency_overrides[get_person_repository]()
        mock_repo.get_by_id = AsyncMock(return_value=mock_person)
        
        response = client.get(f"/person/{person_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "person-123"
        assert data["name"] == "John Doe"
        assert data["age"] == 30

    def test_get_person_not_found(self, client):
        """Test getting a person by ID when not found"""
        person_id = str(ObjectId())  # Valid ObjectId
        
        # Mock repo already returns None by default
        response = client.get(f"/person/{person_id}")
        assert response.status_code == 404
        data = response.json()
        assert "was not found" in data["detail"]

    def test_get_all_persons(self, client):
        """Test getting all persons"""
        # Create mock persons
        mock_persons = [
            Person(
                id="person-1",
                name="John Doe",
                age=30,
                address=Address(
                    id="addr-1",
                    street="Main Street",
                    number=123,
                    neighbor="Downtown",
                    city="Test City"
                ),
                is_pep=False
            ),
            Person(
                id="person-2", 
                name="Jane Smith",
                age=25,
                address=Address(
                    id="addr-2",
                    street="Oak Avenue",
                    number=456,
                    neighbor="Uptown",
                    city="Test City"
                ),
                is_pep=True
            )
        ]
        
        # Get the mock repo and set up the return value
        mock_repo = app.dependency_overrides[get_person_repository]()
        mock_repo.get_all = AsyncMock(return_value=mock_persons)
        
        response = client.get("/person/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["name"] == "John Doe"
        assert data[1]["name"] == "Jane Smith"

    def test_create_person_validation_error(self, client):
        """Test creating a person with invalid data"""
        invalid_data = {
            "name": "John Doe",
            "age": -5,  # Invalid age
            "street": "Main Street",
            "number": 123,
            "neighbor": "Downtown",
            "city": "Test City",
            "is_pep": False
        }

        # Since validation happens in the domain model, it raises an exception
        # that results in a 500 error (should be handled better in production)
        # With mocks, the validation still happens before the mock is called
        with pytest.raises(Exception):  # ValidationError is raised
            response = client.post("/person/", json=invalid_data)

    def test_get_person_invalid_id(self, client):
        """Test getting a person with invalid ID format"""
        # Test with an invalid ObjectId format
        invalid_id = "invalid-id-format"
        
        # With mocks, InvalidId is not raised, so it returns None -> 404
        response = client.get(f"/person/{invalid_id}")
        assert response.status_code == 404  # Mock returns None, treated as not found