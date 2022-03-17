from celery import Celery
from backend.parser import get_product_html, find_name, get_price

app = Celery('get_information', broker='redis://localhost:6379', backend='redis://localhost:6379')


@app.task()
def get_info_about_product(url):
    soup = get_product_html(url)
    name = find_name(soup)
    full_price = get_price(soup)
    price_on_sale = get_price(soup)
    price_with_card = get_price(soup)
    return [name, full_price, price_with_card, price_on_sale]
