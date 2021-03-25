import os
import scrapy
import hashlib
import requests
import datefinder
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

es = Elasticsearch(os.getenv("ELASTIC_SEARCH_HOST"), http_auth=(os.getenv("ELASTIC_NAME" ), os.getenv("ELASTIC_PASSWORD")))

class UdndataSpider(scrapy.Spider):
    name = 'udndata'
    allowed_domains = ['udndata.com']
    start_urls = [
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=1&SearchString=%A4%6A%BE%C7%A6%DB%AA%76%2B%A4%E9%B4%C1%3E%3D19510101%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=0&kind=2&showSearchString=',
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=11&SearchString=%A4%6A%BE%C7%A6%DB%AA%76%2B%A4%E9%B4%C1%3E%3D19510101%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=0&kind=2',
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=1&SearchString=%A4%6A%BE%C7%A6%DB%A5%44%2B%A4%E9%B4%C1%3E%3D19510301%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=1&kind=2&showSearchString=',
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=11&SearchString=%A4%6A%BE%C7%A6%DB%A5%44%2B%A4%E9%B4%C1%3E%3D19510301%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=1&kind=2',
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=21&SearchString=%A4%6A%BE%C7%A6%DB%A5%44%2B%A4%E9%B4%C1%3E%3D19510301%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=1&kind=2',
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=1&SearchString=%BE%C7%B3%4E%A6%DB%A5%D1%2B%A4%E9%B4%C1%3E%3D19510301%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=1&kind=2&showSearchString=',
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=11&SearchString=%BE%C7%B3%4E%A6%DB%A5%D1%2B%A4%E9%B4%C1%3E%3D19510301%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=1&kind=2',
        'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=21&SearchString=%BE%C7%B3%4E%A6%DB%A5%D1%2B%A4%E9%B4%C1%3E%3D19510301%2B%A4%E9%B4%C1%3C%3D20210324&sharepage=50&select=1&kind=2'
    ]

    headers = {
        'Content-Type': 'application/json',
        'cookie': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9; JSESSIONID=25E8E49BE991755666530B194F5F415E-n1',
        'cookie': 'JSESSIONID=42651B337455712FA7BFF7DDF4A3F695-n1; _ga=GA1.2.743700092.1616483827; _gid=GA1.2.483597604.1616483827; _gat=1; _gat_udndata=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.http.Request(url, headers=self.headers ,callback=self.parse)

    def page(self, response):
        for article in response.css('a::attr(href)').re(r'Story.*'):
            if article is not None:
                article = response.urljoin(str(article))
                yield scrapy.http.Request(article, headers=self.headers ,callback=self.article)

    def parse(self, response):
        pages = response.css('a::attr(href)').re(r'Searchdec.*')

        for article in response.css('a::attr(href)').re(r'Story.*'):
            if article is not None:
                article = response.urljoin(str(article))
                yield scrapy.http.Request(article, headers=self.headers ,callback=self.article)

        for page in pages:
            if page is not None:
                page = response.urljoin(str(page))
                yield scrapy.http.Request(page, headers=self.headers ,callback=self.page)

    def article(self, response):
        title = response.css('h1::text').get()
        nfrom = '聯合時報'
        matches = datefinder.find_dates(response.css('.story-source::text').get())
        for match in matches:
            date = match.strftime("%Y-%m-%d %H:%M:%S")

        content = ''
        for p in response.css('article > p::text').getall():
            content += p

        yield {
            'title': title,
            'from': nfrom,
            'date': date,
            'content': content,
        }

        id = title+nfrom+str(date)
        id = hashlib.md5(id.encode()).hexdigest()

        documents = [
            {
                "index": {
                    "_id" : id
                }
            }, {
                "title": title,
                "from": nfrom,
                "content": content,
                "date": date,
            }
        ]

        es.bulk(body=documents, index='news')
