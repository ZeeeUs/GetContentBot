import random

from bs4 import BeautifulSoup
import requests

HOST = 'https://www.instagram.com/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html, content_type):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find('meta', property=f'og:{content_type}')["content"]
    return items


def download(url, ext):
    name = f'dwnld{random.randint(1, 1000)}.{ext}'
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)
    return name


def start(content_type, ext, url):
    html = get_html(url)
    content_url = get_content(html, content_type)
    name = download(content_url, ext)
    return name
