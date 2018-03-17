# coding: utf-8
class BaseDownloaderException(Exception):
    """Downloader无法解决的网络错误"""


class SeleniumException(Exception):
    """Selenium无法打开"""

class ParseException(Exception):
    """无法找到元素"""

class TaskFinishSignal(Exception):
    """到达抓取时间节点，完成任务"""