# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import os
import pathlib
import tarfile


def main() -> None:
    tfile = pathlib.Path("lamptimer.tar")
    manifest = pathlib.Path("manifest.txt")
    with tarfile.open(tfile, "w") as tar:
        for ifile in manifest.read_text().split(os.linesep):
            tar.add(ifile)


if __name__ == "__main__":
    main()
