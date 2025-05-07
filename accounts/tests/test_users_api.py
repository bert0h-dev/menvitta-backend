import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email="admin@test.com",
        password="AdminPass123!",
        first_name="Admin",
        last_name="User",
        user_type="admin"
    )

@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        email="staff@test.com",
        password="StaffPass123!",
        first_name="Staff",
        last_name="User",
        user_type="staff"
    )

@pytest.fixture
def normal_user(db):
    return User.objects.create_user(
        email="user@test.com",
        password="UserPass123!",
        first_name="Normal",
        last_name="User",
        user_type="user",
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def staff_client(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    return api_client

@pytest.fixture
def user_client(api_client, normal_user):
    api_client.force_authenticate(user=normal_user)
    return api_client

@pytest.mark.django_db
class TestUserViewSet:
    def test_list_users(self, auth_client, admin_user, staff_user, normal_user):
        url = reverse("user-list")
        response = auth_client.get(url)
        print("RESPONSE DATA:", response.data)
        assert response.status_code == status.HTTP_200_OK
        users = response.data.get("data", {}).get("results", [])
        assert isinstance(users, list), f"Expected a list, got {type(users)}: {users}"
        emails = [u["email"] for u in users]
        assert admin_user.email in emails
        assert staff_user.email in emails
        assert normal_user.email in emails

    def test_create_user(self, auth_client):
        url = reverse("user-list")
        payload = {
            "email": "newuser@test.com",
            "password": "NewUser123!",
            "password2": "NewUser123!",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "user_type": "user",
        }
        response = auth_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@test.com").exists()

    def test_retrieve_user(self, auth_client, normal_user):
        url = reverse("user-detail", args=[normal_user.id])
        response = auth_client.get(url)
        print("RESPONSE DATA RETRIEVE:", response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["email"] == normal_user.email

    def test_update_user(self, auth_client, normal_user):
        url = reverse("user-detail", args=[normal_user.id])
        payload = {
            "email": normal_user.email,
            "first_name": "Modificado",
            "last_name": "Apellido",
            "user_type": normal_user.user_type,
        }
        response = auth_client.put(url, payload, format="json")
        print("RESPONSE DATA UPDATE:", response.data)
        assert response.status_code == status.HTTP_200_OK
        normal_user.refresh_from_db()
        assert normal_user.first_name == "Modificado"

    def test_partial_update_user(self, auth_client, normal_user):
        url = reverse("user-detail", args=[normal_user.id])
        payload = {
            "first_name": "Parcial"
        }
        response = auth_client.patch(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        normal_user.refresh_from_db()
        assert normal_user.first_name == "Parcial"

    def test_delete_user(self, auth_client, normal_user):
        url = reverse("user-detail", args=[normal_user.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=normal_user.id).exists()

    def test_create_user_invalid_password(self, auth_client):
        url = reverse("user-list")
        payload = {
            "email": "badpass@test.com",
            "password": "short",
            "password2": "short",
            "first_name": "Bad",
            "last_name": "Password",
            "user_type": "user",
        }
        response = auth_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data["errors"]

    def test_permissions_required(self, api_client, normal_user):
        url = reverse("user-list")
        response = api_client.get(url)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)

@pytest.mark.django_db
class TestChangePasswordView:
    def test_change_password_success(self, auth_client, normal_user):
        url = reverse("user-change-password", args=[normal_user.id])
        payload = {
            "current_password": normal_user.password,
            "new_password": "NewPass123!",
            "confirm_password": "NewPass123!"
        }
        response = auth_client.put(url, payload, format="json")
        print("RESPONSE DATA UPDATE PASSWORD:", response.data)
        assert response.status_code == status.HTTP_200_OK
        normal_user.refresh_from_db()
        assert normal_user.check_password("NewPass123!")

    def test_change_password_invalid(self, auth_client, normal_user):
        url = reverse("user-change-password", args=[normal_user.id])
        payload = {
            "current_password": normal_user.password,
            "new_password": "short",
            "confirm_password": "short"
        }
        response = auth_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in str(response.data["errors"]).lower()

    def test_change_password_forbidden(self, staff_client, normal_user):
        url = reverse("user-change-password", args=[normal_user.id])
        payload = {
            "current_password": normal_user.password,
            "new_password": "AnotherPass123!",
            "confirm_password": "AnotherPass123!"
        }
        # Staff can change, but normal user cannot
        response = staff_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestChangeUserLanguageView:
    def test_change_language_success(self, user_client, normal_user):
        url = reverse("user-change-language", args=[normal_user.id])
        payload = {"language": "es"}
        response = user_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        normal_user.refresh_from_db()
        assert normal_user.language == "es"

    def test_change_language_forbidden(self, user_client, staff_user):
        url = reverse("user-change-language", args=[staff_user.id])
        payload = {"language": "en"}
        response = user_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_change_language_invalid(self, user_client, normal_user):
        url = reverse("user-change-language", args=[normal_user.id])
        payload = {"language": "xx"}
        response = user_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "language" in response.data["errors"]