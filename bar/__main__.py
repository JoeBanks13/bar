"""
Joseph's lemonbar
"""

import subprocess
import time

from .elements import get_battery, get_ws, get_date, get_volume, now_playing
from .constants import (
    BG_COL, FG_COL, HL_COL,
    GENERAL_PLACEHOLDER, TEXT_FONT, ICON_FONT
)

if __name__ == "__main__":
    lemonbar = subprocess.Popen(f"lemonbar "
                                f"-F \\{FG_COL} "
                                f"-B \\{BG_COL} "
                                f"-f {TEXT_FONT} "
                                f"-f {ICON_FONT} "
                                f"-u 0 -o 0 -g 1366x25+0+0",
                                stdin=subprocess.PIPE, shell=True)

    while True:
        ws = get_ws()
        battery = get_battery()
        date = get_date()
        volume = get_volume()
        np = now_playing()

        bar_string = (
            f"%{{O10000}}"
            f"%{{U{HL_COL}+u}}"
            f"%{{l}}{battery}{GENERAL_PLACEHOLDER}{ws}"
            f"%{{c}}{date}"
            f"%{{r}}"
            f"{GENERAL_PLACEHOLDER}"
            f"{np}"
            f"{volume}\n"
        )

        lemonbar.stdin.write(bar_string.encode())
        lemonbar.stdin.flush()

        time.sleep(0.25)
