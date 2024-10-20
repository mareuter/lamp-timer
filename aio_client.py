# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

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
        settings_file = pathlib.Path("settings.toml")

        with settings_file.open("rb") as cfile:
            cdict = tomllib.load(cfile)
        return cdict

    def publish_data(self) -> None:
        """Publish data to Adafruit IO."""
        self.client.send_data(f"{self.feed_group}.notifier", 1)
