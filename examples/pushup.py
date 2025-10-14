from lib.kinematics import Crawler
crawler = Crawler()
import time
crawler.centeredDynamicServoAssignment(-40, 0, -40, 0, -40, 0, -40, 0)
for count in range(3):
  crawler.centeredDynamicServoAssignment(-40, 30, -40, 0, -40, 0, -40, 30)
  crawler.centeredDynamicServoAssignment(-40, -30, -40, 0, -40, 0, -40, -30)
crawler.pca.all_off()