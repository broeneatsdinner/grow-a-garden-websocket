# Grow a Garden on Roblox
## WebSocket Listener

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

Listens for live stock updates from the **Grow a Garden** Roblox game and alerts you when specific items appear.

## Features
- Real-time updates via WebSocket
- Configurable keyword alerts
- macOS desktop notifications (`osascript`)
- Weather event display
- Toggle notifications via CLI (`notify=1` or `notify=0`)

## Requirements
- Python 3.8+
- macOS (for notification support)
- Internet connection

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a keywords.txt file and add one item per line (case-insensitive), e.g.:
```
Advanced Sprinkler
Carrot
```

## Running

```bash
./start.sh notify=1  # Enable macOS notifications
./start.sh           # Also runs with notifications off (default)
./start.sh notify=0  # Explicitly disable notifications
```

Edit **websocket_listener.py** and replace YOUR_DISCORD_ID_HERE with your Discord User ID.

>  [How to find your Discord User ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID).

## Notes

- This script is macOS-only (uses osascript for notifications).
- Tested on macOS 14+ with iTerm2.
- PRs welcome!
