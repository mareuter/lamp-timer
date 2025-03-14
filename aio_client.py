# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import json
import pathlib
import tomllib

from Adafruit_IO import Client

__all__ = ["AioClient"]


class AioClient:
    def __init__(self) -> None:
        """Class constructor."""
        settings = self._get_settings()
        self.client = Client(settings["AIO_USERNAME"], settings["AIO_KEY"])
        self.feed_group = settings["AIO_GROUP"]

    def _get_settings(self) -> dict[str, str]:
        """Parse the settings.

        Returns
        -------
        dict[str, str]
            The parsed settings.
        """
        settings_file = pathlib.Path(".settings.toml")

        with settings_file.open("rb") as cfile:
            cdict = tomllib.load(cfile)
        return cdict

    def publish_notifier(self) -> None:
        """Publish notifier to Adafruit IO."""
        self.client.send_data(f"{self.feed_group}.notifier", 1)

    def publish_timer_info(self) -> None:
        """Publish lamp timer information to Adafruit IO."""
        conditions_file = pathlib.Path("conditions.json")
        with conditions_file.open() as ifile:
            conditions = json.load(ifile)
        timer_info_list = [
            f"sunrise={conditions['sunrise']}",
            f"sunset={conditions['sunset']}",
            f"on={conditions['lamp_on']}",
            f"off={conditions['lamp_off']}",
        ]
        timer_info = ",".join(timer_info_list)
        self.client.send_data(f"{self.feed_group}.lamptimer", timer_info)
