# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime
import json
import pathlib
import time
import tomllib
import signal
import sys
from zoneinfo import ZoneInfo

import board
import displayio

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

from timer_display import TimerDisplay


settings_file = pathlib.Path("~/.settings.toml").expanduser()
with settings_file.open("rb") as mfile:
    settings = tomllib.load(mfile)

TIME_ZONE = ZoneInfo(settings["LOCATION_TIMEZONE"])
DEBOUNCE_TIME_MS = 200
DISPLAY_BUTTON = 23
DISPLAY_ON = True

# Setup display
displayio.release_displays()
spi = board.SPI()
display_bus = FourWire(
    spi, command=board.D25, chip_select=board.CE0, reset=None, baudrate=64000000
)
display = TimerDisplay(display_bus)


def read_and_display() -> None:
    conditions_file = pathlib.Path("conditions.json")
    if not conditions_file.exists():
        time.sleep(0.1)
    with conditions_file.open() as ifile:
        conditions = json.load(ifile)

    current_date = datetime(*(conditions["date"][:7]), tzinfo=TIME_ZONE)
    sunrise = datetime.fromtimestamp(conditions["sunrise"], tz=TIME_ZONE)
    sunset = datetime.fromtimestamp(conditions["sunset"], tz=TIME_ZONE)
    lamp_on_time = datetime.fromtimestamp(conditions["lamp_on"], tz=TIME_ZONE)
    lamp_off_time = datetime.fromtimestamp(conditions["lamp_off"], tz=TIME_ZONE)

    display.set_date_banner(current_date)
    display.set_sunrise_sunset(sunrise, sunset)
    display.set_lamp_on_off(lamp_on_time, lamp_off_time)


def signal_handler(sig, frame) -> None:
    print("Shutting down")
    display.unmount()
    display.off()
    sys.exit(0)


def main(opts: argparse.Namespace) -> None:
    read_and_display()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    main(args)
