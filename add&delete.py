from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

name_db = {}


def get_name_by_url(website_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    # scrape raw site
    website = requests.get(website_url, headers=headers, timeout=10)
    # scrape site
    soup = BeautifulSoup(website.content, "html.parser")
    article = 0
    name_db[article] = soup.find("span", {"class": "b-crumbs__current"}).get_text()
    return name_db


@app.route('/add', methods=['POST'])
def add_tracking():
    website_url = request.json['url']
    new_job = scheduler.add_job(get_name_by_url, 'interval', args=[website_url], seconds=5, id=website_url)
    return website_url


@app.route('/delete', methods=['DELETE'])
def delete_tracking():
    website_url = request.json['url']
    current_job = scheduler.get_job(website_url)
    scheduler.remove_job(website_url)
    return current_job


if __name__ == '__main__':
    app.run(port=5000)
