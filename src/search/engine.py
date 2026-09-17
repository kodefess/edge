import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import SEARCH_URL
from utils.console import console
from utils.delay import (
    human_typing,
    random_delay,
)
from utils.keywords import load_keywords


KEYWORDS = load_keywords()


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

    console.print()
    console.print(
        f"[bold white]{profile_name}[/bold white] "
        f"[dim]· target {max_searches} searches[/dim]"
    )
    console.print()

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
                # Search output
                # --------------------------------------------

                console.print(
                    f"  [green]✓[/green] "
                    f"[dim]{search_count:02d}/{max_searches}[/dim]  "
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

                console.print(
                    f"  [red]✗[/red] "
                    f"[dim]{search_count + 1:02d}/{max_searches}[/dim]  "
                    f"search failed [dim]({type(e).__name__})[/dim]"
                )

                driver.get(
                    SEARCH_URL
                )

                time.sleep(3)

                continue

        # ----------------------------------------------------
        # Profile completed
        # ----------------------------------------------------

        console.print()
        console.print(
            f"[green]✓[/green] Completed "
            f"[dim]{search_count}/{max_searches} searches[/dim]"
        )

        return search_count

    except KeyboardInterrupt:

        console.print()
        console.print(
            f"[yellow]‼[/yellow] Stopped manually "
            f"[dim]{search_count}/{max_searches} searches[/dim]"
        )

        return search_count

    except Exception as e:

        console.print()
        console.print(
            f"[red]✗[/red] {type(e).__name__}"
        )
        console.print(
            f"[dim]  {e}[/dim]"
        )

        return search_count