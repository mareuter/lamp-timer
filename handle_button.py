# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

import argparse
import signal
import subprocess
import sys

import RPi.GPIO as GPIO


DEBOUNCE_TIME_MS = 200
DISPLAY_BUTTON = 23


def signal_handler(sig, frame) -> None:
    print("Shutting down")
    GPIO.cleanup(DISPLAY_BUTTON)
    sys.exit(0)


def toggle_display(channel) -> None:
    cmd = ["/usr/bin/pkill", "-SIGUSR2", "-f", "python run_display.py"]
    subprocess.run(cmd)


def main(opts: argparse.Namespace) -> None:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(DISPLAY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(
        DISPLAY_BUTTON,
        GPIO.FALLING,
        callback=toggle_display,
        bouncetime=DEBOUNCE_TIME_MS,
    )

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    main(args)
