from flask import Flask
from flask import render_template
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import calendar

url = 'https://assets.digitalocean.com/articles/eng_python/beautiful-soup/mockturtle.html'
PULSE_URL = 'https://pulsenitk.in/'
IRIS_URL = 'https://blog.iris.nitk.ac.in/'
IEEE_BLOG_URL = 'https://ieee.nitk.ac.in/blog'
IEEE_URL = 'https://ieee.nitk.ac.in'
todays_date = date.today()

app = Flask(__name__)

@app.route("/")
def index():
    pulse = get_pulse_latest()
    iris = get_iris_latest()
    ieee = get_ieee_latest()
    if len(pulse) < 6:
        pulse += get_pulse_latest(todays_date.year - 1)
    if len(iris) < 6:
        iris += get_iris_latest(todays_date.year - 1)
    carousel = [pulse.pop(0), iris.pop(0), ieee.pop(0)]
    return render_template('index.html', carousel = carousel, ieee = ieee, pulse = pulse, iris = iris)

@app.route("/posts")
@app.route("/posts/<year>/<month>")
def posts(year=todays_date.year , month=todays_date.month):
    print(year, month)
    pulse = pulse_by_month(year=year, month = month)
    iris = iris_by_month(year=year, month = month)
    ieee = ieee_by_month(year=int(year), month = int(month))
    return render_template(
        'month.html', ieee = ieee, pulse = pulse, iris = iris,
        pulse_url = PULSE_URL + str(year) + '/' + str(month),
        iris_url = IRIS_URL + str(year) + '/' + str(month),
        month = calendar.month_name[int(month)] + str(year)
    )

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
def get_pulse_latest(year = todays_date.year):
    pulse = []
    pulse_page = requests.get(PULSE_URL + str(year) )
    pulse_html = BeautifulSoup(pulse_page.text, 'html.parser')
    articles = pulse_html.find_all('article')
    for article in articles:
        data = pulse_article_data(article)
        pulse.append(data)
    return pulse

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

def get_iris_latest(year = todays_date.year):
    iris = []
    iris_page = requests.get(IRIS_URL + str(year) )
    iris_html = BeautifulSoup(iris_page.text, 'html.parser')
    articles = iris_html.find_all('article')
    
    for article in articles:
        data = iris_article_data(article)
        iris.append(data)
    
    return iris

def ieee_img(link):
    page = requests.get(link)
    page_html = BeautifulSoup(page.text, 'html.parser')
    img = page_html.find('section', class_='post').find('img')
    if img != None:
        return IEEE_URL + img.get('src')
    return 'static/noimg.png'

def ieee_article_data(article, img):
    data = {
        'title': None,
        'link': None,
        'img_url': None,
        'info': None,
        'text': None
    }
    data['title'] = article.h2.text.strip()
    data['link'] = 'https://ieee.nitk.ac.in' + article.h2.a.get('href')
    if img:
        data['img_url'] = ieee_img(data['link'])
    info = article.find('p', class_='author-wrap').text.strip().replace('\n', '')
    data['info'] = ' '.join(info.split())
    data['text'] = article.find_all('p')[-1].text.strip()[:100] + '...'
    return data

def get_ieee_latest(img = True):
    ieee = []
    ieee_page = requests.get(IEEE_BLOG_URL )
    ieee_html = BeautifulSoup(ieee_page.text, 'html.parser')
    articles = ieee_html.find_all('article')
    for article in articles:
        data = ieee_article_data(article, img)
        ieee.append(data)
    return ieee

#by month
def iris_by_month(year, month):
    iris = []
    iris_page = requests.get(IRIS_URL + str(year) + '/' + str(month))
    if iris_page.status_code != 200:
        return []
    
    iris_html = BeautifulSoup(iris_page.text, 'html.parser')
    articles = iris_html.find_all('article')
    for article in articles:
        data = iris_article_data(article)
        iris.append(data)
    
    return iris

def pulse_by_month(year, month):
    pulse = []
    pulse_page = requests.get(PULSE_URL + str(year) + '/' + str(month))
    if pulse_page.status_code != 200:
        return []
    
    pulse_html = BeautifulSoup(pulse_page.text, 'html.parser')
    articles = pulse_html.find_all('article')
    for article in articles:
        data = pulse_article_data(article)
        pulse.append(data)
    return pulse

def ieee_by_month(year, month):
    ieee = []
    page = 1
    ieee_page = requests.get(IEEE_BLOG_URL )
    
    while True:
        if ieee_page.status_code != 200:
            return ieee
        ieee_html = BeautifulSoup(ieee_page.text, 'html.parser')
        articles = ieee_html.find_all('article')
        for article in articles:
            data = ieee_article_data(article, img=False)
            datestr = data['info'].split('|')[-1].strip()
            try:
                date = datetime.strptime(datestr, '%B %d, %Y')
                if date.year < year:
                    return ieee
                if date.month == month and date.year == year:
                    data['img_url'] = ieee_img(data['link'])
                    ieee.append(data)
            except:
                print("ieee date err")
            
        page += 1
        ieee_page = requests.get(IEEE_BLOG_URL + '/page' + str(page))
    
    return ieee
#print(ieee_by_month(2021, 1))