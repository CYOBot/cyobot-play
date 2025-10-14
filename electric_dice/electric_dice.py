from lib.display import *
import random
import time
from lib.imu import *

matrix = Matrix()
imu = IMU()

dice = {
   1: [12],
   2: [0, 24],
   3: [4, 12, 20],
   4: [0, 4, 20, 24],
   5: [0, 4, 12, 20, 24],
   6: [0, 4, 10, 14, 20, 24]
}

matrix.reset()
value = 1
prev_accel = imu.acceleration
matrix.set_character("", indices=dice[value], red=100, green=20, blue=50)

while True:
   accel = imu.acceleration
   if accel[0] - prev_accel[0] > 2.0:
       for i in range(20):
           value = random.randint(1, 6)
           matrix.reset()
           matrix.set_character("", indices=dice[value], red=100, green=20, blue=50)
           time.sleep(0.1)

   prev_accel = accel
   time.sleep(0.001)