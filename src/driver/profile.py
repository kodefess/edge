import os
import shutil

from config.settings import (
    ORIGINAL_USER_DATA_DIR,
    SELENIUM_USER_DATA_DIR,
)

from utils.console import console


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

    if (
        not os.path.exists(dst_local_state)
        and os.path.exists(src_local_state)
    ):
        console.print(
            "[dim]  · copying Edge local state...[/dim]"
        )

        shutil.copy2(
            src_local_state,
            dst_local_state,
        )

        console.print(
            "[green]  ✓[/green] "
            "[dim]local state copied[/dim]"
        )

    if not os.path.exists(dst_profile_path):

        if not os.path.exists(src_profile_path):
            raise FileNotFoundError(
                f"Profile not found: {src_profile_path}"
            )

        console.print(
            f"[dim]  · copying profile {profile_name}...[/dim]"
        )

        shutil.copytree(
            src_profile_path,
            dst_profile_path,
        )

        console.print(
            "[green]  ✓[/green] "
            "[dim]profile copied[/dim]"
        )

    return dst_profile_path