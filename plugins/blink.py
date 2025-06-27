# plugins/blink.py
import subprocess
import argparse
import time

# For now, testing/debugging, call this script directly with:
# python plugins/blink.py -c orange -d 5

def blink(color: str, duration: float):
	try:
		# Convert common color names to RGB
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
		rgb = color_map.get(color.lower(), color)  # Accept raw "R,G,B" too

		# Set color
		subprocess.run(["blink1-tool", "--rgb", rgb, "--duration", str(int(duration * 1000))], check=True)
		time.sleep(duration)
		# Turn off
		subprocess.run(["blink1-tool", "--off"], check=True)
	except Exception as e:
		print(f"Error while blinking: {e}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Blink(1) light trigger")
	parser.add_argument("-c", "--color", type=str, default="green", help="Color name or R,G,B (e.g. red or 255,0,0)")
	parser.add_argument("-d", "--duration", type=float, default=1.0, help="Duration in seconds")
	args = parser.parse_args()

	blink(args.color, args.duration)
