from lib.display import *
import time
matrix = Matrix()
while True:
    matrix.set_manual(0, (0, 0, 200))
    time.sleep(1.0)
    matrix.reset()
    time.sleep(1.0)
matrix.reset()