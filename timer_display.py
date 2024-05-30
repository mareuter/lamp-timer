# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

from datetime import datetime, timedelta
import time

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
from adafruit_st7789 import ST7789
import board
import displayio

__all__ = ["TimerDisplay"]


DISPLAY_FONT = bitmap_font.load_font("fonts/SpartanMB-Regular-12.bdf")
TEXT_COLOR = 0xFFFFFF
LIGHT_COLOR = 0xF0E442
DARK_COLOR = 0x0072B2
OFF_CIRCLE_BMP = displayio.OnDiskBitmap("images/Off_Circle.bmp")
ON_CIRCLE_BMP = displayio.OnDiskBitmap("images/On_Circle.bmp")
SUNRISE_BMP = displayio.OnDiskBitmap("images/Sunrise.bmp")
SUNSET_BMP = displayio.OnDiskBitmap("images/Sunset.bmp")
DATE_BANNER_FORMAT = "%B %-d, %Y"
USNO_TIME_FORMAT = "%H:%M"
TIME_FORMAT = "%H:%M:%S"
DISPLAY_DELAY = 0.05


class TimerDisplay:
    def __init__(self, display_bus):
        self.display = ST7789(
            display_bus,
            width=240,
            height=135,
            rotation=270,
            rowstart=40,
            colstart=53,
            backlight_pin=board.D22,
        )
        self.display.root_group = None
        self.main_group = displayio.Group()

        # self._background()
        self._date_banner()
        self._sunrise_sunset()
        self._lamp_on_off()

        self.display.root_group = self.main_group

    @property
    def brightness(self) -> float:
        return self.display.brightness

    def _background(self) -> None:
        bg = displayio.Bitmap(
            width=self.display.width, height=self.display.height, value_count=1
        )
        bg.fill(0)
        c = displayio.Palette(1)
        c[0] = 0x000000
        img = displayio.TileGrid(bg, pixel_shader=c, x=0, y=0)
        self.main_group.append(img)

    def _date_banner(self) -> None:
        date_label = bitmap_label.Label(DISPLAY_FONT, color=TEXT_COLOR)
        date_label.anchor_point = (0, 0.5)
        date_label.anchored_position = (44, 14)
        self.main_group.append(date_label)

    def _sunrise_sunset(self) -> None:
        sunrise_img = displayio.TileGrid(
            SUNRISE_BMP, pixel_shader=SUNRISE_BMP.pixel_shader, x=2, y=47
        )
        self.main_group.append(sunrise_img)

        sunrise_time_label = bitmap_label.Label(DISPLAY_FONT, color=LIGHT_COLOR)
        sunrise_time_label.anchor_point = (0, 0.5)
        sunrise_time_label.anchored_position = (46, 67)
        self.main_group.append(sunrise_time_label)

        sunset_img = displayio.TileGrid(
            SUNSET_BMP, pixel_shader=SUNSET_BMP.pixel_shader, x=122, y=47
        )
        self.main_group.append(sunset_img)

        sunset_time_label = bitmap_label.Label(DISPLAY_FONT, color=DARK_COLOR)
        sunset_time_label.anchor_point = (0, 0.5)
        sunset_time_label.anchored_position = (165, 67)
        self.main_group.append(sunset_time_label)

    def _lamp_on_off(self) -> None:
        on_circle_img = displayio.TileGrid(
            ON_CIRCLE_BMP, pixel_shader=ON_CIRCLE_BMP.pixel_shader, x=2, y=92
        )
        self.main_group.append(on_circle_img)

        on_time_label = bitmap_label.Label(DISPLAY_FONT, color=LIGHT_COLOR)
        on_time_label.anchor_point = (0, 0.5)
        on_time_label.anchored_position = (46, 112)
        self.main_group.append(on_time_label)

        off_circle_img = displayio.TileGrid(
            OFF_CIRCLE_BMP, pixel_shader=OFF_CIRCLE_BMP.pixel_shader, x=122, y=92
        )
        self.main_group.append(off_circle_img)

        off_time_label = bitmap_label.Label(DISPLAY_FONT, color=DARK_COLOR)
        off_time_label.anchor_point = (0, 0.5)
        off_time_label.anchored_position = (165, 112)
        self.main_group.append(off_time_label)

    def _usno_format(self, time: datetime) -> str:
        time += timedelta(seconds=30)
        return time.strftime(USNO_TIME_FORMAT)

    def set_date_banner(self, datestamp: datetime) -> None:
        self.main_group[0].text = datestamp.strftime(DATE_BANNER_FORMAT)
        time.sleep(DISPLAY_DELAY)

    def set_sunrise_sunset(self, sunrise: datetime, sunset: datetime) -> None:
        self.main_group[2].text = self._usno_format(sunrise)
        time.sleep(DISPLAY_DELAY)
        self.main_group[4].text = self._usno_format(sunset)
        time.sleep(DISPLAY_DELAY)

    def set_lamp_on_off(self, lamp_on: datetime, lamp_off: datetime) -> None:
        self.main_group[6].text = lamp_on.strftime(TIME_FORMAT)
        time.sleep(DISPLAY_DELAY)
        self.main_group[8].text = lamp_off.strftime(TIME_FORMAT)

    def off(self) -> None:
        self.display.brightness = 0.0

    def on(self, brightness: float = 1.0) -> None:
        self.display.brightness = brightness

    def mount(self) -> None:
        self.display.root_group = self.main_group

    def unmount(self) -> None:
        self.display.root_group = None
