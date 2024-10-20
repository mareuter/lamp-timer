# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

from aio_client import AioClient


def main() -> None:
    client = AioClient()
    client.publish_data()


if __name__ == "__main__":
    main()
