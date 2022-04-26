import logging
from idlelib.configdialog import is_int
from bs4 import BeautifulSoup
import requests
from requests.exceptions import (RequestException, InvalidURL, InvalidSchema, MissingSchema,
                                 URLRequired, HTTPError, Timeout, ConnectTimeout,
                                 ReadTimeout, InvalidHeader, ContentDecodingError,
                                 StreamConsumedError)

logger = logging.getLogger()


# This function takes as an input products URL, that user sends.
# Than parses website to find and save "sale" price of the good.
def get_product_html(website_url):
    headers = {
        'User-Agent': 'PostmanRuntime/7.28.4'}
    try:
        # scrape raw site
        website = requests.get(website_url, headers=headers)

    except (RequestException, InvalidURL, InvalidSchema, MissingSchema,
            URLRequired, HTTPError, Timeout, ConnectTimeout,
            ReadTimeout, InvalidHeader, ContentDecodingError,
            StreamConsumedError) as e:
        logger.exception(f"While getting page the following exception occurred: {e}")
        raise {"error": {"code": 500,
                         "name": "Internal Server Error"}}

    # scrape site
    soup = BeautifulSoup(website.content, "html.parser")

    if soup is None:
        logger.exception(f"Website {website_url} is empty.")
        raise {"error": {"code": 500,
                         "name": "Internal Server Error"}}

    return soup


# This function checks if user inputs sephora URL
def check_sephora_url(website_url):
    return "sephora" in website_url


# This function checks if user inputs sephora product URL
def check_sephora_product_url(soup):
    m_list = soup.find("div", {"class": "b-product-list__item"})
    return m_list is not None


# This function finds the name of the good
def find_name(soup):
    name_of_good = soup.find("span", {"class": "b-crumbs__current"}).get_text()
    return name_of_good


# This function differs two types of web pages where product has alternatives and has none
def check_for_alternatives(soup):
    m_list = soup.findAll("span", {"class": "b-card-option__image"})
    return len(m_list) > 1


# This function cuts part of page html where is information about user's type of product
def cut_part_need(soup, website_url):
    # get id of the good
    product = "_prod"
    prod_id = str(website_url[-6:] + product)
    temp = soup.find(id=prod_id)
    part_of_soup = temp
    return part_of_soup


# Check the basis of the discount
def check_specific_price(part_of_soup):
    # find if the price discount is provided by card or by current sale
    check = part_of_soup.find("div",
                              {"class": "b-card__price b-card__price--discount-card"})
    return check is None


# Find low price of the specific good
def get_specific_low_price(part_of_soup):
    # Get a price as a list and transform into int
    raw_low_price = part_of_soup.findAll("div", {"class": "b-card__price-value"})[0].get_text().split()
    low_price = str(raw_low_price[0]) + str(raw_low_price[1])
    return int(low_price)


# Find high price of the specific good
def get_specific_high_price(part_of_soup):
    # Get a price as a list and transform into int
    raw_high_price = part_of_soup.findAll("div", {"class": "b-card__price-value"})[1].get_text().split()
    high_price = str(raw_high_price[0]) + str(raw_high_price[1])
    return int(high_price)


# This function checks the basis of the discount (card or sale)
def check_price(soup):
    # find if the price discount is provided by card or by current sale
    return bool(soup.find("div",
                          {"class": "b-card__price b-card__price--discount-card"}))


# This function gets full price of the good without card
def get_full_price(soup):
    # find and save HighPrice
    raw_full_price = soup.find(itemprop="highPrice")
    if raw_full_price:
        full_price = int(raw_full_price['content'])
        # return current high price of the good
        return full_price
    else:
        return None


# This function checks if product is available
def check_availability(soup):
    return bool(soup.find("div", {"class": "b-card__not-available"}))


# Parses price of the non-available good
def get_price(soup):
    price = soup.find("div",
                      {"class": "b-card__price-value"})
    if price.get_text():
        return int(price.get_text().replace('\n', '').replace('c', '').replace(' ', ''))
    else:
        return None


# This function gets current price of the good with card
def get_price_with_card(soup):
    # find and save LowPrice
    raw_price_with_card = soup.find(itemprop="lowPrice")
    price_with_card = int(raw_price_with_card['content'])

    # return current low price of the good
    return price_with_card


# This function gets price with discount based on sale
def get_low_price(soup):
    # find and save LowPrice
    raw_low_price = soup.find(itemprop="lowPrice" or "price")
    if raw_low_price:
        low_price = int(raw_low_price['content'])

        # return current low price of the good
        return low_price
    else:
        return None


# This function gets price without discount based on sale
def get_high_price(soup):
    # find and save HighPrice
    raw_high_price = soup.find(itemprop="highPrice")
    high_price = int(raw_high_price['content'])

    # return current high price of the good
    return high_price


# This function compares current low price of the good and users discount price
# NB! Full price in terms of sephora sale system is a price without any card discounts
def compare_price_discount(low_price, discount, full_price):
    # count low users price
    disc_price = (discount * 100) / full_price
    return disc_price <= low_price


# This function compares price of the good and price that consumer wants
def compare_prices(low_price, user_price):
    return low_price <= user_price


# Parses prices for good with types
def get_prices_for_specified_good(soup, url):
    name = find_name(soup) + ' ' + str(url[-6:])
    part_of_soup = cut_part_need(soup, url)

    if check_availability(part_of_soup):
        full_price = get_specific_low_price(part_of_soup)
        price_with_card = full_price
        price_on_sale = price_with_card
        return [name, full_price, price_with_card, price_on_sale]
    else:
        full_price = get_specific_high_price(part_of_soup)
        price_with_card = get_specific_low_price(part_of_soup)
        price_on_sale = price_with_card
        return [name, full_price, price_with_card, price_on_sale]


# Parses prices of the good with no types
def get_prices_for_non_specified_good(soup):
    if check_price(soup):
        full_price = get_full_price(soup)
        price_with_card = get_price_with_card(soup)
        price_on_sale = 0
    else:
        full_price = get_high_price(soup)
        price_on_sale = get_low_price(soup)
        price_with_card = 0
    return full_price, price_with_card, price_on_sale


# Checks if consumer has chosen type of the product
def check_choice_of_alternative(url):
    soup = get_product_html(url)
    if check_for_alternatives(soup) and is_int(url[-6:]):
        return True
    if not check_for_alternatives(soup):
        return True
    return False


if __name__ == "__main__":
    print(check_choice_of_alternative(
        'https://sephora.ru/make-up/lips/pomade/clarins-joli-rouge-gubnaya-prod1yvc/#store_346243'))
