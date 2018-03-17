# coding: utf-8

import os
from main import start
from default_config import task_config, spider_path


def get_tasks():
    tasks_seconds = []
    tasks_daily = []
    task_info = {}
    for root, dirs, files in os.walk("config"+os.sep+spider_path, topdown=True):
        # print root, dirs, files
        if dirs:
            continue
        for f in files:
            if f != '__init__.py' and f.endswith('config_fre.py'):
                task_info['timed'] = task_config[f.replace('.py', '')]
                task_file = os.sep.join([root, f]).replace(os.sep, '.')
                task_info['mod'] = os.path.splitext(task_file)[0]
                tasks_seconds.append(task_info)
            if f != '__init__.py' and f.endswith('config.py'):
                task_file = os.sep.join([root, f]).replace(os.sep, '.')
                task_mod = os.path.splitext(task_file)[0]
                tasks_daily.append(task_mod)
    # start test
    # for task in tasks_daily:
    #     start(task)
    # for task in tasks_seconds:
    #     start(task['mod'])

    return tasks_seconds, tasks_daily


if __name__ == '__main__':
    get_tasks()
