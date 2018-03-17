# coding: utf-8

import importlib

from main import start
from config.bid.lihailin import jiangxi_zfcg_config
TEST_FILE = jiangxi_zfcg_config
from config.bid.huangtaiwu import shandong_sdzyang_config
TEST_FILE = shandong_sdzyang_config
def main():
    start(TEST_FILE)

if __name__ == '__main__':
    main()