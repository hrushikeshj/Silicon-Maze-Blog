import requests
from bs4 import BeautifulSoup
from datetime import date
PULSE_URL = 'https://pulsenitk.in/'
IRIS_URL = 'https://blog.iris.nitk.ac.in/'
IEEE_BLOG_URL = 'https://ieee.nitk.ac.in/blog'
IEEE_URL = 'https://ieee.nitk.ac.in'
todays_date = date.today()

def ieee_img(link):
    page = requests.get(link)
    page_html = BeautifulSoup(page.text, 'html.parser')
    img = page_html.find('section', class_='post').find('img')
    if img != None:
        return IEEE_URL + img.get('src')
    return 'static/noimg.png'

def ieee_article_data(article):
    data = {
        'title': None,
        'link': None,
        'img_url': None,
        'info': None,
        'text': None
    }
    data['title'] = article.h2.text.strip()
    data['link'] = 'https://ieee.nitk.ac.in' + article.h2.a.get('href')
    data['img_url'] = ieee_img(data['link'])
    info = article.find('p', class_='author-wrap').text.strip().replace('\n', '')
    data['info'] = ' '.join(info.split())
    data['text'] = article.find_all('p')[-1].text.strip()[:100] + '...'
    return data

def get_ieee_latest():
    ieee = []
    ieee_page = requests.get(IEEE_BLOG_URL )
    ieee_html = BeautifulSoup(ieee_page.text, 'html.parser')
    articles = ieee_html.find_all('article')
    for article in articles:
        data = ieee_article_data(article)
        ieee.append(data)
    return ieee

print(get_ieee_latest())

def iris_article_data(article):
    data = {
        'title': None,
        'link': None,
        'img_url': None,
        'info': None,
        'text': None
    }
    data['title'] = article.find('h2', class_='entry-title').text.strip()
    link = article.find('a', class_='entry-thumbnail')
    if link != None:
        data['link'] = link.get('href')
        data['img_url'] = article.find('a', class_='entry-thumbnail').img.get('src')
    data['info'] = article.find('div', class_='entry-meta').text.strip()
    data['text'] = article.find('div', class_='entry-content').text.strip()[:80] + '....'
    return data

def get_iris_latest():
    iris = []
    iris_page = requests.get(IRIS_URL + str(todays_date.year) )
    iris_html = BeautifulSoup(iris_page.text, 'html.parser')
    articles = iris_html.find_all('article')
    
    for article in articles:
        data = iris_article_data(article)
        iris.append(data)
    
    return iris

 


def pulse_article_data(article):
    data = {
        'title': None,
        'link': None,
        'img_url': None,
        'info': None,
        'text': None
    }
    data['title'] = article.find('h2').text.strip()
    img_url = article.find('div', class_='post-thumbnail').get('style').replace(' ', '').replace('background-image:url(','')
    data['img_url'] = img_url[:-2]
    data['link'] = article.find('div', class_='post-thumbnail').a.get('href')
    text = article.find('div', class_='post-meta-content').text
    data['info'] = ' '.join(text.split())
    return data

#returns 10 latest 
def get_pulse_latest():
    pulse = []
    pulse_page = requests.get(PULSE_URL + str(todays_date.year) )
    pulse_html = BeautifulSoup(pulse_page.text, 'html.parser')
    articles = pulse_html.find_all('article')
    for article in articles:
        data = pulse_article_data(article)
        pulse.append(data)
    print(pulse)
    return pulse

