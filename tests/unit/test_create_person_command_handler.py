import pytest
from unittest.mock import AsyncMock
from features.create_person.create_person_command_handler import CreatePersonCommandHandler
from features.create_person.create_person_command import CreatePersonCommand
from models.person import Person
from models.address import Address


class TestCreatePersonCommandHandler:
    @pytest.fixture
    def mock_repository(self):
        repo = AsyncMock()
        repo.save.return_value = "mock-person-id"
        return repo

    @pytest.fixture
    def command_handler(self, mock_repository):
        return CreatePersonCommandHandler(mock_repository)

    @pytest.fixture
    def sample_command(self):
        return CreatePersonCommand(
            name="John Doe",
            age=30,
            street="Main Street",
            number=123,
            neighbor="Downtown",
            city="Test City",
            is_pep=False
        )

    @pytest.mark.asyncio
    async def test_handle_create_person(self, command_handler, mock_repository, sample_command):
        result = await command_handler.handle_create_person(sample_command)

        mock_repository.save.assert_called_once()

        call_args = mock_repository.save.call_args[0][0]
        person = call_args

        assert isinstance(person, Person)
        assert person.name == "John Doe"
        assert person.age == 30
        assert person.is_pep is False
        assert person.id is not None  # Should have a generated UUID
        assert len(person.id) > 0

        assert person.address is not None
        assert isinstance(person.address, Address)
        assert person.address.street == "Main Street"
        assert person.address.number == 123
        assert person.address.neighbor == "Downtown"
        assert person.address.city == "Test City"
        assert person.address.id is not None  # Should have a generated UUID

        assert result == person.id

    @pytest.mark.asyncio
    async def test_handle_create_person_with_pep(self, command_handler, mock_repository):
        """Test creating a PEP person"""
        command = CreatePersonCommand(
            name="Jane Smith",
            age=45,
            street="Business Ave",
            number=999,
            neighbor="Financial District",
            city="Money City",
            is_pep=True
        )

        result = await command_handler.handle_create_person(command)

        mock_repository.save.assert_called_once()
        person = mock_repository.save.call_args[0][0]

        assert person.name == "Jane Smith"
        assert person.age == 45
        assert person.is_pep is True
        assert person.address.city == "Money City"

    @pytest.mark.asyncio
    async def test_handle_create_person_repository_error(self, command_handler, mock_repository, sample_command):

        mock_repository.save.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await command_handler.handle_create_person(sample_command)

    def test_command_handler_initialization(self, mock_repository):
        handler = CreatePersonCommandHandler(mock_repository)
        assert handler.repo == mock_repository

    @pytest.mark.asyncio
    async def test_person_id_uniqueness(self, command_handler, mock_repository, sample_command):
        result1 = await command_handler.handle_create_person(sample_command)
        result2 = await command_handler.handle_create_person(sample_command)

        assert mock_repository.save.call_count == 2

        person1 = mock_repository.save.call_args_list[0][0][0]
        person2 = mock_repository.save.call_args_list[1][0][0]

        assert person1.id != person2.id
        assert result1 != result2
        