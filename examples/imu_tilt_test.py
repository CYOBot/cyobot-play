from lib.display import Matrix
matrix = Matrix()
import time
from lib.imu import IMU
imu = IMU(SDA=17, SCL=18)
while True:
  if (imu.gyro[1]) < -1:
    matrix.set_manual(20, (64, 255, 64))
  elif (imu.gyro[1]) > 1:
    matrix.set_manual(12, (64, 255, 64))
  elif (imu.gyro[0]) < -1:
    matrix.set_manual(2, (64, 255, 64))
  elif (imu.gyro[0]) > 1:
    matrix.set_manual(30, (64, 255, 64))
  else:
    matrix.reset()
  time.sleep(0.001)