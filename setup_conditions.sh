#!/bin/bash

# SPDX-FileCopyrightText: 2024 Michael Reuter
#
# SPDX-License-Identifier: MIT

cd /home/lamptimer
source .venv/bin/activate
python -u setup_conditions.py
# crontab -e < cat crontab.in
# rm crontab.in
