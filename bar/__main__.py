"""
Joseph's lemonbar
"""

import subprocess
import time
import threading
import os

from .elements import get_battery, get_ws, get_date, get_volume, now_playing
from .constants import (
    BG_COL, FG_COL, HL_COL,
    GENERAL_PLACEHOLDER, TEXT_FONT, ICON_FONT
)


def restart():
    print("Restarting...")

    os.execvp("python3.7", ["python3.7", "-m", "bar"])

    # the execvpe(2) syscall replaces the current process
    # we will replace the current process with a new instance to
    # restart the bar


def feed_lemonbar(lemonbar: subprocess.Popen):
    while True:
        ws = get_ws()
        battery = get_battery()
        date = get_date()
        volume = get_volume()
        np = now_playing()

        bar_string = (
            f"%{{O10000}}"
            f"%{{U{HL_COL}+u}}"
            f"%{{l}}{battery}"
            f"{GENERAL_PLACEHOLDER}"
            f"{ws}"
            f"{GENERAL_PLACEHOLDER}"
            f"%{{A:restart:}}\uf0e2%{{A}}"
            f"%{{c}}{date}"
            f"%{{r}}"
            f"{GENERAL_PLACEHOLDER}"
            f"{np}"
            f"{volume}\n"
        )

        lemonbar.stdin.write(bar_string.encode())
        lemonbar.stdin.flush()

        time.sleep(0.25)


def consume_lemonbar(lemonbar: subprocess.Popen):
    while True:
        data = lemonbar.stdout.readline().decode().strip()
        if data.strip() == "restart":
            restart()


if __name__ == "__main__":
    lemonbar = subprocess.Popen(f"lemonbar "
                                f"-F \\{FG_COL} "
                                f"-B \\{BG_COL} "
                                f"-f {TEXT_FONT} "
                                f"-f {ICON_FONT} "
                                f"-u 0 -o 0 -g 1366x25+0+0",
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    feeder = threading.Thread(target=feed_lemonbar, args=(lemonbar,))
    feeder.start()

    consumer = threading.Thread(target=consume_lemonbar, args=(lemonbar,))
    consumer.start()
