import pytest
from rest_framework.exceptions import ValidationError

from accounts.serializers.permissions_serializer import (
    PermissionNameRequestSerializer,
    PermissionNameResponseSerializer
)

@pytest.mark.django_db
class TestPermissionNameRequestSerializer:
    def test_valid_permission_ids(self):
        data = {"permission_ids": [1, 2, 3]}
        serializer = PermissionNameRequestSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["permission_ids"] == [1, 2, 3]

    def test_empty_permission_ids(self):
        data = {"permission_ids": []}
        serializer = PermissionNameRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "permission_ids" in serializer.errors

    def test_invalid_permission_id_type(self):
        data = {"permission_ids": [1, "a", 3]}
        serializer = PermissionNameRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "permission_ids" in serializer.errors

    def test_permission_id_less_than_one(self):
        data = {"permission_ids": [0, 2]}
        serializer = PermissionNameRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "permission_ids" in serializer.errors

@pytest.mark.django_db
class TestPermissionNameResponseSerializer:
    def test_serialize_permission(self):
        data = {"id": 10, "name": "Can view user"}
        serializer = PermissionNameResponseSerializer(data)
        assert serializer.data["id"] == 10
        assert serializer.data["name"] == "Can view user"