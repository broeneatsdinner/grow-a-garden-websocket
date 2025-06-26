# Grow a Garden WebSocket Listener

Listens for live stock updates from the Grow a Garden game and alerts when specific items appear.

## Features
- Real-time updates via WebSocket
- Keyword alerts (configurable)
- macOS desktop notifications
- Weather event display
- Toggle notifications on/off via CLI

## Requirements
- Python 3.8+
- macOS (for notification support via `osascript`)
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
./start.sh notify=0  # Disable notifications (default)
```

Edit **websocket_listener.py** and replace YOUR_DISCORD_ID_HERE with your Discord ID.

> You can find your Discord user ID [using these steps](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID).

## Notes

- This script is designed for macOS (uses osascript for notifications).
- Tested on macOS 14+ and iTerm2.

 PRs welcome!
