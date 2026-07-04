import factory
from typing import Type
from auth.models.db_user import DbUser

from backend.src.auth.services.token_service import hash_password

TEST_PASSWORD = "P@sSw0rD"


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DbUser  # SQLAlchemy model
        sqlalchemy_session_persistence = "commit"  # Commit the session after creating the user instance.

    email = factory.Faker("email")
    password_hash = factory.LazyFunction(
        lambda: hash_password(TEST_PASSWORD)
    )

    @classmethod
    def _create(cls, model_class: Type[DbUser], *args, **kwargs) -> DbUser:
        """
        Override to handle the password argument before creating the user

        Args:
            model_class (Type[DbUser]): Database model class for the user
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            DbUser: Created user instance

        """
        if "password" in kwargs:
            kwargs["password_hash"] = hash_password(kwargs.pop("password"))
        if "email" in kwargs:
            kwargs["email"] = kwargs["email"].lower()
        return super()._create(model_class, *args, **kwargs)
