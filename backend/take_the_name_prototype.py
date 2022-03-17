import requests
from flask import Flask, request
from bs4 import BeautifulSoup


app = Flask(__name__)

name_db = {}


@app.route('/', methods=['POST'])
def index():
    # scrape raw site
    website_url = request.json['url']
    website = requests.get(website_url)
    # scrape site
    soup = BeautifulSoup(website.content, "html.parser")
    article = 0
    name_db[article] = soup.find("span", {"class": "b-crumbs__current"}).get_text()
    return name_db


if __name__ == '__main__':
    app.run(port=5000)
