# coding=utf-8

import logging
import time
import traceback

import requests
from requests import Session as _Session

from .exceptions import BaseDownloaderException

MAX_RETRIES = 30  # 网络错误尝试次数
TIME_OUT = 30  # 超时时间

MAX_PROXY_RETRIES = 20  # 使用代理的尝试次数

logger = logging.getLogger(__name__)

DOWNLOADER_CUR_URL = None


class History(object):
    _last_url = None
    _last_response = None

class Session(_Session):

    def __init__(self):
        super(Session, self).__init__()

    def request(self, method, url, **kwargs):
        History._last_url = url
        if 'timeout' not in kwargs:
            kwargs['timeout'] = TIME_OUT
        for i in range(MAX_RETRIES):
            try:
                if i >= 10:
                    time.sleep(60)
                if i > (MAX_RETRIES / 2):
                    logger.warning("Retry %s times: %s", i, url)

                response = super(Session, self).request(method, url, **kwargs)
                History._last_url = response.request.url
                History._last_response = response
                return response
            except requests.exceptions.HTTPError as e:
                pass
            except requests.exceptions.Timeout as e:
                pass
            except requests.exceptions.ProxyError as e:
                pass
            except Exception as e:
                pass
        else:
            logger.error(u"网络原因 访问 %s 失败", url)
            raise BaseDownloaderException


def request(method, url, **kwargs):

    session = Session()
    response = session.request(method=method, url=url, **kwargs)
    # By explicitly closing the session, we avoid leaving sockets open which
    # can trigger a ResourceWarning in some cases, and look like a memory leak
    # in others.
    session.close()
    return response


def get(url, **kwargs):
    """Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    kwargs.setdefault('allow_redirects', True)
    return request('get', url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    """Sends a POST request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request('post', url, data=data, json=json, **kwargs)

# requests.sessions.Session = requests.Session = Session

def main():
    s = Session()
    get('http://httpbin.org/get', params={'aa', 'bb'})
    print History._last_url
    print History._last_response.request.headers

    url = History._last_url
    request_body = History._last_response.request.body
    response_content = History._last_response.content
    err_msg = 'url:\n{}\n\n=================\n'
    err_msg += 'err_msg:\n{}\n=================\n'
    err_msg += 'request_data:\n{}\n=================\n'
    err_msg += 'content:\n{}'
    err_msg = err_msg.format(url, traceback.format_exc(), request_body, response_content)

if __name__ == '__main__':
    main()
