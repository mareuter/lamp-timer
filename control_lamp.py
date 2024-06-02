#!/bin/bash

# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
from datetime import datetime
import pathlib
import tomllib
from zoneinfo import ZoneInfo

import board
import digitalio


def main(opts: argparse.Namespace) -> None:
    settings_file = pathlib.Path("~/.settings.toml").expanduser()
    with settings_file.open("rb") as mfile:
        settings = tomllib.load(mfile)

    TIME_ZONE = ZoneInfo(settings["LOCATION_TIMEZONE"])

    # Setup power relay pin
    power_relay_pin = digitalio.DigitalInOut(board.D5)
    power_relay_pin.switch_to_output()

    state = bool(opts.lamp_state)
    switch = "on" if state else "off"

    print(f"Turning {switch} lamp at {datetime.now(tz=TIME_ZONE)}")

    power_relay_pin.value = state


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "lamp_state",
        type=int,
        choices=[0, 1],
        help="Control the power relay for the lamp.",
    )

    args = parser.parse_args()

    main(args)
