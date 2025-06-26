import asyncio
import websockets
import json
import datetime
import os
import subprocess

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

	async with websockets.connect(url) as ws:
		print("✅  Connected to Grow a Garden WebSocket.\nWaiting for stock updates...\n")
		notify("🌱  Connected to Grow a Garden WebSocket", "Waiting for stock updates...")
		while True:
			try:
				raw = await ws.recv()
				data = json.loads(raw)
				timestamp = current_timestamp()
				alerted = []

				for section, items in data.items():
					print(f"\n🗂️  {section.upper()} @ {timestamp}")

					# Special handling for WEATHER section
					if section.lower() == "weather":
						if not items:
							print("  (No active weather event)")
							continue
						for item in items:
							# Use display_name if available, otherwise fallback to weather_id
							name = item.get("display_name", item.get("weather_id", "Unknown"))
							start = item.get("Date_Start", "")
							end = item.get("Date_End", "")
							print(f"  - {name} ({start} → {end})")
						continue  # Skip standard stock processing for weather

					# Standard handling for all other stock sections (seed, gear, egg, etc.)
					for item in items:
						name = item.get("display_name", "Unknown")
						qty = item.get("quantity", 0)
						print(f"  - {name} × {qty}")

						# Alert if item name matches any keyword
						if name.lower() in keywords:
							alerted.append(f"{name} × {qty}")

				if alerted:
					def format_alert(item_str):
						name, qty = item_str.rsplit(" × ", 1)
						return f"{WHITE}{name}{RESET} × {ORANGE}{qty}{RESET}"

					summary = ", ".join(format_alert(a) for a in alerted)
					print(f"\n🔔  Matched keywords this update: {summary}")
					notify("🌱  Grow a Garden Stock Alert", ", ".join(alerted))  # keep notification plain

			except Exception as e:
				print("⚠️  Error:", e)
				await asyncio.sleep(5)

async def main():
	await listen()

if __name__ == "__main__":
	asyncio.run(main())
