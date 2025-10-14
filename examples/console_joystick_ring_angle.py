import machine
import math
import time
from lib.display import *

ring = LEDRing()

lefty = machine.ADC(5)
leftx = machine.ADC(2)
lefty.atten(leftx.ATTN_11DB)
leftx.atten(lefty.ATTN_11DB)

while True:
    dx = leftx.read() - 2048
    dy = 2048 - lefty.read()

    angle_radians = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle_radians)
    angle_degrees = (angle_degrees + 90) % 360
    led_index = int(angle_degrees / 30)

    ring.reset()
    ring.set_manual(led_index, (50, 100, 20))

    time.sleep(0.05)