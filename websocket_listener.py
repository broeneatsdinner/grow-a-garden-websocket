import asyncio
import websockets
import json
import datetime
import os
import subprocess
import time   # <<< NEW
import atexit # <<< NEW

from plugins.blink import blink, fade_up_down

# --- Blink state ---
is_light_on = False         # <<< NEW
last_blink_time = 0         # <<< NEW
cooldown_seconds = 5        # <<< NEW

# --- Ensure blink(1) turns off on exit ---
atexit.register(lambda: blink("off"))  # <<< NEW

# Define terminal color codes
WHITE = "\033[37m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

# Replace with your actual Discord user ID
DISCORD_USER_ID = "YOUR_DISCORD_ID_HERE"

# Load keywords from keywords.txt (one per line, case-insensitive)
def load_keywords():
	keywords = set()
	try:
		with open("keywords.txt", "r") as f:
			for line in f:
				kw = line.strip().lower()
				if kw:
					keywords.add(kw)
	except FileNotFoundError:
		pass
	return keywords

# Get current timestamp string
def current_timestamp():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# macOS notification helper
def notify(title, message):
	if os.getenv("GAG_NOTIFY", "0") != "1":
		return  # Notifications are disabled

	title = title.replace('"', '\\"')
	message = message.replace('"', '\\"')
	subprocess.run([
		"osascript",
		"-e",
		f'display notification "{message}" with title "{title}" sound name "Funk"'
	])

async def listen():
	global is_light_on, last_blink_time   # <<< Needed to modify globals

	url = f"wss://websocket.joshlei.com/growagarden?user_id={DISCORD_USER_ID}"
	# Removed upfront keywords load --- now reloaded live

	# Define the stock sections in the order you want to print them
	STOCK_ORDER = [
		"WEATHER",
		"EVENTSHOP_STOCK",
		"COSMETIC_STOCK",
		"EGG_STOCK",
		"SEED_STOCK",
		"GEAR_STOCK"
	]

	while True:  # ✅ Keep reconnecting forever
		try:
			async with websockets.connect(
				url,
				ping_interval=30,
				ping_timeout=10
			) as ws:
				print("✅  Connected to Grow a Garden WebSocket.\nWaiting for stock updates...\n")
				notify("🌱  Connected to Grow a Garden WebSocket", "Waiting for stock updates...")

				while True:
					raw = await ws.recv()
					data = json.loads(raw)
					timestamp = current_timestamp()
					alerted = []
					keywords = load_keywords()  # <<< NEW: reload each stock update

					# Collect output chunks by section
					chunks = {}

					for section, items in data.items():
						section_upper = section.upper()
						lines = [f"\n🗂️  {section_upper} @ {timestamp}"]

						if section_upper == "WEATHER":
							active_items = [w for w in items if w.get("active")]

							if not active_items:
								lines.append("  (No active weather event)")
							else:
								for item in active_items:
									name = item.get("weather_name", item.get("weather_id", "Unknown"))
									start_unix = item.get("start_duration_unix", 0)
									end_unix = item.get("end_duration_unix", 0)
									start = datetime.datetime.fromtimestamp(start_unix).strftime('%H:%M:%S') if start_unix else "?"
									end = datetime.datetime.fromtimestamp(end_unix).strftime('%H:%M:%S') if end_unix else "?"
									lines.append(f"  - {name} ({start} → {end})")

							chunks[section_upper] = "\n".join(lines)
							continue

						for item in items:
							name = item.get("display_name", "Unknown")
							qty = item.get("quantity", 0)
							lines.append(f"  - {name} × {qty}")
							if name.lower() in keywords:
								alerted.append(f"{name} × {qty}")

						chunks[section_upper] = "\n".join(lines)

					# Print sections in defined order
					for section in STOCK_ORDER:
						if section in chunks:
							print(chunks[section])

					for section in sorted(chunks):
						if section not in STOCK_ORDER:
							print(chunks[section])

					# <<< NEW: Debounce blink logic
					current_time = time.time()   # <<<

					if alerted:
						def format_alert(item_str):
							name, qty = item_str.rsplit(" × ", 1)
							return f"{WHITE}{name}{RESET} × {ORANGE}{qty}{RESET}"

						summary = ", ".join(format_alert(a) for a in alerted)
						print(f"\n🔔  Matched keywords this update: {summary}")
						notify("🌱  Grow a Garden Stock Alert", ", ".join(alerted))

						if not is_light_on or (current_time - last_blink_time) > cooldown_seconds:
							fade_up_down(up_ms=500, hold_ms=0, down_ms=30000)  # fade in 0.5 sec → no hold → fade out 30 seconds
							is_light_on = True
							last_blink_time = current_time
					else:
						if is_light_on:
							blink("off", fade_ms=100)
							is_light_on = False

		except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
			print(f"⚠️  Connection closed: {e} --- reconnecting in 5s...")
			await asyncio.sleep(5)

		except Exception as e:
			print(f"⚠️  Error: {e} --- reconnecting in 5s...")
			await asyncio.sleep(5)

async def main():
	await listen()

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("\n👋  Exiting cleanly.")
