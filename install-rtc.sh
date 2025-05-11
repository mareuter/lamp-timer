#!/bin/bash -x

# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

function cleanup {
  if [ -f ".complete.tmp" ]; then
    rm .mv_config.tmp
    rm .complete.tmp
  fi
}

function fixup_hwclock_set {
  file_loc="/lib/udev"
  set_file="${file_loc}/hwclock-set"
  sudo cp ${set_file} "${set_file}.bak"
  touch hwclock-set
  chmod 755 hwclock-set
  python fixup_hwclock_set.py
  sudo mv hwclock-set ${file_loc}
}

function move_config {
  if [ ! -f ".mv_config.tmp" ]; then
    sudo mv config.txt /boot/firmware
    touch .mv_config.tmp
    sudo halt
  else
    sudo i2cdetect -y 1
  fi
}

function remove_fake_hwclock {
  sudo apt -y remove fake-hwclock
  sudo update-rc.d -f fake-hwclock remove
  sudo systemctl disable fake-hwclock
}

function set_hwclock {
  sudo hwclock -r
  date
  sleep 5
  sudo hwclock -w
  sudo hwclock -r
  sleep 5
  touch .complete.tmp
}

move_config
remove_fake_hwclock
fixup_hwclock_set
set_hwclock
cleanup
