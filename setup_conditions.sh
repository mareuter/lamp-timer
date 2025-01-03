#!/bin/bash

# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

cd /home/lamptimer
source .venv/bin/activate
python -u setup_conditions.py
cat crontab.in | crontab -
rm crontab.in
if [ -f "lamp_on" ]; then
  ./lamp_on.sh
  rm lamp_on
fi
