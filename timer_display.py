# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

from datetime import datetime, timedelta

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
from adafruit_st7735r import ST7735R
import displayio
from displayio import FourWire

__all__ = ["TimerDisplay"]


DISPLAY_FONT = bitmap_font.load_font("fonts/SpartanMB-Regular-12.bdf")
TEXT_COLOR = 0xFFFFFF
LIGHT_COLOR = 0xF0E442
DARK_COLOR = 0x0072B2
OFF_CIRCLE_BMP = displayio.OnDiskBitmap("images/Off_Circle.bmp")
ON_CIRCLE_BMP = displayio.OnDiskBitmap("images/On_Circle.bmp")
SUNRISE_BMP = displayio.OnDiskBitmap("images/Sunrise.bmp")
SUNSET_BMP = displayio.OnDiskBitmap("images/Sunset.bmp")
USNO_TIME_FORMAT = "%H:%M"
TIME_FORMAT = "%H:%M:%S"


class TimerDisplay:
    def __init__(self, display_bus: FourWire):
        self.display = ST7735R(display_bus)
        self.main_group = displayio.Group()

        self._sunrise_sunset()
        self._lamp_on_off()

        self.display.root_group = self.main_group

    def _sunrise_sunset(self) -> None:
        sunrise_img = displayio.TileGrid(
            SUNRISE_BMP, pixel_shader=SUNRISE_BMP.pixel_shader, x=0, y=68
        )
        self.main_group.append(sunrise_img)

        sunrise_time_label = bitmap_label.Label(DISPLAY_FONT, color=LIGHT_COLOR)
        sunrise_time_label.anchor_point = (0.5, 0.3175)
        sunrise_time_label.anchored_position = (76, 78)
        self.main_group.append(sunrise_time_label)

        sunset_img = displayio.TileGrid(
            SUNSET_BMP, pixel_shader=SUNSET_BMP.pixel_shader, x=120, y=68
        )
        self.main_group.append(sunset_img)

        sunset_time_label = bitmap_label.Label(DISPLAY_FONT, color=DARK_COLOR)
        sunset_time_label.anchor_point = (0.5, 0.3175)
        sunset_time_label.anchored_position = (196, 78)
        self.main_group.append(sunset_time_label)

    def _lamp_on_off(self) -> None:
        on_circle_img = displayio.TileGrid(
            ON_CIRCLE_BMP, pixel_shader=ON_CIRCLE_BMP.pixel_shader, x=0, y=101
        )
        self.main_group.append(on_circle_img)

        on_time_label = bitmap_label.Label(DISPLAY_FONT, color=LIGHT_COLOR)
        on_time_label.anchor_point = (0.5, 0.3175)
        on_time_label.anchored_position = (76, 111)
        self.main_group.append(on_time_label)

        off_circle_img = displayio.TileGrid(
            OFF_CIRCLE_BMP, pixel_shader=OFF_CIRCLE_BMP.pixel_shader, x=120, y=101
        )
        self.main_group.append(off_circle_img)

        off_time_label = bitmap_label.Label(DISPLAY_FONT, color=DARK_COLOR)
        off_time_label.anchor_point = (0.5, 0.3175)
        off_time_label.anchored_position = (196, 111)
        self.main_group.append(off_time_label)

    def _usno_format(self, time: datetime) -> str:
        time += timedelta(seconds=30)
        return time.strftime(USNO_TIME_FORMAT)

    def set_sunrise_sunset(self, sunrise: datetime, sunset: datetime) -> None:
        self.main_group[1].text = self._usno_format(sunrise)
        self.main_group[3].text = self._usno_format(sunset)

    def set_lamp_on_off(self, lamp_on: datetime, lamp_off: datetime) -> None:
        self.main_group[5].text = lamp_on.strftime(TIME_FORMAT)
        self.main_group[7].text = lamp_off.strftime(TIME_FORMAT)
