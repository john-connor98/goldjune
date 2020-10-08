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

i=0
while True:
    cur_val = current_gold_price()
    sleep(5)
    print(cur_val)
