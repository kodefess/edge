from selenium import webdriver

from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from config.settings import (
    EDGE_DRIVER_PATH,
    SELENIUM_USER_DATA_DIR,
)

from driver.profile import ensure_profile_copied


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