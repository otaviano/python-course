import pytest
from models.address import Address


class TestAddress:
    def test_address_creation(self):
        address = Address(
            id="addr-123",
            street="Main Street",
            number=123,
            neighbor="Downtown",
            city="Test City"
        )

        assert address.id == "addr-123"
        assert address.street == "Main Street"
        assert address.number == 123
        assert address.neighbor == "Downtown"
        assert address.city == "Test City"

    def test_address_model_dump(self):
        address = Address(
            id="addr-456",
            street="Oak Avenue",
            number=456,
            neighbor="Suburb",
            city="Another City"
        )

        data = address.model_dump()
        expected = {
            "id": "addr-456",
            "street": "Oak Avenue",
            "number": 456,
            "neighbor": "Suburb",
            "city": "Another City"
        }

        assert data == expected

    def test_address_validation(self):
        address = Address(
            id="valid-addr",
            street="Valid Street",
            number=100,
            neighbor="Valid Neighbor",
            city="Valid City"
        )
        assert address.number == 100

        # Test invalid number (should raise ValidationError)
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            Address(
                id="invalid-addr",
                street="Invalid Street",
                number=-10,  # Invalid number
                neighbor="Invalid Neighbor",
                city="Invalid City"
            )

    def test_address_equality(self):
        address1 = Address(
            id="addr-1",
            street="First Street",
            number=10,
            neighbor="Area 1",
            city="City 1"
        )

        address2 = Address(
            id="addr-1",
            street="First Street",
            number=10,
            neighbor="Area 1",
            city="City 1"
        )

        address3 = Address(
            id="addr-2",
            street="Second Street",
            number=20,
            neighbor="Area 2",
            city="City 2"
        )

        assert address1 == address2
        assert address1 != address3
