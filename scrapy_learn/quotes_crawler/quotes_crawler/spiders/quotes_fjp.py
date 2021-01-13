import scrapy


class QuotesFjpSpider(scrapy.Spider):
    name = 'quotes_fjp'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
