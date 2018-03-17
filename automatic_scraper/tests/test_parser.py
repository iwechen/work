# coding: utf-8

import unittest

import sys
sys.path.append('..')

from util import parser

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


class TestParser(unittest.TestCase):
    def test_build_parser_xpath(self):
        pattern = {'pattern': '//a', 'type': 'xpath', 'target': 'html'}
        _parser = parser.build_parser(pattern)
        self.assertIsInstance(_parser, parser.XPathParser)

    def test_build_parser_css(self):
        pattern = {'pattern': 'a', 'type': 'css', 'target': 'html'}
        _parser = parser.build_parser(pattern)
        self.assertIsInstance(_parser, parser.CSSParser)

    def test_xpath_html(self):
        pattern = {'pattern': '//p[@class="title"]', 'type': 'xpath', 'target': 'html'}
        _parser = parser.build_parser(pattern)
        _parser.parse(html_doc)
        self.assertEqual(_parser.result, '<p class="title"><b>The Dormouse\'s story</b></p>')

    def test_xpath_text(self):
        pattern = {'pattern': '//p[@class="title"]', 'type': 'xpath', 'target': 'text'}
        _parser = parser.build_parser(pattern)
        _parser.parse(html_doc)
        self.assertEqual(_parser.result, 'The Dormouse\'s story')

    def test_css_html(self):
        pattern = {'pattern': 'p.title', 'type': 'css', 'target': 'html'}
        _parser = parser.build_parser(pattern)
        _parser.parse(html_doc)
        self.assertEqual(_parser.result, '<p class="title"><b>The Dormouse\'s story</b></p>')

    def test_css_text(self):
        pattern = {'pattern': 'p.title', 'type': 'css', 'target': 'text'}
        _parser = parser.build_parser(pattern)
        _parser.parse(html_doc)
        self.assertEqual(_parser.result, 'The Dormouse\'s story')

    def test_multi_xpath(self):
        pattern = {'pattern': '//a[@class="sister"]', 'type': 'xpath', 'target': 'html'}
        _parser = parser.build_parser(pattern)
        _parser.parse(html_doc)
        self.assertEqual(len(_parser.result), 3)

    def test_multi_css(self):
        pattern = {'pattern': 'a.sister', 'type': 'css', 'target': 'html'}
        _parser = parser.build_parser(pattern)
        _parser.parse(html_doc)
        self.assertEqual(len(_parser.result), 3)


if __name__ == '__main__':
    unittest.main()