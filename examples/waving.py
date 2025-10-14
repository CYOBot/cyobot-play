from lib.kinematics import Crawler
crawler = Crawler()
import time
for count in range(3):
  for i in range(-30, 31):
    crawler.pca.set_angle(0, i)
    time.sleep(0.02)
  for i in range(30, -31, -1):
    crawler.pca.set_angle(0, i)
    time.sleep(0.02)
crawler.pca.all_off()