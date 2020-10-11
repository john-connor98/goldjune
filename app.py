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
i = 0
while i<10000000:
    cur_val = int(current_gold_price())
    if prev != cur_val:
        start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        requests.get("https://api.telegram.org/bot1340927566:AAHzy54vtOJcqB2OKO5Qgo5vHzLxvNYdkRY/sendMessage?chat_id=985062789&text={} : {} || {}".format(str(i), str(prev), str(cur_val)))
    prev = cur_val
    i+=1
