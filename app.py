import numpy
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
from time import gmtime, strftime, sleep
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
import psycopg2


def current_gold_price():
    r = requests.get('https://www.goodreturns.in/gold-rates/').text
    soup = BeautifulSoup(r, "html.parser")
    article = soup.find('div', id='current-price')
    s_price = article.strong.text
    price = int((s_price.split()[1]).replace(',',''))
    return price

def fetchprice():
    DATABASE_URL = "postgres://tfjiopqvoihdjk:8498a090be6eef60a073c56f68564abe983724e448d9c7815db2b493953b19f2@ec2-52-72-34-184.compute-1.amazonaws.com:5432/d634219rgelf7s"
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("select price from goldprice")
    data = cursor.fetchone()
    lastprice = data[0]
    return lastprice  
    
    

# def job():
#     cur_val = int(current_gold_price())
#     requests.get("https://api.telegram.org/bot1340927566:AAHzy54vtOJcqB2OKO5Qgo5vHzLxvNYdkRY/sendMessage?chat_id=985062789&text=Price :- prev = {}: curr = {}".format(str(prev), str(cur_val)))
        
sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():
    cur_val = int(current_gold_price())
    last_price = int(fetchprice())
    requests.get("https://api.telegram.org/bot1340927566:AAHzy54vtOJcqB2OKO5Qgo5vHzLxvNYdkRY/sendMessage?chat_id=985062789&text=Price :- last = {} : curr = {}".format(str(last_price), str(cur_val))) 

sched.start()
