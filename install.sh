#!/bin/bash -x

# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

function install-adafruit {
  python -m venv .env
  # shellcheck disable=SC1091
  source .env/bin/activate
  pip install requests
  pip install Adafruit-Blinka
  pip install adafruit-circuitpython-st7735r
  pip install adafruit-circuitpython-bitmap-font
  pip install adafruit-circuitpython-display-text
}

function reboot {
	sudo shutdown -r now
}

######################
# Installation Process
######################
install-adafruit
# reboot
