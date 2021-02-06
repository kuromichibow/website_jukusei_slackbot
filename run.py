#!/usr/bin/python3

from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import slackweb
import ssl
from datetime import datetime ,timedelta
import os
from dotenv import load_dotenv
load_dotenv()

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

today = datetime.today()
yesterday = today - timedelta(days=1)
formatted_yesterday = datetime.strftime(yesterday, '%Y/%m/%d')

top_articles_yesterday = [s for s in top_articles if formatted_yesterday in s]

# print(top_articles_yesterday)

if top_articles_yesterday == []:
    top_articles_yesterday.append("更新記事はありません")

if __name__ == "__main__":
    token = os.environ['SLACKBOT_API_TOKEN']
    slack = slackweb.Slack(url=token)
    for feed in top_articles_yesterday:
        slack.notify(text=feed)