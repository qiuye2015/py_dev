import scrapy

from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    # start_urls = ['http://tencent.com/']
    baseURL ="https://careers.tencent.com/search.html?query=ot_40001001&index="
    offset = 1
    start_urls = [baseURL+str(offset)]


    def parse(self, response):
        print("++++++++",response.text)
        node_list = response.xpath("/html/body/div[1]/div[4]/div[3]/div[2]/div[3]/div")

        print("-----------------",len(node_list))
        for node  in node_list:
            item = TencentItem()
            item["positionName"] = node.xpath("./div[2]/a/h4")
            # .extract()[0].encode("utf-8")
            print(" --------------",node)
            # print(item["positionName"])
            yield item

        self.offset += 1
        if self.offset<3:
            url = self.baseURL+ str(self.offset)
            yield scrapy.Request(url, callback=self.parse)
