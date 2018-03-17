# coding: utf-8

import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.INFO)
logging.getLogger("chardet").setLevel(logging.INFO)

log_level = logging.DEBUG

root_logger = logging.getLogger()
logger = logging.getLogger(__name__)
root_logger.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d -%(filename)s:%(lineno)s- %(levelname)s: %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S')

fh = logging.FileHandler('run.log')
fh.setLevel(log_level)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(log_level)
ch.setFormatter(formatter)

root_logger.addHandler(ch)
root_logger.addHandler(fh)
