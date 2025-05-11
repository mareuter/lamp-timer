#!/bin/bash -x

# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

function cleanup {
  rm ".upgrade.tmp"
}

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

function install-aio {
  python -m venv .venv3
  # shellcheck disable=SC1091
  source .venv3/bin/activate
  pip install adafruit-io
}

function install-service {
  sudo mv init-lamptimer.service run-display.service display-control.service /lib/systemd/system
  sudo systemctl daemon-reload
  sudo systemctl enable init-lamptimer.service
  sudo systemctl enable run-display.service
  sudo systemctl enable display-control.service
}

function turn-off-wlan-power-save {
  sudo iw wlan0 set power_save off
}

function update-os {
	if [ ! -f ".upgrade.tmp" ]; then
		sudo apt update
		sudo apt upgrade -y
		touch ".upgrade.tmp"
		sudo reboot
	fi
}


######################
# Installation Process
######################
rm lamptimer.tar.gz
fixup-settings
update-os
turn-off-wlan-power-save
install-packages
install-adafruit
install-gpio
install-aio
install-service
cleanup
sudo reboot
