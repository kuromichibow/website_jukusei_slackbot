import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')

def update_recent_article(news):
    with open('config.ini', 'r') as f:
        lines = f.readlines()
    with open('config.ini', 'w') as f:
        for line in lines:
            if re.match(r'(recent_article = )', line):
                f.write('recent_article = {}'.format(news))
                continue
            f.write(line)