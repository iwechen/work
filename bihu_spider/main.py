from bihu.spider import BihuSpider
import os
import time

while True:
    # os.system('python3 BihuSpider')
    bh = BihuSpider()
    bh.run()

    time.sleep(1200)
 


