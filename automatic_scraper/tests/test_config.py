# coding: utf-8

import unittest
import sys
import os
sys.path.append('..')


tasks = []
for root, dirs, files in os.walk(os.pardir + os.sep + "config", topdown=True):
    if dirs:
        continue
    for f in files:
        if f != '__init__.py' and f.endswith('.py'):
            task_mod = os.sep.join([root, f]).replace(os.sep, '.').strip('.py')
            tasks.append(task_mod)

class ConfigTest(unittest.TestCase):
    def test_task(self):
        pass


if __name__ == '__main__':
    unittest.main()