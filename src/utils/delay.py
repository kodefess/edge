import random
import time


def random_delay(min_sec=5, max_sec=15):
    """Generate a random delay."""

    return random.uniform(
        min_sec,
        max_sec,
    )


def human_typing(element, text):
    """Type text with a random delay between characters."""

    for char in text:
        element.send_keys(char)

        time.sleep(
            random.uniform(
                0.05,
                0.2,
            )
        )