import pytest
from pydantic import SecretStr, ValidationError

from config.app_settings import AppSettings


@pytest.fixture
def valid_settings_data() -> dict[str, str | int]:
    """Provides valid values for the required AppSettings fields."""
    return {
        "secret_key": "test-secret",
        "frontend_origins": "https://example.com",
        "openai_api_key": "test-api-key",
        "pghost": "localhost",
        "pgport": 5432,
        "pgdatabase": "test_db",
        "pguser": "test_user",
        "pgpassword": "test-password",
    }


class TestAppSettings:
    """Tests for AppSettings defaults, validation, and derived values."""

    def test_settings_parse_secret_fields_and_default_algorithm(
        self,
        valid_settings_data: dict[str, str | int],
    ) -> None:
        """
        GIVEN: Valid settings values with secrets provided as strings.
        WHEN: AppSettings is instantiated.
        THEN: Secrets are protected and the default algorithm is applied.
        """
        settings = AppSettings(**valid_settings_data)

        assert settings.secret_key == SecretStr("test-secret")
        assert settings.openai_api_key == SecretStr("test-api-key")
        assert settings.algorithm == "HS256"
        assert settings.database_url == ("postgresql+asyncpg://test_user:test-password@localhost:5432/test_db")

    @pytest.mark.parametrize(
        ("origins", "expected_origins"),
        [
            ("https://example.com", ["https://example.com"]),
            (
                " http://localhost:5173/ , https://app.example.com ",
                ["http://localhost:5173", "https://app.example.com"],
            ),
            (
                "http://localhost:5173/,https://app.example.com",
                ["http://localhost:5173", "https://app.example.com"],
            ),
        ],
    )
    def test_frontend_origins_accept_explicit_http_origins(
        self,
        valid_settings_data: dict[str, str | int],
        origins: str,
        expected_origins: list[str],
    ) -> None:
        """
        GIVEN: One or more explicit HTTP(S) frontend origins.
        WHEN: AppSettings is instantiated with those origins.
        THEN: The input is accepted and trusted origins are normalized.
        """
        valid_settings_data["frontend_origins"] = origins

        settings = AppSettings(**valid_settings_data)

        assert settings.frontend_origins == origins
        assert settings.trusted_frontend_origins == expected_origins

    @pytest.mark.parametrize(
        "origins",
        [
            pytest.param("*", id="wildcard"),
            pytest.param("ftp://example.com", id="unsupported-scheme"),
            pytest.param("//example.com", id="missing-scheme"),
            pytest.param("https:///missing-host", id="missing-host"),
            pytest.param("https://example.com/app", id="path"),
            pytest.param("https://example.com?query=1", id="query"),
            pytest.param("https://example.com#fragment", id="fragment"),
            pytest.param("https://user:password@example.com", id="credentials"),
            pytest.param("https://example.com:invalid", id="invalid-port"),
            pytest.param("", id="empty-value"),
            pytest.param("https://example.com,", id="trailing-empty-origin"),
            pytest.param("https://example.com,,https://app.example.com", id="empty-origin"),
        ],
    )
    def test_frontend_origins_reject_invalid_values(
        self,
        valid_settings_data: dict[str, str | int],
        origins: str,
    ) -> None:
        """
        GIVEN: A wildcard, malformed, or non-origin frontend value.
        WHEN: AppSettings is instantiated with that value.
        THEN: Pydantic raises a validation error.
        """
        valid_settings_data["frontend_origins"] = origins

        with pytest.raises(ValidationError):
            AppSettings(**valid_settings_data)
