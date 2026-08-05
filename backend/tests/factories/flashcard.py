import factory
from flashcards.models.db_flashcard import DbFlashcard, PartOfSpeech


class FlashcardFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DbFlashcard
        sqlalchemy_session_persistence = "commit"

    word = factory.Faker("word")
    meaning = factory.Faker("sentence", nb_words=6)
    part_of_speech = factory.Faker("random_element", elements=[part for part in PartOfSpeech])
    example = factory.Faker("sentence", nb_words=10)
