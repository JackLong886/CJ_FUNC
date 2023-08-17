import time
from utils.timer import Timer

if __name__ == '__main__':
    startup_timer = Timer()
    time.sleep(2)
    startup_timer.record('wait 2s')
    time.sleep(1)
    startup_timer.record('wait 1s')
    print(f"Startup time: {startup_timer.summary()}.")

