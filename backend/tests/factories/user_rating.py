import factory

from flashcards.enums import DatabaseRating
from flashcards.models import DbUserRating


class UserRatingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DbUserRating
        sqlalchemy_session_persistence = "commit"

    user_id = None
    flashcard_id = None
    rating = factory.Faker("random_element", elements=[rating for rating in DatabaseRating])

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        kwargs = super()._adjust_kwargs(**kwargs)
        if kwargs.get("user_id") is None:
            raise ValueError("UserRatingFactory requires 'user_id'.")
        if kwargs.get("flashcard_id") is None:
            raise ValueError("UserRatingFactory requires 'flashcard_id'.")
        return kwargs
