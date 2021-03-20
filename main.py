import requests
from lxml import html
from datetime import datetime
from pprint import pprint


LINKS = {'mail': 'https://news.mail.ru/',
         'lenta': 'https://lenta.ru/',
         'yandex': 'https://yandex.ru/'
         }

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}


class Parser:
    def __init__(self, links_dict, headers):
        self.links_dict = links_dict
        self.headers = headers
        self.result_news = []

    def router(self):
        for name, value in self.links_dict.items():
            getattr(self, f'parse_{name}', None)(value)
        pprint(self.result_news)

    def parse_mail(self, url):
        response = requests.get(url, headers=HEADERS)
        dom = html.fromstring(response.text)
        items = dom.xpath(
            '//a[contains(@class,"photo photo_full photo_scale")] | //a[contains(@class,"photo photo_small photo_scale photo_full js-topnews__item")] ')
        i = 0
        for item in items:
            news = {}
            name = item.xpath('.//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text()')[0].replace('\xa0', ' ')
            url_new = item.xpath('//a[contains(@class, "js-topnews__item")]/@href')[i]
            news['name'] = name
            news['url'] = url_new
            source, date = self.get_news_data(url_new)
            news['source'] = source
            news['date'] = date
            self.result_news.append(news)
            i += 1

    def get_news_data(self, link):
        response = requests.get(link, headers=HEADERS)
        dom = html.fromstring(response.text)
        items = dom.xpath('//div[contains(@class,"article js-article")]')
        for item in items:
            source = item.xpath('.//span[@ class ="link__text"]/text()')[0]
            date = item.xpath('//span[@ class ="note__text breadcrumbs__text js-ago"]/@ datetime')[0]
            return source, date

    def parse_lenta(self, url):
        response = requests.get(url, headers=HEADERS)
        dom = html.fromstring(response.text)
        items = dom.xpath('//div[@class="b-yellow-box__wrap"]/div[@class="item"]')
        source = "lenta.ru"
        for item in items:
            news = {}
            name = item.xpath('.//a/text()')[0].replace('\xa0',' ')
            url_new = item.xpath('.//a/@href')[0]
            day_list = url_new.replace('/news/', '').split('/')
            day = day_list.pop(0) + '.' + day_list.pop(0) + '.' + day_list.pop(0)
            news['name'] = name
            news['link'] = url + url_new
            news['source'] = source
            news['date'] = day
            self.result_news.append(news)

    def parse_yandex(self, url):
        response = requests.get(url, headers=HEADERS)
        dom = html.fromstring(response.text)
        items = dom.xpath('//ol/li')
        date = datetime.today().strftime("%d-%m-%Y")
        for item in items:
            news = {}
            source = item.xpath('.//object/@title')[0]
            name = item.xpath('.//span[contains(@class ,"news__item-content")]/text()')[0]
            url_new = item.xpath('.//a/@href')[0]
            news['source'] = source
            news['link'] = url_new
            news['name'] = name
            news['date'] = date
            self.result_news.append(news)


parser = Parser(LINKS, HEADERS)

parser.router()
