import os
import random
import shutil
import subprocess
import time

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from keywords import KEYWORDS


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

EDGE_DRIVER_PATH = os.getenv(
    "EDGE_DRIVER_PATH"
)

SEARCH_URL = os.getenv(
    "SEARCH_URL",
    "https://www.bing.com"
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
        ""
    ).split(",")
    if profile.strip()
]

SEARCHES_PER_PROFILE = int(
    os.getenv(
        "SEARCHES_PER_PROFILE",
        "30"
    )
)


# ============================================================
# VALIDATE CONFIGURATION
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


if not KEYWORDS:
    raise RuntimeError(
        "KEYWORDS is empty in keywords.py"
    )


# ============================================================
# HELPERS
# ============================================================

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


def close_running_edge():
    """
    Close existing Edge and EdgeDriver processes.

    Output is suppressed to keep the terminal clean.
    """

    subprocess.run(
        [
            "taskkill",
            "/F",
            "/IM",
            "msedge.exe",
            "/T",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        [
            "taskkill",
            "/F",
            "/IM",
            "msedgedriver.exe",
            "/T",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    time.sleep(2)


# ============================================================
# PROFILE MANAGEMENT
# ============================================================

def ensure_profile_copied(profile_name):
    """
    Copy the original Edge profile to the Selenium directory.

    The profile is only copied if it does not already exist.
    """

    src_profile_path = os.path.join(
        ORIGINAL_USER_DATA_DIR,
        profile_name,
    )

    dst_profile_path = os.path.join(
        SELENIUM_USER_DATA_DIR,
        profile_name,
    )

    src_local_state = os.path.join(
        ORIGINAL_USER_DATA_DIR,
        "Local State",
    )

    dst_local_state = os.path.join(
        SELENIUM_USER_DATA_DIR,
        "Local State",
    )

    os.makedirs(
        SELENIUM_USER_DATA_DIR,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Copy Local State
    # --------------------------------------------------------

    if (
        not os.path.exists(dst_local_state)
        and os.path.exists(src_local_state)
    ):
        print("  → Copying Edge Local State...")

        shutil.copy2(
            src_local_state,
            dst_local_state,
        )

        print("  ✓ Local State copied")

    # --------------------------------------------------------
    # Copy Profile
    # --------------------------------------------------------

    if not os.path.exists(dst_profile_path):

        if not os.path.exists(src_profile_path):
            raise FileNotFoundError(
                f"Profile not found: {src_profile_path}"
            )

        print(
            f"  → Copying profile: "
            f"{profile_name}"
        )

        shutil.copytree(
            src_profile_path,
            dst_profile_path,
        )

        print("  ✓ Profile copied")

    return dst_profile_path


# ============================================================
# SELENIUM DRIVER
# ============================================================

def create_driver(profile_name):
    """Create Edge WebDriver using the specified profile."""

    ensure_profile_copied(
        profile_name
    )

    options = Options()

    options.add_argument(
        f"user-data-dir={SELENIUM_USER_DATA_DIR}"
    )

    options.add_argument(
        f"profile-directory={profile_name}"
    )

    options.add_experimental_option(
        "excludeSwitches",
        [
            "enable-automation",
            "enable-logging",
        ],
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False,
    )

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_argument(
        "--start-maximized"
    )

    options.add_argument(
        "--disable-infobars"
    )

    options.add_argument(
        "--no-first-run"
    )

    options.add_argument(
        "--no-default-browser-check"
    )

    options.add_argument(
        "--remote-debugging-port=0"
    )

    service = Service(
        EDGE_DRIVER_PATH
    )

    driver = webdriver.Edge(
        service=service,
        options=options,
    )

    # Hide webdriver property
    driver.execute_script(
        """
        Object.defineProperty(
            navigator,
            'webdriver',
            {
                get: () => undefined
            }
        )
        """
    )

    return driver


# ============================================================
# SEARCH
# ============================================================

def run_searches_for_profile(
    driver,
    profile_name,
    max_searches=30,
):
    """
    Run searches for a single Edge profile.
    """

    wait = WebDriverWait(
        driver,
        10,
    )

    driver.get(
        SEARCH_URL
    )

    print()
    print(
        f"Profile : {profile_name}"
    )
    print(
        f"Target  : {max_searches} searches"
    )
    print("-" * 60)

    search_count = 0
    used_keywords = []

    try:

        while search_count < max_searches:

            # ------------------------------------------------
            # Get unused keywords
            # ------------------------------------------------

            available_keywords = [
                keyword
                for keyword in KEYWORDS
                if keyword not in used_keywords
            ]

            # Reset keyword pool
            if not available_keywords:

                used_keywords = []

                available_keywords = KEYWORDS

            keyword = random.choice(
                available_keywords
            )

            used_keywords.append(
                keyword
            )

            try:

                # --------------------------------------------
                # Random delay
                # --------------------------------------------

                time.sleep(
                    random_delay(
                        8,
                        20,
                    )
                )

                # --------------------------------------------
                # Find search box
                # --------------------------------------------

                search_box = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.NAME,
                            "q",
                        )
                    )
                )

                # --------------------------------------------
                # Clear search box
                # --------------------------------------------

                search_box.clear()

                time.sleep(
                    random.uniform(
                        0.5,
                        1.5,
                    )
                )

                # --------------------------------------------
                # Type keyword
                # --------------------------------------------

                human_typing(
                    search_box,
                    keyword,
                )

                time.sleep(
                    random.uniform(
                        0.5,
                        1.0,
                    )
                )

                # --------------------------------------------
                # Execute search
                # --------------------------------------------

                search_box.send_keys(
                    Keys.ENTER
                )

                search_count += 1

                # --------------------------------------------
                # Clean terminal output
                # --------------------------------------------

                print(
                    f"[{search_count:02d}/{max_searches}] "
                    f"{keyword}"
                )

                # --------------------------------------------
                # Simulate reading
                # --------------------------------------------

                time.sleep(
                    random.uniform(
                        2,
                        5,
                    )
                )

                # --------------------------------------------
                # Random scroll
                # --------------------------------------------

                scroll_amount = random.randint(
                    200,
                    800,
                )

                driver.execute_script(
                    f"window.scrollBy(0, {scroll_amount});"
                )

                time.sleep(
                    random.uniform(
                        1,
                        3,
                    )
                )

                # --------------------------------------------
                # Occasionally open search result
                # --------------------------------------------

                if random.random() < 0.3:

                    try:

                        results = driver.find_elements(
                            By.CSS_SELECTOR,
                            "h2 a",
                        )

                        if results:

                            result_to_click = random.choice(
                                results[:5]
                            )

                            result_to_click.click()

                            time.sleep(
                                random.uniform(
                                    5,
                                    10,
                                )
                            )

                            driver.back()

                            time.sleep(
                                random.uniform(
                                    2,
                                    4,
                                )
                            )

                    except Exception:
                        pass

                # --------------------------------------------
                # Return to search page
                # --------------------------------------------

                driver.get(
                    SEARCH_URL
                )

                time.sleep(
                    random.uniform(
                        2,
                        4,
                    )
                )

            except Exception as e:

                print(
                    f"[ERROR] Search "
                    f"#{search_count + 1}: "
                    f"{type(e).__name__}"
                )

                driver.get(
                    SEARCH_URL
                )

                time.sleep(3)

                continue

        # ----------------------------------------------------
        # Profile completed
        # ----------------------------------------------------

        print("-" * 60)

        print(
            f"✓ Completed: "
            f"{search_count}/{max_searches} searches"
        )

        return search_count

    except KeyboardInterrupt:

        print()
        print(
            "[STOPPED] Script stopped manually."
        )

        print(
            f"Progress: "
            f"{search_count}/{max_searches}"
        )

        return search_count

    except Exception as e:

        print(
            f"[ERROR] Unexpected error: "
            f"{type(e).__name__}: {e}"
        )

        return search_count


# ============================================================
# MAIN
# ============================================================

def main():

    total_profiles = len(
        PROFILES
    )

    total_searches = 0

    print()
    print("=" * 60)
    print("  AUTOMATED SEARCH")
    print("=" * 60)

    print(
        f"  Profiles : {total_profiles}"
    )

    print(
        f"  Target   : "
        f"{SEARCHES_PER_PROFILE} searches/profile"
    )

    print(
        f"  Keywords : {len(KEYWORDS)}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # Close existing Edge
    # --------------------------------------------------------

    close_running_edge()

    # --------------------------------------------------------
    # Process profiles
    # --------------------------------------------------------

    for index, profile in enumerate(
        PROFILES,
        start=1,
    ):

        print()

        print(
            f"[PROFILE {index}/{total_profiles}] "
            f"{profile}"
        )

        driver = None

        try:

            # Create browser
            driver = create_driver(
                profile
            )

            # Run searches
            searches_done = run_searches_for_profile(
                driver,
                profile,
                max_searches=SEARCHES_PER_PROFILE,
            )

            total_searches += searches_done

        except Exception as e:

            print(
                f"[ERROR] {profile}: "
                f"{type(e).__name__}: {e}"
            )

        finally:

            if driver:
                driver.quit()

        # ----------------------------------------------------
        # Delay between profiles
        # ----------------------------------------------------

        if index < total_profiles:

            time.sleep(
                random.uniform(
                    10,
                    20,
                )
            )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("  COMPLETED")
    print("=" * 60)

    print(
        f"  Profiles processed : "
        f"{total_profiles}"
    )

    print(
        f"  Searches completed : "
        f"{total_searches}"
    )

    print(
        f"  Average/profile    : "
        f"{total_searches / total_profiles:.1f}"
    )

    print("=" * 60)
    print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()