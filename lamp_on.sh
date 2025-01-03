#!/bin/bash

# SPDX-FileCopyrightText: 2024-2025 Michael Reuter
#
# SPDX-License-Identifier: MIT

cd /home/lamptimer
source .venv/bin/activate
python -u control_lamp.py 1
