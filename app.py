from flask import Flask
from flask import render_template
import requests
from bs4 import BeautifulSoup
from datetime import date

url = 'https://assets.digitalocean.com/articles/eng_python/beautiful-soup/mockturtle.html'
PULSE_URL = 'https://pulsenitk.in/'
IRIS_URL = 'https://blog.iris.nitk.ac.in/'
IEEE_URL = 'https://ieee.nitk.ac.in/blog'

app = Flask(__name__)

@app.route("/")
def index():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return render_template('index.html', x=soup.prettify())

@app.route("/<f>")
def f(f):
    return f"<p>Hello, World! {f}</p>"

@app.route("/hi/<f>")
def hi(f):
    return render_template('hi.html', name=f)

def get_pulse(year = 2021):
    pulse_page = requests.get(PULSE_URL + '2021')
    pulse_html = BeautifulSoup(pulse_page.text, 'html.parser')
    article = pulse_html.find_all('article')
    print(article[0].div)
