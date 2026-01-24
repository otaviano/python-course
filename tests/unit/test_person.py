import pytest
from models.person import Person
from models.address import Address


class TestPerson:
    def test_person_creation_with_address(self):
        """Test creating a Person with an address"""
        address = Address(
            id="addr-123",
            street="Main Street",
            number=123,
            neighbor="Downtown",
            city="Test City"
        )

        person = Person(
            id="person-123",
            name="John Doe",
            age=30,
            address=address,
            is_pep=False
        )

        assert person.id == "person-123"
        assert person.name == "John Doe"
        assert person.age == 30
        assert person.address == address
        assert person.is_pep is False

    def test_person_creation_without_address(self):
        """Test creating a Person without an address"""
        person = Person(
            id="person-456",
            name="Jane Smith",
            age=25,
            is_pep=True
        )

        assert person.id == "person-456"
        assert person.name == "Jane Smith"
        assert person.age == 25
        assert person.address is None
        assert person.is_pep is True

    def test_person_model_dump(self):
        """Test Person model serialization"""
        person = Person(
            id="person-789",
            name="Bob Wilson",
            age=40,
            is_pep=False
        )

        data = person.model_dump()
        expected = {
            "id": "person-789",
            "name": "Bob Wilson",
            "age": 40,
            "address": None,
            "is_pep": False
        }

        assert data == expected

    def test_person_validation(self):
        """Test Person model validation"""
        from pydantic import ValidationError
        
        # Valid person
        person = Person(
            id="valid-id",
            name="Valid Name",
            age=20,
            is_pep=True
        )
        assert person.age == 20

        # Test invalid age (should raise ValidationError)
        with pytest.raises(ValidationError):
            Person(
                id="invalid-id",
                name="Invalid Age",
                age=-5,  # Invalid age
                is_pep=False
            )

    def test_person_equality(self):
        """Test Person equality comparison"""
        person1 = Person(
            id="test-1",
            name="Test Person",
            age=35,
            is_pep=False
        )

        person2 = Person(
            id="test-1",
            name="Test Person",
            age=35,
            is_pep=False
        )

        person3 = Person(
            id="test-2",
            name="Different Person",
            age=35,
            is_pep=False
        )

        assert person1 == person2
        assert person1 != person3