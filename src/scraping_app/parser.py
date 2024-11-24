import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('rabota', 'work')

# headers - для "обмана" серверов
headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def work(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='HH-React-Root')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-info--umZA61PpMY07JVJtomBA'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content = title
                    company = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-employer-text'})
                    jobs.append({'title': title.text, 'url': href, 'description': content.text, 'company': company.text,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div dose not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors

def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.rabota.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'r-serp'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-preview-card__top'})
                for div in div_list:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'})
                    company = div.find('span', attrs={'class': 'vacancy-preview-card__company-name'})
                    jobs.append({'title': title.text.strip(), 'url': domain + href, 'description': content.text, 'company': company.text.strip(),
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div dose not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors