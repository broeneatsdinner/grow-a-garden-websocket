# 🔵 Standard blink
python plugins/blink.py -c blue -f 100 -b 60

# 🟠 Jagged wave
python plugins/blink.py --wave -c orange -f 100

# 🟡 Ease-out exponential
python plugins/blink.py --easeout -c yellow -f 9000

# 🟣 Ease-in exponential
python plugins/blink.py --easein -c purple -f 9000

# ⚪ Ease-in-out exponential
python plugins/blink.py --easeinout -c white -f 1000

# ⚫ Turn off manually
python plugins/blink.py --off
