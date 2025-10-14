import machine
import time
from lib.display import LEDRing

lefty = machine.ADC(5)
leftx = machine.ADC(2)
leftx.atten(leftx.ATTN_11DB)
lefty.atten(lefty.ATTN_11DB)
ring = LEDRing()

while True:
  if (leftx.read()) > 3000:
    ring.set_manual(3, (64, 255, 64))
  elif (leftx.read()) < 1000:
    ring.set_manual(9, (64, 255, 64))
  if (lefty.read()) > 3000:
    ring.set_manual(0, (64, 255, 64))
  elif (lefty.read()) < 1000:
    ring.set_manual(6, (64, 255, 64))
  ring.reset()
  time.sleep(0.001)