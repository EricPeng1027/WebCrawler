import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<div\sclass="list_num.*?>(\d+).</div>.*?'                    #rank number
                         + 'class="pic"><a\shref="(.*?)".*?'                           #book link
                         + 'class="name">.*?title=.*?>(.*?)</a>.*?'                    #book name
                         + 'class="publisher_info">.*?title="(.*?)".*?'                #author
                         + 'class="publisher_info"><span>(.*?)</span>.*?'              #publish date
                         + 'target="_blank">(.*?)</a>.*?</li>', re.S)                  #publishment
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'link': item[1],
            'title': item[2],
            'author': item[3],
            'date': item[4],
            'publishment': item[5]
        }
    #print(items)

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main():
    url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-24hours-0-0-1-1'
    html = get_one_page(url)
    rank_types = ["bestsellers", "newhotsales", "childrensbooks", "surplusbooks", "fivestars", "soaringsales", "ebooks",
                 "enewhotbooks"]

    for rank_type in rank_types:
        for i in range(25):
            url = 'http://bang.dangdang.com/books/' + rank_type + '/01.00.00.00.00.00-24hours-0-0-1-' + str(i + 1)
            html = get_one_page(url)
            for item in parse_one_page(html):
                print(item)
                write_to_file(item)

    #print(html)
    #parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    main()