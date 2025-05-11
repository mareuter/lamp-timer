# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import os
import pathlib
import tarfile


def main(opts: argparse.Namespace) -> None:
    tfile = pathlib.Path("lamptimer.tar")
    manifest = pathlib.Path("manifest.txt")
    manifest_display = pathlib.Path("manifest-display.txt")
    with tarfile.open(tfile, "w") as tar:
        for ifile in manifest.read_text().strip().split(os.linesep):
            tar.add(ifile)
        if opts.display:
            for dfile in manifest_display.read_text().strip().split(os.linesep):
                tar.add(dfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--display", action="store_true", help="Add display related files."
    )

    args = parser.parse_args()
    main(args)
