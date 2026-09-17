import subprocess
import time


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