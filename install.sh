#!/bin/bash -x

# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

function install-adafruit {
  mkdir lamp-timer
  cd lamp-timer || return
  python3 -m venv .env
  # shellcheck disable=SC1091
  source .env/bin/activate
  pip3 install Adafruit-Blinka
  pip3 install adafruit-circuitpython-st7735r
}

function reboot {
	sudo shutdown -r now
}

######################
# Installation Process
######################
install-adafruit
# reboot
