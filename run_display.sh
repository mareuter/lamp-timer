#!/bin/bash

# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

cd /home/lamptimer
source .env/bin/activate
python -u run_display.py
