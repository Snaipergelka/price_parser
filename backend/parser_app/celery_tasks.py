import os
import time
from celery import Celery
from .api_routers.routers_config import connecting_to_db
from backend.parser_app.parser import (get_product_html,
                                       find_name,
                                       get_price,
                                       check_availability,
                                       check_for_alternatives,
                                       get_prices_for_specified_good,
                                       get_prices_for_non_specified_good)

app = Celery('get_information',
             broker=os.environ.get('BROKER_URL'),
             backend=os.environ.get('BACKEND_URL'))


# Parses information about product for the first time and starts update.
@app.task()
def get_info_about_product(url):
    info = parse_info_about_product(url)
    result = {
        "name": info[0],
        "full_price": info[1],
        "price_with_card": info[2],
        "price_on_sale": info[3]
    }
    update_info_about_product.delay(url)
    return result


# Updates information about product in db one time per hour.
@app.task()
def update_info_about_product(url):
    time.sleep(60)
    product_info = parse_info_about_product(url)
    product_in_schema = {"full_price": product_info[1],
                         "price_with_card": product_info[2],
                         "price_on_sale": product_info[3]}
    connecting_to_db().update_information_about_product(product_in_schema, product_info[0])
    update_info_about_product.delay(url)


# Parses all information about product.
def parse_info_about_product(url):
    soup = get_product_html(url)

    if check_for_alternatives(soup):
        name, full_price, price_with_card, price_on_sale = get_prices_for_specified_good(soup, url)
        return [name, full_price, price_with_card, price_on_sale]

    name = find_name(soup)
    if check_availability(soup):
        full_price = get_price(soup)
        price_on_sale = 0
        price_with_card = 0
        return [name, full_price, price_with_card, price_on_sale]

    else:
        full_price, price_with_card, price_on_sale = get_prices_for_non_specified_good(soup)
        return [name, full_price, price_with_card, price_on_sale]
