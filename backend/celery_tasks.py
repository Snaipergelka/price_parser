from celery import Celery
from backend.parser import (get_product_html,
                            find_name,
                            get_price,
                            check_availability,
                            check_for_alternatives,
                            get_prices_for_specified_good,
                            get_prices_for_non_specified_good)

app = Celery('get_information', broker='redis://localhost:6379', backend='redis://localhost:6379')


@app.task()
def get_info_about_product(url):
    soup = get_product_html(url)
    name = find_name(soup)

    if check_for_alternatives(soup):
        name, full_price, price_with_card, price_on_sale = get_prices_for_specified_good(soup, url)
        return [name, full_price, price_with_card, price_on_sale]

    if check_availability(soup):
        full_price = get_price(soup)
        price_on_sale = 0
        price_with_card = 0
        return [name, full_price, price_with_card, price_on_sale]

    else:
        full_price, price_with_card, price_on_sale = get_prices_for_non_specified_good(soup)
        return [name, full_price, price_with_card, price_on_sale]
