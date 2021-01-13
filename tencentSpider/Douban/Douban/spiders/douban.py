import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['maoyan.com']

    baseURL = "https://www.douban.com/group/463778/?ref=sidebar"
    # offset = 1
    start_urls = [baseURL]

    def parse(self, response):
        content = response.xpath('//*[@id="group-topics"]')
        print(content)



