import requests
import bs4
import lxml
import re
import json
from fake_headers import Headers

keywords = ['Привет', 'разработчик','проектировать','компьютер']

response = requests.get('https://habr.com/ru/articles/', headers=Headers(browser='chrome', os='mac').generate())
soup = bs4.BeautifulSoup(response.text, features='lxml')
article_list = soup.select('div', class_='tm-articles-list__item')

# время
time = re.findall(r'<time datetime(.*?)</time>', response.text)
time_=[]

for t in time:
    match = re.search(r'title="([^"]*)"',t)
    if match:
        title_value = match.group(1)
        print(title_value)
        time_.append(title_value)


link_indeces =[]
links =[]
counter_l  = -1
global_indeces =[]
parse=[]

headers = []
article_list = set(article_list)
#article_list = list(article_list)
# ссылки статей и текст превью
preview_list = []

for article in article_list:
    if  article.find('a','tm-title__link') is not None:
        counter_l += 1
        link_indeces.append(counter_l)
        link = 'https://habr.com/ru/articles/'+  article.find('a','tm-title__link')['href']

        links.append(link)
        head = article.select('span')[2].text
        head_flag = False

        if head!='Новости ' and head!='Статьи ':
            head_flag = True
            headers.append(head)

        if article.find('div', 'article-formatted-body article-formatted-body article-formatted-body_version-2') is not None:
            preview = article.find('div', 'article-formatted-body article-formatted-body article-formatted-body_version-2').text
            print(preview)
            preview_list.append(preview)


length = min(len(headers), len(time_), len(preview_list))

for i in range(length):
    for kw in keywords:
        if kw in preview_list[i]:
            global_indeces.append(i)
            parse.append({
                    'title': headers[i],
                    'link': links[i],
                    'time': time_[i]
                })


with open("article.json" ,'w',  encoding="utf-8") as f:
    f.write(json.dumps(parse, ensure_ascii=False,indent=4))




