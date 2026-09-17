import os

from config.settings import KEYWORDS_FILE


def load_keywords():
    if not os.path.exists(KEYWORDS_FILE):
        raise FileNotFoundError(
            f"Keywords file not found: {KEYWORDS_FILE}"
        )

    with open(
        KEYWORDS_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        keywords = [
            line.strip()
            for line in file
            if line.strip()
        ]

    if not keywords:
        raise RuntimeError(
            "KEYWORDS is empty in keywords.txt"
        )

    return keywords