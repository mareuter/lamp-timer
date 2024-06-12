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
  # Debian bookworm requires next two lines
  pip uninstall -y rpi-gpio
  pip install rpi-lgpio
}

function install-service {
  sudo mv init-lamptimer.service /lib/systemd/system
  sudo systemctl daemon-reload
  sudo systemctl enable init-lamptimer.service
}


######################
# Installation Process
######################
rm lamptimer.tar.gz
fixup-settings
install-packages
install-adafruit
install-service
sudo reboot
