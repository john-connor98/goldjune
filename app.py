import numpy
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
from time import sleep
from flask import Flask, request, make_response, render_template
from flask_cors import cross_origin

def current_gold_price():
    r = requests.get('https://www.goodreturns.in/gold-rates/').text
    soup = BeautifulSoup(r, "html.parser")
    article = soup.find('div', id='current-price')
    s_price = article.strong.text
    price = int((s_price.split()[1]).replace(',',''))
    return price

app = Flask(__name__)
nnum = 1
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
    cur_val = current_gold_price()
    nnum+=1
    answ = f'count :- {nnum} || price :- {cur_val}'
    return {
              "fulfillmentMessages": [
                {
                  "text": {
                    "text":  [
                         answ
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
