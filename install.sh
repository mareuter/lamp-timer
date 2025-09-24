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

function install-lamptimer-service {
  sudo mv init-lamptimer.service /lib/systemd/system
  sudo systemctl daemon-reload
  sudo systemctl enable init-lamptimer.service
}

function install-mta {
  sudo mv sendmail /usr/sbin
  sudo mkdir /var/tmp/cron
  sudo chmod 777 /var/tmp/cron
  sudo mv clean-mta-logs /etc/cron.weekly
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
install-mta
install-gpio
install-aio
install-lamptimer-service
cleanup
sudo reboot
