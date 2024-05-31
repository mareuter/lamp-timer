# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import asyncio
from datetime import datetime, time, timedelta
import pathlib
import random
import tomllib
from zoneinfo import ZoneInfo

import board
import digitalio
import displayio

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
import requests

from timer_display import TimerDisplay

# Setup display
displayio.release_displays()
spi = board.SPI()
display_bus = FourWire(
    spi, command=board.D25, chip_select=board.CE0, reset=None, baudrate=64000000
)
display = TimerDisplay(display_bus)

# Setup display buttons
display_on_off_btn = digitalio.DigitalInOut(board.D23)
display_on_off_btn.switch_to_input()

# Setup power relay pin
power_relay_pin = digitalio.DigitalInOut(board.D5)
power_relay_pin.switch_to_output()

settings_file = pathlib.Path("~/.settings.toml").expanduser()
with settings_file.open("rb") as mfile:
    settings = tomllib.load(mfile)

TIME_ZONE = ZoneInfo(settings["LOCATION_TIMEZONE"])
CHECK_TIME = time(0, 10, 0, tzinfo=TIME_ZONE)
ONE_DAY = timedelta(days=1)
FIVE_MINUTES = timedelta(seconds=300)
TEN_MINUTES = timedelta(seconds=600)
LAMP_OFF_TIME = time.fromisoformat(settings["LAMP_OFF_TIME"])
LOCATION_LONGITUDE = settings["LOCATION_LONGITUDE"]
LOCATION_LATITUDE = settings["LOCATION_LATITUDE"]
LOCATION_HEIGHT = settings["LOCATION_HEIGHT"]
HELIOS_WEBSERVICE = settings["HELIOS_WEBSERVICE"]
DISPLAY_TIMEOUT = 5 * 60


class TimerCondition:
    def __init__(self):
        self.initialized = False
        self.next_check_time = None
        self.lamp_on_time = None
        self.lamp_off_time = None


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


async def dim_screen(evt: asyncio.Event) -> None:
    while True:
        interrupted = False
        await evt.wait()
        print("Starting display timeout")
        timeout = DISPLAY_TIMEOUT
        while timeout > 0:
            if not evt.is_set():
                interrupted = True
                print("Interrupt display timeout")
                break
            await asyncio.sleep(1)
            timeout -= 1
        if not interrupted:
            print("Turning off display")
            display.off()
            evt.clear()


async def time_setter(tc):
    while True:
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

        tc.lamp_on_time = sunset + get_on_variation_from_range()
        tc.lamp_off_time = (
            datetime.combine(current_date, LAMP_OFF_TIME, tzinfo=TIME_ZONE)
            + get_off_variation_from_range()
        )
        tc.initialized = True

        display.set_date_banner(current_date)
        display.set_sunrise_sunset(sunrise, sunset)
        display.set_lamp_on_off(tc.lamp_on_time, tc.lamp_off_time)

        tc.next_check_time = datetime.combine(current_date, CHECK_TIME) + ONE_DAY
        current_delta = get_seconds_from_now(tc.next_check_time)
        print(f"Next check time in {current_delta} seconds")
        await asyncio.sleep(current_delta)
        tc.initialized = False


async def lamp_control(tc):
    while True:
        while not tc.initialized:
            print("Waiting for conditions")
            await asyncio.sleep(1)
        current_delta = get_seconds_from_now(tc.lamp_on_time)
        print(f"Lamp on time in {current_delta} seconds")
        await asyncio.sleep(current_delta)
        print(f"Turning on lamp at {get_current_time()}")
        current_delta = get_seconds_from_now(tc.lamp_off_time)
        # GPIO on
        power_relay_pin.value = True
        print(f"Lamp off time in {current_delta} seconds")
        await asyncio.sleep(current_delta)
        print(f"Turning off lamp at {get_current_time()}")
        # GPIO off
        power_relay_pin.value = False
        current_delta = get_seconds_from_now(tc.next_check_time) + 10
        print(f"Next lamp control check in {current_delta} seconds")
        await asyncio.sleep(current_delta)


async def monitor_buttons(evt: asyncio.Event) -> None:
    evt.set()
    monitor_on = True
    while True:
        if not display_on_off_btn.value:
            if monitor_on:
                print("Turn off display")
                display.unmount()
                display.off()
                evt.clear()
                monitor_on = False
            else:
                print("Turn on display")
                if display.brightness != 1.0:
                    display.on()
                display.mount()
                evt.set()
                monitor_on = True
        await asyncio.sleep(1.0)
        if not evt.is_set():
            monitor_on = False


async def main():
    tc = TimerCondition()
    display_event = asyncio.Event()
    await asyncio.gather(
        time_setter(tc),
        lamp_control(tc),
        monitor_buttons(display_event),
        dim_screen(display_event),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        display.off()
        display.unmount()
        power_relay_pin.value = False
