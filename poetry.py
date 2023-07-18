import requests
from bs4 import BeautifulSoup
import json
import time


def crawl_tang_poems():
    # 开始时间
    start_time = time.time()

    # 发送http请求
    url = "https://so.gushiwen.cn/gushi/tangshi.aspx"
    response = requests.get(url)

    # 解析html
    soup = BeautifulSoup(response.text, "html.parser")
    poem_list = []

    # 获取诗词列表
    div_list = soup.find_all('div', class_="typecont")

    id = 1
    for div in div_list:
        source_list = div.find_all('span')
        for source in source_list:
            # 获取诗词标题和作者
            string_source = source.text.strip()
            try:
                temp = string_source.split('(')
                title = temp[0]
                author = temp[1][:-1]
            except:
                title = string_source
                author = '佚名'

            # 获取诗词内容
            url_head = 'https://so.gushiwen.cn'
            content_url = url_head + str(source).split(' ')[1][6:-1]
            content_response = requests.get(content_url)
            content_soup = BeautifulSoup(content_response.text, 'html.parser')
            content_line = content_soup.find_all('meta')[3]
            content = content_line.get("content")

            poem = {"id": id, "title": title, "content": content, "author": author}
            print(poem)
            poem_list.append(poem)

            id += 1

    # 计算耗时
    end_time = time.time()
    print(f'爬取总耗时为: {end_time - start_time} s')
    print(f'每秒爬取的个数为: {int(id / (end_time - start_time))} 首')

    # 保存
    with open("tang_poems.json", 'w', encoding='UTF-8') as f:
        json.dump(poem_list, f, ensure_ascii=False, indent=4)  # 最后一个参数用于更好的存储


if __name__ == '__main__':
    crawl_tang_poems()
