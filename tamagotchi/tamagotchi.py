import time
import random
import math
import machine
from lib.display import Matrix, LEDRing
from lib.imu import IMU
from audio import player

# --- Hardware setup ---
left = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
right = machine.Pin(38, machine.Pin.IN, machine.Pin.PULL_UP)
matrix = Matrix()
ring = LEDRing()
imu = IMU(SDA=17, SCL=18)
mPlayer = player(None)
mPlayer.set_vol(80)

# --- Constants ---
INACTIVITY_TIMEOUT = 5
STATE_DECAY_INTERVAL = 3
ANIMATION_INTERVAL = 1.0
SHAKE_THRESHOLD = 2.5  # adjust as needed

# --- Pet state ---
pet = {
    "health": 100,
    "fun": 100,
    "menu_index": 0,
    "menu_mode": False,
    "last_action": time.time()
}

# --- Icons ---
apple = [
    ([2,6,7,8,10,11,12,13,14,15,16,17,18,19,21,22,23], (255,0,0)),
    ([2], (0,255,0))
]
drumstick = [
    ([1,2,3,5,6,7,8,10,11,12,13,16,17], (255,120,0)),
    ([7,11,12], (255,180,50)),
    ([20,21], (255,255,255))
]
menu_items = [apple, drumstick]

# --- Faces ---
faces = {
    "happy": [15, 19, 21, 22, 23],
    "neutral": [16, 17, 18],
    "sad": [20, 16, 17, 18, 24]
}

# --- Utility: LED gauge logic ---
def gauge_indices(percent, leds_top_to_bottom):
    n = len(leds_top_to_bottom)
    if percent >= 100:
        count = n
    else:
        count = max(0, min(n-1, math.ceil(percent * n / 100.0)))
    return leds_top_to_bottom[n - count:]

def gauge_color(percent, hi, mid, low):
    if percent > 80:
        return hi
    elif percent > 30:
        return mid
    else:
        return low

# --- Drawing Utilities ---
def draw_icon(icon):
    matrix.reset()
    for layer in icon:
        matrix.set_character("", indices=layer[0],
                             red=layer[1][0], green=layer[1][1], blue=layer[1][2])

def play_sound(name):
    try:
        if name == "eat":
            mPlayer.play('file://sdcard/lib/data/robot-on.wav')
        elif name == "click":
            mPlayer.play('file://sdcard/lib/data/button.wav')
    except:
        pass

def feed_pet():
    play_sound("eat")
    pet["health"] = min(100, pet["health"] + 25)
    update_ring()
    time.sleep(1)

def shake_pet():
    pet["fun"] = min(100, pet["fun"] + 25)
    update_ring()

def show_menu_item():
    draw_icon(menu_items[pet["menu_index"]])

# --- Button Handlers ---
def left_button(pin):
    pet["last_action"] = time.time()
    play_sound("click")
    if not pet["menu_mode"]:
        pet["menu_mode"] = True
        pet["menu_index"] = 0
    else:
        pet["menu_index"] = (pet["menu_index"] + 1) % len(menu_items)
    show_menu_item()
    time.sleep(0.2)

def right_button(pin):
    pet["last_action"] = time.time()
    if pet["menu_mode"]:
        feed_pet()
        pet["menu_mode"] = False
    else:
        pet["menu_mode"] = True
        show_menu_item()
    time.sleep(0.2)

left.irq(trigger=machine.Pin.IRQ_FALLING, handler=left_button)
right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_button)

# --- LED Ring update ---
def update_ring():
    ring.reset()

    # Health gauge (left side)
    health_leds = [11,10,9,8,7,6]
    health_on = gauge_indices(pet["health"], health_leds)
    health_color = gauge_color(pet["health"], (0,150,0), (150,150,0), (150,0,0))
    for led in health_on:
        ring.set_manual(led, health_color)

    # Fun gauge (right side)
    fun_leds = [0,1,2,3,4,5]
    fun_on = gauge_indices(pet["fun"], fun_leds)
    fun_color = gauge_color(pet["fun"], (0,0,150), (150,100,0), (150,0,0))
    for led in fun_on:
        ring.set_manual(led, fun_color)

# --- Animation Frames (eyes) ---
animation_frames = [
    [6,8],       # normal eyes
    [5,7],       # look left
    [7,9],       # look right
    [6,8],       # back to center
]

# --- Main Loop ---
last_decay_time = time.time()
last_accel = imu.acceleration
frame_idx = 0
matrix.reset()

while True:
    now = time.time()

    # Detect shaking for fun
    accel = imu.acceleration
    if abs(accel[0]-last_accel[0])>SHAKE_THRESHOLD or \
       abs(accel[1]-last_accel[1])>SHAKE_THRESHOLD or \
       abs(accel[2]-last_accel[2])>SHAKE_THRESHOLD:
        shake_pet()
    last_accel = accel

    # State decay
    if now - last_decay_time >= STATE_DECAY_INTERVAL:
        last_decay_time = now
        pet["health"] = max(0, pet["health"] - 5)
        pet["fun"] = max(0, pet["fun"] - 5)

    # Exit menu after inactivity
    if pet["menu_mode"] and now - pet["last_action"] > INACTIVITY_TIMEOUT:
        pet["menu_mode"] = False
        matrix.reset()

    # Mood from average
    mood_score = (pet["health"] + pet["fun"]) / 2
    if mood_score > 70:
        face_name, face_color = "happy", (0,255,100)
    elif mood_score > 30:
        face_name, face_color = "neutral", (255,255,0)
    else:
        face_name, face_color = "sad", (255,80,0)

    # --- Render (merged) ---
    matrix.reset()
    if pet["menu_mode"]:
        show_menu_item()
    else:
        # Combine eyes (animation) + mouth (face)
        eyes = animation_frames[frame_idx]
        mouth = faces[face_name]
        all_pixels = eyes + mouth
        matrix.set_character("", indices=all_pixels,
                             red=face_color[0], green=face_color[1], blue=face_color[2])
        frame_idx = (frame_idx + 1) % len(animation_frames)

    update_ring()
    time.sleep(ANIMATION_INTERVAL)
