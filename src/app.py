import random
import time

from config.settings import (
    PROFILES,
    SEARCHES_PER_PROFILE,
)

from driver.edge import create_driver

from search.engine import (
    run_searches_for_profile,
    KEYWORDS,
)

from utils.console import console
from utils.process import close_running_edge


def main():

    total_profiles = len(
        PROFILES
    )

    total_searches = 0

    # --------------------------------------------------------
    # Application Header
    # --------------------------------------------------------

    console.print()
    console.print(
        "[bold white]Automated Search[/bold white] "
        "[dim]· Selenium / Edge[/dim]"
    )
    console.print()

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    console.print(
        f"[dim]profiles[/dim]  {total_profiles}"
    )

    console.print(
        f"[dim]target[/dim]    "
        f"{SEARCHES_PER_PROFILE} searches/profile"
    )

    console.print(
        f"[dim]keywords[/dim]  {len(KEYWORDS)}"
    )

    console.print()

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

        console.print(
            f"[dim]profile {index}/{total_profiles}[/dim]"
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

            console.print()
            console.print(
                f"[red]✗[/red] Error "
                f"[dim]· {profile}[/dim]"
            )

            console.print(
                f"[dim]  {type(e).__name__}: {e}[/dim]"
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
    # Final Summary
    # --------------------------------------------------------

    console.print()
    console.print(
        "[bold white]Session Summary[/bold white]"
    )

    console.print(
        f"[dim]  profiles processed[/dim]  "
        f"{total_profiles}"
    )

    console.print(
        f"[dim]  searches completed[/dim]  "
        f"{total_searches}"
    )

    console.print(
        f"[dim]  average / profile[/dim]   "
        f"{total_searches / total_profiles:.1f}"
    )

    console.print()

    console.print(
        "[green]✓[/green] Session completed successfully."
    )

    console.print()


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        console.print()
        console.print(
            "[yellow]‼[/yellow] Script stopped."
        )

    except Exception as e:

        console.print()
        console.print(
            f"[red]✗[/red] Fatal error "
            f"[dim]· {type(e).__name__}[/dim]"
        )

        console.print(
            f"[dim]  {e}[/dim]"
        )