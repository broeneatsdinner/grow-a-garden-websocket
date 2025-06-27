# plugins/blink.py

import subprocess
import argparse

def blink(color: str, duration: float = 0, fade_ms: int = 100):
	"""
	Set the Blink(1) light to a specified color.
	- If duration > 0, sleep for that many seconds (for manual use).
	- No auto turn-off; use blink("off") explicitly when needed.
	"""
	try:
		color_map = {
			"red": "255,0,0",
			"green": "0,255,0",
			"blue": "0,0,255",
			"orange": "255,165,0",
			"white": "255,255,255",
			"yellow": "255,255,0",
			"purple": "128,0,128",
			"off": "0,0,0"
		}

		rgb = color_map.get(color.lower(), color)
		subprocess.run(["blink1-tool", "--rgb", rgb, "--millis", str(fade_ms)], check=True)

	except Exception as e:
		print(f"⚠️  Error while blinking: {e}")

if __name__ == "__main__":
	import time
	import sys

	parser = argparse.ArgumentParser(description="Trigger a Blink(1) light color.")
	parser.add_argument("-c", "--color", type=str, default="green",
	                    help="Color name or R,G,B (e.g. 'red' or '255,0,0')")
	parser.add_argument("-d", "--duration", type=float, default=0,
	                    help="Optional duration in seconds to keep light on")
	parser.add_argument("-f", "--fade", type=int, default=100,
	                    help="Fade duration in milliseconds (default: 100ms)")
	args = parser.parse_args()

	blink(args.color, fade_ms=args.fade)
	if args.duration > 0:
		time.sleep(args.duration)
