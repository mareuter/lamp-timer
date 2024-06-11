# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

from datetime import datetime, time, timedelta
import json
import os
import pathlib
import random
import tomllib
from zoneinfo import ZoneInfo

import requests


settings_file = pathlib.Path("~/.settings.toml").expanduser()
with settings_file.open("rb") as mfile:
    settings = tomllib.load(mfile)

TIME_ZONE = ZoneInfo(settings["LOCATION_TIMEZONE"])
LAMP_OFF_TIME = time.fromisoformat(settings["LAMP_OFF_TIME"])
LOCATION_LONGITUDE = settings["LOCATION_LONGITUDE"]
LOCATION_LATITUDE = settings["LOCATION_LATITUDE"]
LOCATION_HEIGHT = settings["LOCATION_HEIGHT"]
HELIOS_WEBSERVICE = settings["HELIOS_WEBSERVICE"]

CHECK_TIME = time(0, 10, 0, tzinfo=TIME_ZONE)
ONE_DAY = timedelta(days=1)
FIVE_MINUTES = timedelta(seconds=300)
TEN_MINUTES = timedelta(seconds=600)
CRONTAB_FORMAT = "%M %H %d %m"


def get_current_time() -> datetime:
    return datetime.now(tz=TIME_ZONE)


def get_seconds_from_now(dt: datetime) -> int:
    return (dt - get_current_time()).total_seconds()


def get_on_variation_from_range() -> timedelta:
    value = random.randrange(-FIVE_MINUTES.seconds, FIVE_MINUTES.seconds)
    return timedelta(seconds=value)


def get_off_variation_from_range() -> timedelta:
    value = random.randrange(-TEN_MINUTES.seconds, TEN_MINUTES.seconds)
    return timedelta(seconds=value)


def main():
    current_time = get_current_time()
    current_date = current_time.date()
    print(current_time)
    print("Setting up conditions")

    payload = {
        "cdatetime": current_time.timestamp(),
        "tz": TIME_ZONE.key,
        "lat": LOCATION_LATITUDE,
        "lon": LOCATION_LONGITUDE,
    }

    response = requests.get(HELIOS_WEBSERVICE, params=payload)

    sunrise = datetime.fromtimestamp(float(response.json()["sunrise"]), TIME_ZONE)
    sunset = datetime.fromtimestamp(float(response.json()["sunset"]), TIME_ZONE)

    lamp_on_time = sunset + get_on_variation_from_range()
    lamp_off_time = (
        datetime.combine(current_date, LAMP_OFF_TIME, tzinfo=TIME_ZONE)
        + get_off_variation_from_range()
    )

    output = {
        "date": current_date.timetuple(),
        "sunrise": sunrise.timestamp(),
        "sunset": sunset.timestamp(),
        "lamp_on": lamp_on_time.timestamp(),
        "lamp_off": lamp_off_time.timestamp(),
    }

    conditions_file = pathlib.Path("conditions.json")
    with conditions_file.open("w+") as ofile:
        json.dump(output, ofile, indent=2)

    next_check_time = datetime.combine(current_date, CHECK_TIME) + ONE_DAY
    current_delta = get_seconds_from_now(next_check_time)
    print(f"Next check time in {current_delta} seconds")

    check_time_script = "/home/lamptimer/setup_conditions.sh"
    cron_output = [
        f"{next_check_time.strftime(CRONTAB_FORMAT)} * {check_time_script}",
        f"{lamp_on_time.strftime(CRONTAB_FORMAT)} * /home/lamptimer/lamp_on.sh",
        f"{lamp_off_time.strftime(CRONTAB_FORMAT)} * /home/lamptimer/lamp_off.sh",
        "",
    ]
    crontab_file = pathlib.Path("crontab.in")
    crontab_file.write_text(os.linesep.join(cron_output))

    if get_current_time() > lamp_on_time:
        lamp_on_file = pathlib.Path("lamp_on")
        lamp_on_file.touch()


if __name__ == "__main__":
    main()
