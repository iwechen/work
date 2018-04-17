import logging
from .clean import BihuClean

root_logger = logging.getLogger(__name__)
root_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')


fh = logging.FileHandler('bihu.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setFormatter(formatter)

root_logger.addHandler(fh)
root_logger.addHandler(ch)



