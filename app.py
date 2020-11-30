import os
import csv
import json
import time
import pytz
import numpy
import requests
import schedule
import psycopg2
import pandas as pd 
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.blocking import BlockingScheduler

DATABASE_URL = "postgres://tfjiopqvoihdjk:8498a090be6eef60a073c56f68564abe983724e448d9c7815db2b493953b19f2@ec2-52-72-34-184.compute-1.amazonaws.com:5432/d634219rgelf7s"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

def extract_price(driver):
    html = driver.page_source
    try:
        soup = BeautifulSoup(html, "html.parser")
        all_divs = soup.find('div', {'class' : '_1cMg'})
        price_str = all_divs.text
        price = float((price_str.split('₹'))[1].split('/')[0])
    except AttributeError:
        price = 0
    return price

def fetchprice():
    cursor.execute("select *from goldprice ORDER BY index DESC LIMIT 1")
    data = cursor.fetchone()
    last_buy_price = data[1]
    last_sell_price = data[2]
    return (last_buy_price, last_sell_price)  

def updateprice(buy_price, sell_price):
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    date = datetime_ist.strftime('%a %b %d %Y time - %H:%M:%S ')
    cursor.execute("update goldprice set todtime = %s, buy = %s, sell = %s where index = (select max(index) from goldprice) )",[date, buy_price, sell_price])
    conn.commit()   
        
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    url = "https://paytm.com/digitalgold"
    driver.get(url)
    time.sleep(3)
    cur_val = extract_price(driver)
    buy_price = round(cur_val + ((3*cur_val)/100),2)
    
    element = driver.find_element_by_link_text("Sell")
    element.click()
    sell_price = extract_price(driver)
    time.sleep(2)
    last_buy_price, last_sell_price = fetchprice()
    
    if buy_price != last_buy_price or sell_price != last_sell_price:
        requests.get("https://api.telegram.org/bot1340927566:AAHzy54vtOJcqB2OKO5Qgo5vHzLxvNYdkRY/sendMessage?chat_id=985062789&text=buy = {} : sell = {}".format(str(buy_price), str(sell_price))) 
        updateprice(buy_price, sell_price)
    driver.close()
    
sched.start()

# def current_gold_price():
#     r = requests.get('https://www.goodreturns.in/gold-rates/').text
#     soup = BeautifulSoup(r, "html.parser")
#     article = soup.find('div', id='current-price')
#     s_price = article.strong.text
#     price = int((s_price.split()[1]).replace(',',''))
#     return price

