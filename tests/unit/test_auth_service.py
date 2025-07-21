from re import A, S
from unittest.mock import AsyncMock, patch
import pytest
from types import SimpleNamespace

from app.account.services.auth_service import register_user_logic, authenticate_user
from app.account.schemas.user import UserCreate
from app.core.exceptions import (
    UserAlreadyExistsError,
    ResourceNotFoundError,
    InvalidCredentialsError,
)


@pytest.fixture
def fake_user_data():
    return UserCreate(
        username="testuser", email="test@example.com", password="secure123"
    )


@pytest.fixture
def path_urls():
    with (
        patch(
            "app.account.services.auth_service.user_repo.check_username_or_email_exists"
        ) as mock_check,
        patch("app.account.services.auth_service.user_repo.save_user_db") as mock_save,
        patch("app.account.services.auth_service.hash_password") as mock_hash,
    ):
        yield {"mock_check": mock_check, "mock_save": mock_save, "mock_hash": mock_hash}


@pytest.mark.asyncio
class TestCreateUser:
    async def test_registers_user_succesfully(self, path_urls, fake_user_data):
        session = AsyncMock()
        path_urls["mock_check"].return_value = None
        path_urls["mock_hash"].return_value = "hashed_password"
        path_urls["mock_save"].return_value = {
            "id": 1,
            "username": fake_user_data.username,
        }
        result = await register_user_logic(session, fake_user_data)

        path_urls["mock_check"].assert_awaited_once_with(
            session=session, user_data=fake_user_data
        )
        path_urls["mock_hash"].assert_awaited_once_with(fake_user_data.password)
        path_urls["mock_save"].assert_awaited_once_with(
            session=session,
            user_data=fake_user_data,
            hashed_password="hashed_password",
        )

        assert result["username"] == "testuser"

    async def test_register_user_already_exists(self, path_urls, fake_user_data):
        session = AsyncMock()
        path_urls["mock_check"].return_value = True
        with pytest.raises(UserAlreadyExistsError):
            await register_user_logic(session, fake_user_data)
        path_urls["mock_save"].assert_not_awaited()
        path_urls["mock_hash"].assert_not_awaited()


@pytest.mark.asyncio
class TestLoginUser:
    async def test_login_user(self, fake_user_data):
        session = AsyncMock()
        with (
            patch(
                "app.account.services.auth_service.user_repo.find_by_username_or_email"
            ) as mock_find,
            patch(
                "app.account.services.auth_service.verify_password", return_value=True
            ) as mock_verify,
        ):
            user = SimpleNamespace(
                username="testuser",
                email="test@example.com",
                hashed_password="hashed_password",
            )
            mock_find.return_value = user

            result = await authenticate_user(
                session=session,
                username_or_email=fake_user_data.username,
                password=fake_user_data.password,
            )
            mock_find.assert_awaited_once_with(
                session=session, identifier=fake_user_data.username
            )
            mock_verify.assert_awaited_once_with(
                fake_user_data.password, user.hashed_password
            )
            assert result == user

    async def test_user_not_register(self, fake_user_data):
        with (
            patch(
                "app.account.services.auth_service.user_repo.find_by_username_or_email"
            ) as mock_find,
            patch("app.account.services.auth_service.verify_password") as mock_verify,
        ):
            session = AsyncMock()
            mock_find.return_value = None
            with pytest.raises(ResourceNotFoundError):
                await authenticate_user(
                    session=session,
                    username_or_email=fake_user_data.username,
                    password=fake_user_data.password,
                )
            mock_find.assert_awaited_once_with(
                session=session, identifier=fake_user_data.username
            )
            mock_verify.assert_not_called()

    async def test_password_incorrect(self, fake_user_data):
        with (
            patch(
                "app.account.services.auth_service.user_repo.find_by_username_or_email"
            ) as mock_find,
            patch("app.account.services.auth_service.verify_password") as mock_verify,
        ):
            session = AsyncMock()

            user = SimpleNamespace(
                username=fake_user_data.username,
                email=fake_user_data.email,
                hashed_password="hashed_haha_wrong",
            )
            mock_find.return_value = user
            mock_verify.return_value = False  # <-- имитируем неверный пароль

            with pytest.raises(InvalidCredentialsError):
                await authenticate_user(
                    session=session,
                    username_or_email=fake_user_data.username,
                    password="wrong_password",
                )

            mock_find.assert_awaited_once_with(
                session=session, identifier=fake_user_data.username
            )
            mock_verify.assert_awaited_once_with("wrong_password", user.hashed_password)



