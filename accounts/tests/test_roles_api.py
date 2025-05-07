
import pytest
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from accounts.serializers.roles_serializer import (
    RolesSerializer,
    AssignRoleSerializer,
    RemoveRoleSerializer
)

User = get_user_model()

@pytest.mark.django_db
class TestRolesSerializer:
    def test_create_role_with_valid_data(self):
        perm = Permission.objects.first()
        data = {
            "name": "Administrador",
            "permissions": [perm.id]
        }
        serializer = RolesSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        role = serializer.save()
        assert role.name == "Administrador"
        assert perm in role.permissions.all()

    def test_create_role_with_empty_name(self):
        perm = Permission.objects.first()
        data = {
            "name": "   ",
            "permissions": [perm.id]
        }
        serializer = RolesSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_create_role_with_duplicate_name(self):
        perm = Permission.objects.first()
        Group.objects.create(name="Soporte")
        data = {
            "name": "Soporte",
            "permissions": [perm.id]
        }
        serializer = RolesSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_update_role_name_and_permissions(self):
        perm1 = Permission.objects.first()
        perm2 = Permission.objects.last()
        group = Group.objects.create(name="Ventas")
        group.permissions.set([perm1])
        data = {
            "name": "Ventas Actualizado",
            "permissions": [perm2.id]
        }
        serializer = RolesSerializer(instance=group, data=data)
        assert serializer.is_valid(), serializer.errors
        updated_group = serializer.save()
        assert updated_group.name == "Ventas Actualizado"
        assert list(updated_group.permissions.all()) == [perm2]

@pytest.mark.django_db
class TestAssignRoleSerializer:
    def test_assign_role_to_user(self):
        user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="1234",
            first_name="Test",
            last_name="User"
        )
        group = Group.objects.create(name="TestRole")
        data = {
            "user_id": user.id,
            "role_id": group.id
        }
        serializer = AssignRoleSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        assert group in user.groups.all()

    def test_assign_role_already_assigned(self):
        user = User.objects.create_user(
            email="testuser2@example.com",
            username="testuser2",
            password="1234",
            first_name="Test2",
            last_name="User2"
        )
        group = Group.objects.create(name="TestRole2")
        user.groups.add(group)
        data = {
            "user_id": user.id,
            "role_id": group.id
        }
        serializer = AssignRoleSerializer(data=data)
        assert not serializer.is_valid()
        assert "role_id" in serializer.errors

@pytest.mark.django_db
class TestRemoveRoleSerializer:
    def test_remove_role_from_user(self):
        user = User.objects.create_user(
            email="testuser3@example.com",
            username="testuser3",
            password="1234",
            first_name="Test3",
            last_name="User3"
        )
        group = Group.objects.create(name="TestRole3")
        user.groups.add(group)
        data = {
            "user_id": user.id,
            "role_id": group.id
        }
        serializer = RemoveRoleSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        assert group not in user.groups.all()

    def test_remove_role_not_assigned(self):
        user = User.objects.create_user(
            email="testuser4@example.com",
            username="testuser4",
            password="1234",
            first_name="Test4",
            last_name="User4"
        )
        group = Group.objects.create(name="TestRole4")
        data = {
            "user_id": user.id,
            "role_id": group.id
        }
        serializer = RemoveRoleSerializer(data=data)
        assert not serializer.is_valid()
        assert "role_id" in serializer.errors
