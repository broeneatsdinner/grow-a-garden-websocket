#!/usr/bin/env bash
set -e  # Exit on error

# Go to the script's directory (ensures relative paths work)
cd "$(dirname "$0")"

# Default notify=1 - By default, keep MacOS notifications on
notify=1

# Check if any notifications (notify) arguments were passed when running
# this startup script
for arg in "$@"; do
	if [[ $arg == notify=* ]]; then
		notify="${arg#notify=}"
	fi
done

# Set terminal global variable for this websocket app's notifications
export GAG_NOTIFY="$notify"

# Activate the virtual environment
source venv/bin/activate

# Run the listener
python websocket_listener.py
