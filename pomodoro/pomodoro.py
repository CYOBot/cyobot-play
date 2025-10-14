from lib.display import *
import machine
import time
import _thread
from audio import player

# Initialize audio, pins, LED ring and matrix
mPlayer = player(None)
mPlayer.set_vol(100)
left = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
right = machine.Pin(38, machine.Pin.IN, machine.Pin.PULL_UP)
ring = LEDRing()
matrix = Matrix()

# Global timer variables
set_minutes = 0      # Timer length in minutes (set via left button, max 60)
running = False      # Timer running state
elapsed_seconds = 0  # Time elapsed in seconds

matrix.reset()
ring.reset()
mPlayer.stop()

# Helper function to update the LED ring progress
def update_led_ring_progress():
    global set_minutes, running
    total_seconds = set_minutes * 60
    seconds_left = total_seconds - elapsed_seconds
    fraction = (seconds_left + 4*60 + 59) / 3600
    num_leds = int(fraction * 12)
    ring.reset()
    for i in range(num_leds):
        ring.set_manual(i, (200, 20, 50))  # Color for progress

# Helper function to visually indicate the set time on the LED ring.
def update_led_ring_set_time():
    ring.reset()
    leds_to_light = int(((set_minutes + 4) / 60) * 12)
    for i in range(leds_to_light):
        ring.set_manual(i, (50, 150, 50))  # Color for set time

# Function to scroll the remaining minutes on the LED matrix.
def update_matrix_countdown():
    # Calculate the remaining minutes
    minutes_remaining = max(0, set_minutes - (elapsed_seconds // 60))
    # Scroll the remaining minutes as text
    matrix.scroll("{}".format(int(minutes_remaining)), red=200, green=20, blue=50, speed=0.1)

# The timer function running on a separate thread.
def timer_thread():
    global elapsed_seconds, running
    start_time = time.time()
    blink_on = False
    matrix.reset()
    while running and elapsed_seconds < set_minutes * 60:
        elapsed_seconds = int(time.time() - start_time)
        update_led_ring_progress()
        if blink_on:
            matrix.reset()
            blink_on = False
        else:
            matrix.set_character("", indices={7, 17}, red=200, green=20, blue=50)
            blink_on = True
        time.sleep(1)
    # Timer complete – play alarm if a valid duration was set.
    if elapsed_seconds >= set_minutes * 60 and set_minutes > 0:
        mPlayer.play('file://sdcard/lib/data/alarm.mp3')
    # Reset timer state and clear LED ring.
    running = False
    elapsed_seconds = 0
    ring.reset()

# Left button handler: Increase the timer (only allowed when not running).
def left_button_handler(pin):
    global set_minutes
    if not running:
        set_minutes = min(set_minutes + 1, 60)
        update_led_ring_set_time()
        matrix.reset()
        matrix.set_character("{}".format(int(set_minutes % 10)), red=50, green=150, blue=50)
    else:
        update_matrix_countdown()
    time.sleep(0.1)

# Right button handler: Toggle the timer start/stop.
def right_button_handler(pin):
    global running, elapsed_seconds, mPlayer, set_minutes, scanning_effect_timer
    if not running and set_minutes > 0:
        mPlayer.play('file://sdcard/lib/data/robot-on.wav')
        time.sleep_ms(200)
        running = True
        elapsed_seconds = 0
        _thread.start_new_thread(timer_thread, ())
    elif running:
        mPlayer.play('file://sdcard/lib/data/button.wav')
        time.sleep_ms(200)
        running = False
        elapsed_seconds = 0
        set_minutes = 0
        ring.reset()
        matrix.reset()
        mPlayer.stop()
    time.sleep(0.1)

# Attach interrupt handlers to the buttons.
left.irq(trigger=machine.Pin.IRQ_FALLING, handler=left_button_handler)
right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_button_handler)

# Main loop (could be used for other tasks if needed)
while True:
    time.sleep(0.1)
