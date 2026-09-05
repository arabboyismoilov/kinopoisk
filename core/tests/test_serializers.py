from core.serializers import RegisterSerializer
import pytest

@pytest.mark.django_db
def test_register_serializer_success():
    data = {
        "username": "ali23787238",
        "password": "1234"
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid()
    

@pytest.mark.django_db
def test_register_serializer_fail_on_not_providing_password():
    data = {
        "username": "ali",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert 'password' in serializer.errors
    