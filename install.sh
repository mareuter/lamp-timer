#!/bin/bash -x

# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

function fixup-settings {
  mv settings.toml .settings.toml
  chmod 600 .settings.toml
}

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

function install-gpio {
  python -m venv .venv2
  # shellcheck disable=SC1091
  source .venv2/bin/activate
  pip install rpi-lgpio
}

function install-service {
  sudo mv init-lamptimer.service run-display.service display-control.service /lib/systemd/system
  sudo systemctl daemon-reload
  sudo systemctl enable init-lamptimer.service
  sudo systemctl enable run-display.service
  sudo systemctl enable display-control.service
}


######################
# Installation Process
######################
rm lamptimer.tar.gz
fixup-settings
install-packages
install-adafruit
install-gpio
install-service
sudo reboot
