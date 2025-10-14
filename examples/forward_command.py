from lib.kinematics import Crawler
crawler = Crawler()
for i in range(3):
    crawler.command("forward")
crawler.pca.all_off()