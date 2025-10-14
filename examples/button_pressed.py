import time
import machine
left = machine.Pin(4, machine.Pin.IN)
from lib.display import Matrix
matrix = Matrix()
while True:
  if (left.value()) == 0:
    matrix.set_manual(0, (64, 255, 64))
  else:
    matrix.reset()
  time.sleep(0.001)
matrix.reset()