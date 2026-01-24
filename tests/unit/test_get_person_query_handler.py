import pytest
from unittest.mock import AsyncMock
from features.get_person.get_person_query_handler import GetPersonQueryHandler
from features.get_person.get_person_query import GetPersonQuery
from features.get_person.get_all_person_query import GetAllPersonQuery
from models.person import Person
from models.address import Address


class TestGetPersonQueryHandler:
    @pytest.fixture
    def mock_repository(self):
        """Create a mock PersonRepository"""
        repo = AsyncMock()
        return repo

    @pytest.fixture
    def query_handler(self, mock_repository):
        """Create GetPersonQueryHandler with mocked repository"""
        return GetPersonQueryHandler(mock_repository)

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
    async def test_handle_get_person_found(self, query_handler, mock_repository, sample_person):
        """Test getting a person by ID when found"""
        # Setup mock
        mock_repository.get_by_id.return_value = sample_person

        # Create query
        query = GetPersonQuery(id="person-123")

        # Call handler
        result = await query_handler.handle_get_person(query)

        # Verify repository was called correctly
        mock_repository.get_by_id.assert_called_once_with("person-123")

        # Verify result
        assert result == sample_person
        assert result.id == "person-123"
        assert result.name == "John Doe"

    @pytest.mark.asyncio
    async def test_handle_get_person_not_found(self, query_handler, mock_repository):
        """Test getting a person by ID when not found"""
        # Setup mock to return None
        mock_repository.get_by_id.return_value = None

        # Create query
        query = GetPersonQuery(id="non-existent-id")

        # Call handler
        result = await query_handler.handle_get_person(query)

        # Verify repository was called correctly
        mock_repository.get_by_id.assert_called_once_with("non-existent-id")

        # Verify result
        assert result is None

    @pytest.mark.asyncio
    async def test_handle_get_all_persons(self, query_handler, mock_repository, sample_person):
        """Test getting all persons"""
        # Setup mock
        people_list = [sample_person]
        mock_repository.get_all.return_value = people_list

        # Create query
        query = GetAllPersonQuery()

        # Call handler
        result = await query_handler.handle_get_all_person(query)

        # Verify repository was called correctly
        mock_repository.get_all.assert_called_once()

        # Verify result
        assert result == people_list
        assert len(result) == 1
        assert result[0] == sample_person

    @pytest.mark.asyncio
    async def test_handle_get_all_persons_empty(self, query_handler, mock_repository):
        """Test getting all persons when list is empty"""
        # Setup mock
        mock_repository.get_all.return_value = []

        # Create query
        query = GetAllPersonQuery()

        # Call handler
        result = await query_handler.handle_get_all_person(query)

        # Verify result
        assert result == []
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_handle_get_all_persons_multiple(self, query_handler, mock_repository):
        """Test getting multiple persons"""
        # Create multiple persons
        person1 = Person(id="person-1", name="John", age=30, is_pep=False)
        person2 = Person(id="person-2", name="Jane", age=25, is_pep=True)
        person3 = Person(id="person-3", name="Bob", age=40, is_pep=False)

        people_list = [person1, person2, person3]
        mock_repository.get_all.return_value = people_list

        query = GetAllPersonQuery()
        result = await query_handler.handle_get_all_person(query)

        assert len(result) == 3
        assert result[0].name == "John"
        assert result[1].name == "Jane"
        assert result[2].name == "Bob"

    def test_query_handler_initialization(self, mock_repository):
        """Test that query handler initializes correctly"""
        handler = GetPersonQueryHandler(mock_repository)
        assert handler.repo == mock_repository

    @pytest.mark.asyncio
    async def test_repository_error_handling(self, query_handler, mock_repository):
        """Test handling repository errors"""
        # Make repository.get_by_id raise an exception
        mock_repository.get_by_id.side_effect = Exception("Database connection error")

        query = GetPersonQuery(id="person-123")

        with pytest.raises(Exception, match="Database connection error"):
            await query_handler.handle_get_person(query)

    @pytest.mark.asyncio
    async def test_get_all_repository_error_handling(self, query_handler, mock_repository):
        """Test handling repository errors in get_all"""
        mock_repository.get_all.side_effect = Exception("Database error")

        query = GetAllPersonQuery()

        with pytest.raises(Exception, match="Database error"):
            await query_handler.handle_get_all_person(query)