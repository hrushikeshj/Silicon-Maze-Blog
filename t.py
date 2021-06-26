import requests
from bs4 import BeautifulSoup
from datetime import date
PULSE_URL = 'https://pulsenitk.in/'
IRIS_URL = 'https://blog.iris.nitk.ac.in/'
IEEE_URL = 'https://ieee.nitk.ac.in/blog'
def get_pulse(year = 2021):
    pulse = []
    pulse_page = requests.get(PULSE_URL + '2021')
    pulse_html = BeautifulSoup(pulse_page.text, 'html.parser')
    articles = pulse_html.find_all('article')
    for article in articles:
        data = {
            'title': None,
            'link': None,
            'img_url': None,
            'text': None
        }
        img_url = article.find('div', class_='post-thumbnail').get('style').replace(' ', '').replace('background-image:url(','')
        data['img_url'] = img_url[:(len(img_url)-1)]
        data['link'] = article.find('div', class_='post-thumbnail').a.get('href')
        text = articles[0].find('div', class_='post-meta-content').text
        data['text'] = ' '.join(text.split())
        pulse.append(data)
    print(pulse)
get_pulse()