import numpy
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
from time import gmtime, strftime, sleep

def current_gold_price():
    r = requests.get('https://www.goodreturns.in/gold-rates/').text
    soup = BeautifulSoup(r, "html.parser")
    article = soup.find('div', id='current-price')
    s_price = article.strong.text
    price = int((s_price.split()[1]).replace(',',''))
    return price

prev = 0
while True:
    cur_val = current_gold_price()
    sleep(5)
    if prev != cur_val:
        start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        requests.get("https://api.telegram.org/bot1340927566:AAHzy54vtOJcqB2OKO5Qgo5vHzLxvNYdkRY/sendMessage?chat_id=985062789&text={} || {}".format(type(prev), type(cur_val)))
        prev = cur_val
