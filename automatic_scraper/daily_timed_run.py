# coding:utf-8
from datetime import datetime
import time
from run import get_tasks
from main import start
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from default_config import HOUR, MIN, SEC


# import logging

# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)  # DEBUG
#
# fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
# h = logging.StreamHandler()
# h.setFormatter(fmt)
# log.addHandler(h)

def daily_start():
    """
    启动日常爬虫
    :param tasks_daily: 所有日常爬虫的list
    :return:
    """
    task_seconds, tasks_daily = get_tasks()
    for task in tasks_daily:
        start(task)



if __name__ == '__main__':


    scheduler_daily = BackgroundScheduler(executors={'default': ThreadPoolExecutor(1)})
    scheduler_daily.add_job(daily_start, 'cron', hour=HOUR, minute=MIN, second=SEC)

    scheduler_daily.start()
    while True:
        time.sleep(3600)
