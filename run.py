#!/usr/bin/python3

from urllib import request
from bs4 import BeautifulSoup
from config import config, update_recent_article
from urllib.parse import urljoin
import slackweb
import ssl
import os

url = "https://www.keio.ac.jp/ja/news/2021/"
html = request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

infoItems = soup.find('ul', class_="infoItems")
infoItem = infoItems.find_all('li', class_="infoItem")

top_articles = []
for item in infoItem:
    date = item.select('span.infoDate')[0].text
    title = item.select('span.infoText')[0].text
    relative_link = item.select('a.infoLink')[0].get("href")
    link = urljoin("https://www.keio.ac.jp/", relative_link)
    top_articles.append(f'{date} | {title} | {link}')

# print(top_articles)

recent_article = config['web_info']['recent_article']

# print(recent_article)

article_list = []
update_start = False

for news in reversed(top_articles):
    if update_start:
        article_list.append(news)
        continue
    if news == recent_article:
        update_start = True

update_recent_article(news)

if article_list == []:
    article_list.append("更新記事はありません")

if __name__ == "__main__":
    token = os.environ['SLACKBOT_API_TOKEN']
    slack = slackweb.Slack(url=token)
    for feed in article_list:
        slack.notify(text=feed)