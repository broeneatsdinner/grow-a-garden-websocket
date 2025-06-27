# plugins/blink.py

import subprocess
import argparse
import time

def blink(color: str, duration: float, fade_ms: int = 100):
	"""
	Set the Blink(1) light to a specified color for a given duration.
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
		time.sleep(duration)
		subprocess.run(["blink1-tool", "--off"], check=True)

	except Exception as e:
		print(f"⚠️  Error while blinking: {e}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Trigger a Blink(1) light color pulse.")
	parser.add_argument("-c", "--color", type=str, default="green",
	                    help="Color name or R,G,B (e.g. 'red' or '255,0,0')")
	parser.add_argument("-d", "--duration", type=float, default=1.0,
	                    help="How long to keep the light on (in seconds)")
	parser.add_argument("-f", "--fade", type=int, default=100,
	                    help="Fade-in duration in milliseconds (default: 100ms)")
	args = parser.parse_args()

	blink(args.color, args.duration, args.fade)
