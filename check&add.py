from flask import Flask, request

app = Flask(__name__)


url_price_db = {}
sale_price_db = {}
check_result = {}


@app.route('/criteria', methods=['POST'])
def add_criteria():
    website_url = request.json['url']
    sale = request.json['sale']
    price = request.json['price']
    if 'Nothing' in sale:
        url_price_db[website_url] = 'price'
        sale_price_db['price'] = price
    else:
        url_price_db[website_url] = 'sale'
        sale_price_db['sale'] = sale
    return {'dictionary1': url_price_db, 'dictionary2': sale_price_db}


@app.route('/check', methods=['POST'])
def check_current_price():
    website_url = request.json['url']
    current_price = request.json['price']
    criteria_price = request.json['criteria_price']
    if current_price > criteria_price:
        check_result[website_url] = False
        return check_result
    else:
        check_result[website_url] = True
        return check_result


if __name__ == '__main__':
    app.run(port=5000)
