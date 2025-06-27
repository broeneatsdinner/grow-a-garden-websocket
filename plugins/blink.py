# plugins/blink.py

import subprocess
import argparse
import time
import math

def blink(color: str, fade_ms: int = 100, brightness_pct: int = 100):
	"""
	Set the Blink(1) light to a specified color.
	"""
	try:
		# Clear any previously queued patterns/commands
		subprocess.run(["blink1-tool", "--clear"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

		brightness_pct = max(0, min(100, brightness_pct))
		if brightness_pct < 100:
			brightness = max(1, round((brightness_pct / 100) * 255))
			cmd += ["--brightness", str(brightness)]

		subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

	except Exception as e:
		print(f"⚠️  Error while setting Blink(1) light: {e}")

def boop_wave(color: str = "orange", fade_ms: int = 100, delay: float = 0.3):
	"""
	Play a jagged rising brightness wave.
	"""
	levels = [0, 10, 5, 20, 15, 40, 30, 60, 50, 80, 70, 100]
	for level in levels:
		blink(color=color, fade_ms=fade_ms, brightness_pct=level)
		time.sleep(delay)

def boop_easeout(color: str = "orange", fade_ms: int = 50, delay: float = 0.05, steps: int = 20):
	"""
	Fade in brightness using ease-out exponential curve.
	"""
	for i in range(steps + 1):
		t = i / steps
		brightness = round((1 - math.pow(2, -10 * t)) * 100)
		blink(color=color, fade_ms=fade_ms, brightness_pct=brightness)
		time.sleep(delay)

def boop_easein(color: str = "orange", fade_ms: int = 50, delay: float = 0.05, steps: int = 20):
	"""
	Fade in brightness using ease-in exponential curve.
	"""
	for i in range(steps + 1):
		t = i / steps
		brightness = round(math.pow(2, 10 * (t - 1)) * 100)
		brightness = min(100, max(0, brightness))
		blink(color=color, fade_ms=fade_ms, brightness_pct=brightness)
		time.sleep(delay)

def boop_easeinout(color: str = "orange", fade_ms: int = 50, delay: float = 0.05, steps: int = 40):
	"""
	Smooth fade-in and fade-out using easeInOutExponential.
	"""
	for i in range(steps + 1):
		t = i / steps
		if t < 0.5:
			brightness = round((math.pow(2, 20 * t - 10)) / 2 * 100)
		else:
			brightness = round((2 - math.pow(2, -20 * t + 10)) / 2 * 100)
		brightness = min(100, max(0, brightness))
		blink(color=color, fade_ms=fade_ms, brightness_pct=brightness)
		time.sleep(delay)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Control the Blink(1) USB light.")
	parser.add_argument("-c", "--color", type=str, default="green",
	                    help="Color name or R,G,B (e.g. 'red' or '255,0,0')")
	parser.add_argument("-f", "--fade", type=int, default=100,
	                    help="Fade-in duration in milliseconds")
	parser.add_argument("-b", "--brightness", type=int, default=100,
	                    help="Brightness (0--100 percent)")
	parser.add_argument("--wave", action="store_true",
	                    help="Play jagged brightness wave")
	parser.add_argument("--easeout", action="store_true",
	                    help="Play exponential ease-out brightness")
	parser.add_argument("--easein", action="store_true",
	                    help="Play exponential ease-in brightness")
	parser.add_argument("--easeinout", action="store_true",
	                    help="Play ease-in-out exponential brightness")
	parser.add_argument("--off", action="store_true",
	                    help="Turn the Blink(1) light off")

	args = parser.parse_args()

	if args.off:
		blink("off")
	elif args.easeinout:
		boop_easeinout(color=args.color, fade_ms=args.fade)
	elif args.easeout:
		boop_easeout(color=args.color, fade_ms=args.fade)
	elif args.easein:
		boop_easein(color=args.color, fade_ms=args.fade)
	elif args.wave:
		boop_wave(color=args.color, fade_ms=args.fade)
	else:
		blink(args.color, args.fade, args.brightness)
