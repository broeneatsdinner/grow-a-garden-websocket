import asyncio
import websockets
import json
import datetime
import os
import subprocess
from plugins.blink import blink

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
	url = f"wss://websocket.joshlei.com/growagarden?user_id={DISCORD_USER_ID}"
	keywords = load_keywords()

	# Define the stock sections in the order you want to print them
	STOCK_ORDER = [
		"WEATHER",
		"EVENTSHOP_STOCK",
		"COSMETIC_STOCK",
		"EGG_STOCK",
		"SEED_STOCK",
		"GEAR_STOCK"
	]

	while True:  # ✅ New: keep reconnecting forever
		try:
			# ✅ Add ping_interval to send heartbeats every 30 sec
			async with websockets.connect(
				url,
				ping_interval=30,  # keepalive ping every 30 sec
				ping_timeout=10    # if no pong in 10 sec, consider it dead
			) as ws:
				print("✅  Connected to Grow a Garden WebSocket.\nWaiting for stock updates...\n")
				notify("🌱  Connected to Grow a Garden WebSocket", "Waiting for stock updates...")

				while True:
					# Receive a stock update
					raw = await ws.recv()
					data = json.loads(raw)
					timestamp = current_timestamp()
					alerted = []

					# Collect output chunks by section
					chunks = {}

					for section, items in data.items():
						section_upper = section.upper()
						lines = [f"\n🗂️  {section_upper} @ {timestamp}"]

						# Special case: WEATHER
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

						# Example WEATHER debug block (keep commented if unused)
						# if section_upper == "WEATHER":
						# 	print(f"\n🐞  DEBUG WEATHER RAW:\n{json.dumps(items, indent=2)}\n")
						# 	if not items:
						# 		lines.append("  (No active weather event)")
						# 	else:
						# 		for item in items:
						# 			name = item.get("display_name", item.get("weather_id", "Unknown"))
						# 			start = item.get("Date_Start", "")
						# 			end = item.get("Date_End", "")
						# 			lines.append(f"  - {name} ({start} → {end})")
						# 	chunks[section_upper] = "\n".join(lines)
						# 	continue

						# Standard stock handling
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

					# Print any unmatched sections last
					for section in sorted(chunks):
						if section not in STOCK_ORDER:
							print(chunks[section])

					if alerted:
						def format_alert(item_str):
							name, qty = item_str.rsplit(" × ", 1)
							return f"{WHITE}{name}{RESET} × {ORANGE}{qty}{RESET}"

						summary = ", ".join(format_alert(a) for a in alerted)
						print(f"\n🔔  Matched keywords this update: {summary}")
						notify("🌱  Grow a Garden Stock Alert", ", ".join(alerted))
						blink("white", fade_ms=100, brightness_pct=100)  # Turn on and stay on
					else:
						blink("off", fade_ms=100)  # Turn off

		# ✅ These exceptions mean the connection closed: reconnect
		except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
			print(f"⚠️  Connection closed: {e} --- reconnecting in 5s...")
			await asyncio.sleep(5)

		# ✅ Any other error: log + reconnect
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
