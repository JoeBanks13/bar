"""
Functions to get elements which make up the bar
"""

from .constants import (
    BG_COL, BG_SEC_COL, FG_COL, FG_SEC_COL,
    HL_COL, BATTERY_PLACEHOLDER, WORKSPACE_PLACEHOLDER,
    CLOCK_PLACEHOLDER, VOLUME_PLACEHOLDER, GENERAL_PLACEHOLDER
)

import subprocess
import datetime


def reset(value: str) -> str:
    return "{0}%{{B-}}%{{T-}}%{{F-}}".format(value)


def _run_command(command: str) -> str:
    command = subprocess.run(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    # No need to return stderr because I don't want
    # it in my bar, I'll see if something fails.
    return command.stdout.decode().rstrip("\n")


def get_battery() -> str:
    output = _run_command("acpi --battery | cut -d, -f2")

    return reset(f"%{{B{BG_COL}}}"
                 f"%{{F{FG_COL}}}"
                 f"{BATTERY_PLACEHOLDER}"
                 f"{output.lstrip()}"
                 f"{BATTERY_PLACEHOLDER}")


def get_ws() -> str:
    # bspwm here we go...
    output = _run_command("bspc wm -g")

    desktops = output.split(":")[1:7]

    ws_string = ""

    for desktop in desktops:
        # o - unoccupied focused desktop
        # O - occupied focused desktop
        # F - free focused desktop
        # f - free unfocused desktop
        # U - urgent focused desktop
        # u - urgent unfocused desktop

        if desktop[0] in ["o"]:
            color = (BG_COL, FG_SEC_COL)
        elif desktop[0] in ["U", "u"]:
            color = (BG_COL, HL_COL)
        elif desktop[0] in ["F", "O"]:
            color = (BG_SEC_COL, FG_COL)
        else:
            color = (BG_COL, BG_SEC_COL)

        ws_string += (
            f"%{{A:switch-{desktop[1:]}:}}"
            f"%{{B{color[0]}}}"
            f"%{{F{color[1]}}}"
            f"{WORKSPACE_PLACEHOLDER}"
            f"{desktop[1:]}"
            f"{WORKSPACE_PLACEHOLDER}"
            f"%{{A}}"
        )

    return reset(ws_string)


def get_date() -> str:
    time = datetime.datetime.now().strftime("%a %d %b / %H:%M:%S")

    return reset(f"%{{B{BG_SEC_COL}}}"
                 f"%{{F{FG_COL}}}"
                 f"{CLOCK_PLACEHOLDER}"
                 f"{time}"
                 f"{CLOCK_PLACEHOLDER}")


def get_volume() -> str:
    output = _run_command("pactl list sinks"
                          "| grep '^[[:space:]]Volume:'"
                          "| head -n 1")

    volume = output.split("/")[1].strip()

    return reset(f"%{{B{BG_SEC_COL}}}"
                 f"%{{F{FG_COL}}}"
                 f"{VOLUME_PLACEHOLDER}"
                 f"\uf028 {volume}"
                 f"{VOLUME_PLACEHOLDER}")


def now_playing() -> str:
    artist = _run_command("playerctl metadata xesam:artist")
    song = _run_command("playerctl metadata xesam:title")

    if song == "":
        return ""

    string = f"{song}"

    if artist != "":
        string += f" - {artist}"

    if len(string) > 40:
        string = string[0:37] + "..."

    string = "\uf001 " + string

    return reset(f"%{{B{BG_SEC_COL}}}"
                 f"%{{F{FG_COL}}}"
                 f"{GENERAL_PLACEHOLDER}"
                 f"{string}"
                 f"{GENERAL_PLACEHOLDER}")
