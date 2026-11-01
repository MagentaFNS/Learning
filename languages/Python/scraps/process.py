import time
import sys

empty = "░"
process = "█"
total = 20

# имитация установки
for i in range(total + 1):
    bar = process * i + empty * (total - i)
    percent = int(i / total * 100)
    sys.stdout.write(f"\r{bar} {percent}%")
    sys.stdout.flush()
    time.sleep(0.15)
