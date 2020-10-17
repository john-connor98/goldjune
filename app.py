import numpy
import csv
import json
import time
import requests
import schedule
import psycopg2
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler

DATABASE_URL = "postgres://tfjiopqvoihdjk:8498a090be6eef60a073c56f68564abe983724e448d9c7815db2b493953b19f2@ec2-52-72-34-184.compute-1.amazonaws.com:5432/d634219rgelf7s"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

def extract_price(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find('div', {'class' : '_1cMg'})
    price_str = all_divs.text
    price = float((price_str.split('₹'))[1].split('/')[0])
    return price
# def current_gold_price():
#     r = requests.get('https://www.goodreturns.in/gold-rates/').text
#     soup = BeautifulSoup(r, "html.parser")
#     article = soup.find('div', id='current-price')
#     s_price = article.strong.text
#     price = int((s_price.split()[1]).replace(',',''))
#     return price

# def fetchprice():
#     cursor.execute("select buy, sell from goldprice")
#     data = cursor.fetchone()
#     last_buy_price = data[0]
#     last_sell_price = data[1]
#     return last_buy_price, last_sell_price  

# def updateprice(buy_price, sell_price):
#     cursor.execute("update goldprice set buy = (%s), sell = (%s) where buy>=0", [buy_price, sell_price])
#     conn.commit()   
        
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    url = "https://paytm.com/digitalgold"
    driver = webdriver.Chrome(r'chromedriver.exe')
    driver.get(url)
    time.sleep(3)
    cur_val = extract_price(driver)
    buy_price = price + ((3*price)/100)
    
    element = driver.find_element_by_link_text("Sell")
    element.click()
    sell_price = extract_price(driver)
    time.sleep(2)
    
    requests.get("https://api.telegram.org/bot1340927566:AAHzy54vtOJcqB2OKO5Qgo5vHzLxvNYdkRY/sendMessage?chat_id=985062789&text=buy_price = {} : sell_price = {}".format(str(buy_price), str(sell_price))) 
#     last_buy_price, last_sell_price = fetchprice()
    
#     if buy_val != last_buy_price or sell_price != last_sell_price:
#         requests.get("https://api.telegram.org/bot1340927566:AAHzy54vtOJcqB2OKO5Qgo5vHzLxvNYdkRY/sendMessage?chat_id=985062789&text=buy_price = {} : sell_price = {}".format(str(buy_price), str(sell_price))) 
#         updateprice(buy_price, sell_price)
    driver.close()
    
sched.start()
