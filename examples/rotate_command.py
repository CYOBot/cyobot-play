from lib.kinematics import Crawler
crawler = Crawler()
for i in range(3):
    crawler.command("rotate_left")
crawler.pca.all_off()