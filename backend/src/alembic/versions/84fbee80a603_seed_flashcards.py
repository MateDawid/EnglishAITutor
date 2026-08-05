"""seed_flashcards_from_json

Revision ID: 84fbee80a603
Revises: d8f2c3b1a5e9
Create Date: 2026-07-19 06:27:09.842328

"""

import logging
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import json
import uuid
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = "84fbee80a603"
down_revision: Union[str, Sequence[str], None] = "3ad30277dea3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

LOGGER = logging.getLogger(__name__)


def upgrade() -> None:
    """Seed flashcards from flashcards.json."""
    LOGGER.warning(f"🪲 DEBUG: {os.environ.get('SEED_FLASHCARDS')}")
    if not os.environ.get("SEED_FLASHCARDS", "").lower() == "true":
        LOGGER.warning("⚠️ Populating database Flashcards skipped.")
        return
    LOGGER.warning("ℹ️ Populating database Flashcards from flashcards.json.")
    json_path = Path(__file__).parent.parent / "flashcards.json"

    with open(json_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    conn = op.get_bind()

    for w in words:
        conn.execute(
            sa.text(
                "INSERT INTO flashcards (id, word, meaning, part_of_speech, example) "
                "VALUES (:id, :word, :meaning, CAST(:part_of_speech AS part_of_speech_enum), :example)"
            ),
            {
                "id": uuid.uuid4(),
                "word": w["word"],
                "meaning": w["meaning"],
                "part_of_speech": "_".join(w["part_of_speech"].split()).upper(),
                "example": w.get("example"),
            },
        )


def downgrade() -> None:
    """Remove seeded flashcards."""
    op.execute("TRUNCATE TABLE flashcards")
