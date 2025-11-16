#!/bin/bash -x

# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

function install-packages {
  sudo apt install python3-dev
}

function install-adafruit {
  python -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install requests
  pip install Adafruit-Blinka
  pip install adafruit-blinka-displayio
  pip install adafruit-circuitpython-bitmap-font
  pip install adafruit-circuitpython-display-text
  pip install adafruit-circuitpython-st7789
}

function install-display-service {
  sudo mv run-display.service display-control.service /lib/systemd/system
  sudo systemctl daemon-reload
  sudo systemctl enable run-display.service
  sudo systemctl enable display-control.service
}


######################
# Installation Process
######################
install-packages
install-adafruit
install-display-service
sudo reboot
