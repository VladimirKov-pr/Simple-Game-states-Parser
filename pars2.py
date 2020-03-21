import requests
from bs4 import BeautifulSoup as BS


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BS(html, 'lxml')

def main():


if __name__ == '__main__':
    main()
