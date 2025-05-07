import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from authentication.serializers.auth_serializer import (
    LoginSerializer,
    LogoutSerializer,
    RefreshTokenSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestLoginSerializer:
    def test_login_success(self):
        user = User.objects.create_user(
            email="testlogin@example.com",
            password="supersecret",
            first_name="Test",
            last_name="Login"
        )
        data = {"email": "testlogin@example.com", "password": "supersecret"}
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        tokens = serializer.validated_data
        assert "access" in tokens
        assert "refresh" in tokens

    def test_login_invalid_email(self):
        data = {"email": "wrong@example.com", "password": "supersecret"}
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "auth" in serializer.errors

    def test_login_invalid_password(self):
        user = User.objects.create_user(
            email="testlogin2@example.com",
            password="supersecret",
            first_name="Test2",
            last_name="Login2"
        )
        data = {"email": "testlogin2@example.com", "password": "wrongpass"}
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "auth" in serializer.errors

@pytest.mark.django_db
class TestLogoutSerializer:
    def test_logout_success(self):
        user = User.objects.create_user(
            email="testlogout@example.com",
            password="supersecret"
        )
        refresh = str(RefreshToken.for_user(user))
        data = {"refresh": refresh}
        serializer = LogoutSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["refresh"] == refresh

    def test_logout_missing_refresh(self):
        data = {
            "refresh": "1772736464737scdcb2341897sdfc"
        }
        serializer = LogoutSerializer(data=data)
        assert not serializer.is_valid()
        assert "auth" in serializer.errors

    def test_logout_invalid_refresh(self):
        data = {"refresh": "invalidtoken"}
        serializer = LogoutSerializer(data=data)
        assert not serializer.is_valid()
        assert "auth" in serializer.errors

@pytest.mark.django_db
class TestRefreshTokenSerializer:
    def test_refresh_token_success(self):
        user = User.objects.create_user(
            email="testrefresh@example.com",
            password="supersecret"
        )
        refresh = str(RefreshToken.for_user(user))
        data = {"refresh": refresh}
        serializer = RefreshTokenSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["refresh"] == refresh

    def test_refresh_token_missing(self):
        data = {
            "refresh": "1772736464737scdcb2341897sdfc"
        }
        serializer = RefreshTokenSerializer(data=data)
        assert not serializer.is_valid()
        assert "auth" in serializer.errors