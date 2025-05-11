# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import os
import pathlib

SET_FILE = "hwclock-set"


def main(opts: argparse.Namespace) -> None:
    original_file = pathlib.Path(f"/lib/udev/{SET_FILE}")
    new_file = pathlib.Path(SET_FILE)
    original_lines = original_file.read_text().split(os.linesep)
    new_lines = []
    for original_line in original_lines:
        if original_line.startswith("#") or original_line == "":
            new_lines.append(original_line)
            continue
        if original_line.startswith("dev") or "hctosys" in original_line:
            new_lines.append(original_line)
            continue
        new_line = f"#{original_line}"
        new_lines.append(new_line)
    new_file.write_text(os.linesep.join(new_lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    main(args)
