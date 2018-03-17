# coding: utf-8

import HTMLParser

from lxml import etree
from lxml.html import clean
from pyquery import PyQuery as pq

from .exceptions import ParseException


class BaseParser(object):
    """解析器基类"""
    cleaner = clean.Cleaner()
    # 删除标签中<style>
    cleaner.style = True
    # 删除标签中所有属性
    cleaner.safe_attrs_only = True
    cleaner.safe_attrs = set()

    def __init__(self):
        self._result = None
        self._pat_text = None
        self._target = None

    def parse(self, html):
        """根据相应pattern解析html"""
        raise NotImplementedError

    def _clean_source(self, dirty_source):
        """清洗标签"""
        return self.cleaner.clean_html(dirty_source)

    @property
    def cleaned_source(self):
        return [self._clean_source(i) for i in self.source]

    @property
    def pattern(self):
        return self._pat_text

    @pattern.setter
    def pattern(self, value):
        self._pat_text = value

    @property
    def source(self):
        for item in self._result:
            yield item

    @property
    def text(self):
        return [pq(i).text() for i in self.source]

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def result(self):
        result = ''
        if not self.source:
            raise ParseException("No such pattern <%s>" % self._pat_text)
        else:
            if self._target == 'html':
                result = self.source
            elif self._target == 'clean_html':
                result = self.cleaned_source
            elif self._target == 'text':
                result = self.text
        if len(result) == 1:
            result = result[0]
        return result


class CSSParser(BaseParser):
    """css选择器解析器"""

    def parse(self, html):
        if not isinstance(html, unicode):
            html = unicode(html, 'utf-8')

        d = pq(html)
        result = d.find(self._pat_text)
        self._result = result
        return result

    @property
    def source(self):
        result = []
        for i in self._result:
            result.append(pq(i).outer_html())
        return result


class XPathParser(BaseParser):
    """xpath语法解析器"""

    html_parser = HTMLParser.HTMLParser()

    def parse(self, html):
        if not isinstance(html, unicode):
            html = unicode(html, 'utf-8')

        tree = etree.HTML(html)
        result = tree.xpath(self._pat_text)
        self._result = result
        return result

    @property
    def source(self):
        result = []
        for item in self._result:
            if isinstance(item, etree._Element):
                source = etree.tostring(item, with_tail=False)
                source = self.html_parser.unescape(source)
            else:
                source = item
            result.append(source)
        return result

def build_parser(pattern):
    pat_type, pat_text, target = parse_pattern(pattern)
    if pat_type == 'xpath':
        _parser = XPathParser()
    elif pat_type in ['css_selector', 'css']:
        _parser = CSSParser()
    else:
        # 其他解析模块未实现
        raise ValueError

    _parser.pattern = pat_text
    _parser.target = target

    return _parser

def parse_pattern(pattern):
    """
    解析pattern类型和文本
    :param pattern:
    :return:
    """
    pat_type = pattern['type']
    pat_text = pattern['pattern']
    target = pattern['target']
    # pat_type:
    #     - xpath  (默认)
    #     - class_name
    #     - css_selector
    #     - id
    #     - link_text
    #     - name
    #     - partial_link_text
    #     - tag_name
    return pat_type, pat_text, target


def _test_xpath():
    import requests
    page = requests.get('http://www.tjconstruct.cn/shchxt/tonggao.doc/epr_zbgg/2017/ZBGG3104[2017]0911.htm').content
    page = page.decode('gb2312')
    parser = XPathParser()
    parser.pattern = '//span[@class="title"]/text()'
    print parser.parse(page)
    print parser.source


def _test_css():
    import requests
    page = requests.get('http://www.tjconstruct.cn/shchxt/tonggao.doc/epr_zbgg/2017/ZBGG3104[2017]0911.htm').content
    page = page.decode('gb2312')
    d = pq(page)
    parser = CSSParser()
    parser.pattern = 'html'
    print parser.parse(page)
    print parser.source

def _test():
    _test_css()
    _test_xpath()


if __name__ == '__main__':
    _test()
