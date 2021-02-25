import requests
from lxml import etree
import re
import os
from faker import Factory
import ast
import random


class MoJing_Spider(object):
    def __init__(self):
        user_agent = []
        for i in range(30):
            f = Factory.create()
            ua = "{{{0}}}".format("'User-Agent'" + ":" + "'{}'".format(f.user_agent()))
            headers = ast.literal_eval(ua)  # 使用 ast.literal_eval 将str转换为dict
            user_agent.append(headers)
        self.headers = random.choice(user_agent)
        self.start_url = 'https://www.520mojing.com/forum.php'  # 网站根地址
        self.main_folder = r'/Volumes/魔镜街拍图'  # 主路径
        # print(self.headers)

    # 解析主页
    def data_range(self):
        start_res = requests.get(url=self.start_url, headers=self.headers)
        start_sel = etree.HTML(start_res.content.decode())
        return start_sel

    # 获取网址列表
    def get_author_url(self, start_sel):
        main_url_list = start_sel.xpath('//dt[@style="font-size:15px; margin-top:6px"]/a/@href')
        return main_url_list

    # 获取分区网址
    def create_url(self, author_url):
        author_res = requests.get(url=author_url, headers=self.headers)
        author_sel = etree.HTML(author_res.content.decode())
        try:
            id = re.findall(r'https://www.520mojing.com/forum-(.*?)-1.html', author_url)[0]
            len_page = author_sel.xpath('//span[@id="fd_page_top"]/div/label/span/text()')[0].replace('/ ', '').replace(
                ' 页', '')
            len_page = int(len_page)
            name = author_sel.xpath('//div[@class="bm_h cl"]/h1/a/text()')[0]
            print(f'=================正在保存{name}图片，共{len_page}页=================')
            return name, id, len_page
        except IndexError:
            pass

    # 获取每页图片链接
    def get_pciturelinks(self, page_url):
        picture_res = requests.get(url=page_url, headers=self.headers)
        picture_sel = etree.HTML(picture_res.content.decode())
        try:
            pciture_links = picture_sel.xpath('//div[@class="c cl"]/a/img/@data-src')
            return pciture_links
        except IndexError:
            pass

    # 保存图片
    def save_picture(self, name, link, num):
        try:
            # 创建多层文件夹
            folder = self.main_folder + '/' + name + '/' + str(num) + '/'
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(folder + link.split('/')[-2] + os.path.splitext(link)[-1], 'wb') as f:
                image = requests.get(url=link, headers=self.headers).content
                f.write(image)
        except:
            print('保存失败')

    def run(self):
        start_sel = self.data_range()
        main_url_list = self.get_author_url(start_sel)
        for author_url in main_url_list:
            name, id, len_page = self.create_url(author_url)
            for num in range(1, len_page + 1):
                page_url = f'https://www.520mojing.com/forum-{id}-{num}.html'
                pciture_links = self.get_pciturelinks(page_url)
                for link in pciture_links:
                    # print(link)
                    self.save_picture(name, link, num)


if __name__ == '__main__':
    MoJing = MoJing_Spider()  # 实例化对象
    MoJing.run()