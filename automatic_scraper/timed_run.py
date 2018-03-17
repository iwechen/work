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

def daily_start(tasks_daily):
    """
    启动日常爬虫
    :param tasks_daily: 所有日常爬虫的list
    :return:
    """
    for task in tasks_daily:
        try:
            start(task)
        except Exception as e:
            print e


def seconds_start(task):
    """
    启动实时爬虫
    :param task: 实时爬虫
    :return:
    """
    start(task)


if __name__ == '__main__':
    task_seconds, tasks_daily = get_tasks()

    scheduler_daily = BackgroundScheduler(executors={'default': ThreadPoolExecutor(1)})
    scheduler_daily.add_job(daily_start, 'cron', hour=HOUR, minute=MIN, second=SEC, args=[tasks_daily])

    # scheduler_seconds = BackgroundScheduler(executors={'default': ThreadPoolExecutor(len(task_seconds))})
    # for task in task_seconds:
    #     scheduler_seconds.add_job(seconds_start, 'interval', seconds=task['timed'], args=[task['mod']])

    scheduler_daily.start()
    # scheduler_seconds.start()
    while True:
        time.sleep(3600)
