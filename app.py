import numpy
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from time import sleep

def current_gold_price():
    r = requests.get('https://www.goodreturns.in/gold-rates/').text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find('div', id='current-price')
    s_price = article.strong.text
    price = int((s_price.split()[1]).replace(',',''))
    return price

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    res = manage_query(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def manage_query(req):
    cur_val = str(current_gold_price())
    return {
              "fulfillmentMessages": [
                {
                  "text": {
                    "text":  [
                         cur_val
                    ]
                    
                  }
                }
              ]
            }
    # return {
    #           "fulfillmentMessages": [
    #             {
    #               "text": {
    #                 "text": [
    #                   query
    #                 ]
    #               }
    #             }
    #           ]
    #         }

if __name__ == '__main__':
    app.run()
