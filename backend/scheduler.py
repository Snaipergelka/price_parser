# This function installs the scheduler that makes parsing intervally
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import requests


def get_product_html():
    website_url = 'https://sephora.ru/make-up/lips/shiny/clarins-natural-lip-perfector-prodgac/#store_326868'
    # scrape raw site
    website = requests.get(website_url)
    # scrape site
    soup = BeautifulSoup(website.content, "html.parser")

    name_of_good = soup.find("span", {"class": "b-crumbs__current"}).get_text()
    print(name_of_good)


scheduler = BackgroundScheduler()
job = scheduler.add_job(get_product_html, 'interval', seconds=10)


scheduler.start()


while True:
    1 + 1