import requests
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequsetException:
        return None

def parse_one_page(html):
    pattern = re.compile('board-index-.*?">(\d+)</i>.*?name"><a.*?>(.*?)</a></p>.*?releasetime">(.*?)</p>.*?"score">.*?>(.*?)</i>.*?fraction">(\d+)</i>',re.S)
    items = re.findall(pattern,html)
    #print(items)
    for item in items:
        yield{
                "index":item[0],
                "name":item[1],
                "time":item[2].strip()[5:],
                "score":item[3]+item[4]
                }

def write_to_file(content):
    with open("result.txt",'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+"\n")
        f.close


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        #print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    #pool = Pool();
    #pool.map(main,[i*10 for i in range(10)])
