# plugins/blink.py

import subprocess
import argparse

def blink(color: str, fade_ms: int = 100, brightness_pct: int = 100):
	"""
	Set the Blink(1) light to a specified color.
	- color: name or RGB string (e.g. 'white' or '255,255,255')
	- fade_ms: fade duration in milliseconds
	- brightness_pct: human-friendly brightness (0--100%)
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
		cmd = ["blink1-tool", "--rgb", rgb, "--millis", str(fade_ms)]

		# Convert 0--100% to blink1 brightness scale (1--255)
		brightness_pct = max(0, min(100, brightness_pct))
		if brightness_pct < 100:
			brightness = max(1, round((brightness_pct / 100) * 255))
			cmd += ["--brightness", str(brightness)]

		subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

	except Exception as e:
		print(f"⚠️  Error while setting Blink(1) light: {e}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Control the Blink(1) USB light.")
	parser.add_argument("-c", "--color", type=str, default="green",
	                    help="Color name or R,G,B (e.g. 'red' or '255,0,0')")
	parser.add_argument("-f", "--fade", type=int, default=100,
	                    help="Fade-in duration in milliseconds (default: 100ms)")
	parser.add_argument("-b", "--brightness", type=int, default=100,
	                    help="Brightness (0--100 percent, default: 100)")
	args = parser.parse_args()

	blink(args.color, args.fade, args.brightness)
