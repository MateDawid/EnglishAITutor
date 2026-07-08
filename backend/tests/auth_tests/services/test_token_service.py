from datetime import UTC, datetime

import jwt

from auth.services.token_service import (
    create_access_token,
    hash_password,
    verify_access_token,
    verify_password,
)
from config import settings


class TestHashPasswordFunction:
    """
    Tests for hash_password function.
    """

    def test_hash_password_returns_hashed_value(self):
        """
        GIVEN: A plain password.
        WHEN: The password is hashed.
        THEN: A hashed string is returned that differs from the original password.
        """
        password = "my-secure-password"

        hashed_password = hash_password(password)

        assert isinstance(hashed_password, str)
        assert hashed_password != password

    def test_hash_password_generates_different_hashes_for_same_password(self):
        """
        GIVEN: The same password.
        WHEN: It is hashed multiple times.
        THEN: Different hashes are generated due to salting.
        """
        password = "my-secure-password"

        hash_1 = hash_password(password)
        hash_2 = hash_password(password)

        assert hash_1 != hash_2


class TestVerifyPasswordFunction:
    """
    Tests for verify_password function.
    """

    def test_verify_password_returns_true_for_matching_password(
        self,
    ):
        """
        GIVEN: A password and its hash.
        WHEN: Password verification is performed.
        THEN: True is returned.
        """
        password = "my-secure-password"
        hashed_password = hash_password(password)

        result = verify_password(
            password,
            hashed_password,
        )

        assert result is True

    def test_verify_password_returns_false_for_wrong_password(
        self,
    ):
        """
        GIVEN: A password hash and an incorrect password.
        WHEN: Password verification is performed.
        THEN: False is returned.
        """
        hashed_password = hash_password("correct-password")

        result = verify_password(
            "wrong-password",
            hashed_password,
        )

        assert result is False


class TestCreateAccessTokenFunction:
    """
    Tests for create_access_token function.
    """

    def test_create_access_token_returns_string(self):
        """
        GIVEN: Valid token payload.
        WHEN: Access token is created.
        THEN: A JWT string is returned.
        """
        token = create_access_token(
            data={"sub": "123"},
        )

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_contains_subject_claim(
        self,
    ):
        """
        GIVEN: A subject in the payload.
        WHEN: Access token is created.
        THEN: The encoded token contains the same subject.
        """
        subject = "user-id-123"

        token = create_access_token(
            data={"sub": subject},
        )

        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )

        assert payload["sub"] == subject

    def test_create_access_token_contains_expiration_claim(
        self,
    ):
        """
        GIVEN: Token payload.
        WHEN: Access token is created.
        THEN: The token contains an expiration claim in the future.
        """
        token = create_access_token(
            data={"sub": "123"},
        )

        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )

        assert "exp" in payload

        expiration = datetime.fromtimestamp(
            payload["exp"],
            tz=UTC,
        )

        assert expiration > datetime.now(UTC)


class TestVerifyAccessTokenFunction:
    """
    Tests for verify_access_token function.
    """

    def test_verify_access_token_returns_subject_for_valid_token(
        self,
    ):
        """
        GIVEN: A valid access token.
        WHEN: The token is verified.
        THEN: The subject is returned.
        """
        subject = "user-id-123"

        token = create_access_token(
            data={"sub": subject},
        )

        result = verify_access_token(token)

        assert result == subject

    def test_verify_access_token_returns_none_for_invalid_token(
        self,
    ):
        """
        GIVEN: An invalid token.
        WHEN: The token is verified.
        THEN: None is returned.
        """
        result = verify_access_token("invalid-token")

        assert result is None

    def test_verify_access_token_returns_none_for_tampered_token(
        self,
    ):
        """
        GIVEN: A valid token that has been modified.
        WHEN: The token is verified.
        THEN: None is returned.
        """
        token = create_access_token(
            data={"sub": "123"},
        )

        tampered_token = f"{token}tampered"

        result = verify_access_token(
            tampered_token,
        )

        assert result is None

    def test_verify_access_token_returns_none_when_sub_claim_missing(
        self,
    ):
        """
        GIVEN: A token without a subject claim.
        WHEN: The token is verified.
        THEN: None is returned because the token is invalid.
        """
        token = jwt.encode(
            {
                "exp": datetime.now(UTC).timestamp() + 3600,
            },
            settings.secret_key.get_secret_value(),
            algorithm=settings.algorithm,
        )

        result = verify_access_token(token)

        assert result is None

    def test_verify_access_token_returns_none_when_exp_claim_missing(
        self,
    ):
        """
        GIVEN: A token without an expiration claim.
        WHEN: The token is verified.
        THEN: None is returned because the token is invalid.
        """
        token = jwt.encode(
            {
                "sub": "123",
            },
            settings.secret_key.get_secret_value(),
            algorithm=settings.algorithm,
        )

        result = verify_access_token(token)

        assert result is None

    def test_verify_access_token_returns_none_for_expired_token(
        self,
    ):
        """
        GIVEN: An expired token.
        WHEN: The token is verified.
        THEN: None is returned.
        """
        token = jwt.encode(
            {
                "sub": "123",
                "exp": datetime.now(UTC).timestamp() - 3600,
            },
            settings.secret_key.get_secret_value(),
            algorithm=settings.algorithm,
        )

        result = verify_access_token(token)

        assert result is None