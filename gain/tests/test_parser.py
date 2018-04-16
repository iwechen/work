
# from gain import Css, Item, Parser, Xpath


# def test_parse():
#     html = '<title class="username">tom</title><div class="karma">15</div>'

#     class User(Item):
#         username = Xpath('//title')
#         karma = Css('.karma')

#     parser = Parser(html, User)

#     user = parser.parse_item(html)
#     assert user.results == {
#         'username': 'tom',
#         'karma': '15'
#     }


# def test_parse_urls():
#     html = ('<a href="item?id=14447885">64comments</a>'
#             '<a href="item?id=14447886">64comments</a>')

#     class User(Item):
#         username = Xpath('//title')
#         karma = Css('.karma')

#     parser = Parser('item\?id=\d+', User)
#     parser.parse_urls(html, 'https://blog.scrapinghub.com')
#     assert parser.pre_parse_urls.qsize() == 2




from gain import Css, Item, Parser, Spider
import aiofiles

class Post(Item):
    title = Css('.entry-title')
    print(title)
    content = Css('.entry-content')
    print(content)

    async def save(self):
        async with aiofiles.open('scrapinghub.txt', 'a+') as f:
            await f.write(self.results['title'])


class MySpider(Spider):
    concurrency = 5
    headers = {'User-Agent': 'Google Spider'}
    start_url = 'https://blog.scrapinghub.com/'
    parsers = [Parser('https://blog.scrapinghub.com/page/\d+/'),
               Parser('https://blog.scrapinghub.com/\d{4}/\d{2}/\d{2}/[a-z0-9\-]+/', Post)]


MySpider. run()

