import os

from dotenv import load_dotenv


# ============================================================
# PATHS
# ============================================================

SRC_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PROJECT_ROOT = os.path.dirname(
    SRC_DIR
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    os.path.join(
        PROJECT_ROOT,
        ".env",
    )
)


# ============================================================
# CONFIGURATION
# ============================================================

EDGE_DRIVER_PATH = os.getenv(
    "EDGE_DRIVER_PATH"
)

SEARCH_URL = os.getenv(
    "SEARCH_URL",
    "https://www.bing.com",
)

ORIGINAL_USER_DATA_DIR = os.getenv(
    "ORIGINAL_USER_DATA_DIR"
)

SELENIUM_USER_DATA_DIR = os.getenv(
    "SELENIUM_USER_DATA_DIR"
)

PROFILES = [
    profile.strip()
    for profile in os.getenv(
        "PROFILES",
        "",
    ).split(",")
    if profile.strip()
]

SEARCHES_PER_PROFILE = int(
    os.getenv(
        "SEARCHES_PER_PROFILE",
        "30",
    )
)


# ============================================================
# RESOLVE DRIVER PATH
# ============================================================

if EDGE_DRIVER_PATH:
    if not os.path.isabs(EDGE_DRIVER_PATH):
        EDGE_DRIVER_PATH = os.path.abspath(
            os.path.join(
                PROJECT_ROOT,
                EDGE_DRIVER_PATH,
            )
        )


# ============================================================
# KEYWORDS
# ============================================================

KEYWORDS_FILE = os.path.join(
    SRC_DIR,
    "data",
    "keywords.txt",
)


# ============================================================
# VALIDATION
# ============================================================

REQUIRED_CONFIG = {
    "EDGE_DRIVER_PATH": EDGE_DRIVER_PATH,
    "ORIGINAL_USER_DATA_DIR": ORIGINAL_USER_DATA_DIR,
    "SELENIUM_USER_DATA_DIR": SELENIUM_USER_DATA_DIR,
}


missing_config = [
    key
    for key, value in REQUIRED_CONFIG.items()
    if not value
]


if missing_config:
    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(missing_config)
    )


if not PROFILES:
    raise RuntimeError(
        "PROFILES is empty in .env"
    )


if not os.path.isfile(EDGE_DRIVER_PATH):
    raise FileNotFoundError(
        "EdgeDriver not found:\n"
        f"{EDGE_DRIVER_PATH}"
    )