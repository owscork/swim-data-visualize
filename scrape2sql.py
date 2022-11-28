import urllib.request
import mysql.connector
import time
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime


conn = mysql.connector.connect(user='root', password='@Kingpin12', host='localhost')

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(executable_path='/Users/owencorkery/Downloads/chromedriver')

url = "https://www.swimcloud.com/swimmer/426155/"


browser.get(url)

html = browser.page_source

browser.find_element(By.XPATH, '//*[@id="js-swimmer-profile-times"]/div/ul/li[2]/a').click()
time.sleep(5)

#html = browser.page_source
#soup = bs(html, features="html.parser")
cur = conn.cursor()

cur.execute("DROP DATABASE IF EXISTS OwenSwims")
cur.execute("CREATE DATABASE OwenSwims")
cur.execute("USE OwenSwims")

for n in range(1,34):

#//*[@id="js-swimmer-profile-times-container"]/div[1]/div/ul/li[33]/a
#//*[@id="js-swimmer-profile-times-container"]/div[1]/div/ul/li[32]/a
    browser.find_element(By.XPATH, '/html/body/div[2]/div[4]/div[3]/div/div[3]/div[1]/div/div/div[1]/div/button').click()
    
    browser.find_element(By.XPATH, '//*[@id="js-swimmer-profile-times-container"]/div[1]/div/ul/li['+str(n)+']/a').click()
    time.sleep(3)
#//*[@id="js-swimmer-profile-times-container"]/div[1]/div/ul/li[4]/a
#//*[@id="js-swimmer-profile-times-container"]/div[1]/div/ul/li[5]/a
    html = browser.page_source
    soup = bs(html, features="html.parser")
    w = soup.find("ul", attrs={"aria-labelledby":"byEventDropDownList"})
    f = w.find_all("li")
    event = f[n-1].text.strip()
    print(event)

    k = -1
    y = ""
    e = 0
    q = ""
    while event[k] != " ":
        y = event[k] + y
        k -= 1
    p = event[k-1]
    while event[e] != " ":
        q = q + event[e]
        e += 1
    
    q = y + q + p

    table = soup.find("table", attrs={"class": "c-table-clean table table-hover"})

    table_heads = table.thead.find_all("tr")
    headings = []
    for th in table_heads:
    # remove any newlines and extra spaces from left and right
        headings.append(th.text.replace('\n', ' ').strip())
    print(headings)
    table_data = table.tbody.find_all("tr")
    times = []
    meets = []
    dates = []
#print(table_data)
#RVONCEONC
    
    cur.execute("CREATE TABLE "+q+" (times VARCHAR(20), meets VARCHAR(100), dates VARCHAR(40), year INT, sec FLOAT)")

    m = 0
    for td in table_data:
        m += 1
    # remove any newlines and extra spaces from left and right
        td.text.strip()
        x = td.text.split("\n")
        while("" in x):
            x.remove("")
        if len(x) > 3:
            num = len(x) - 3
            for i in range(num):
                x.pop(1)
        times.append(x[0])
        meets.append(x[1])
        dates.append(x[2])
        if ":" in x[0]:
            #print(x[0])
            #x[0] = x[0].strip()
            if x[0][1] == ':':
                sec = (float(x[0][0]) * 60) + float(x[0][2:])
            else:
                sec = (float(x[0][0:2]) * 60) + float(x[0][3:])
            #tm = datetime.strptime(x[0], "%H:%M.%S")
            #print(tm)
            #print("########")
        else:
            #print(x[0])
            #x[0] = x[0].strip()
            #x[0] = "00:"+x[0]
            sec = float(x[0])
            #tm = datetime.strptime(x[0], "%H:%M.%S")
            #print(tm)
           # print("############")'''
        g = x[2]
        g = g.replace(",", "")
        #print(g)
        yr = int(g[-4:])
        t = "INSERT INTO "+q+" (times, meets, dates, year, sec) VALUES (%s, %s, %s, %s, %s)"
        v = (x[0], x[1], g, yr, sec)
        
        cur.execute(t, v)
        
        

    #times.append(td.text.replace('\n', ' ').strip())
    #print(times)

conn.commit()
'''print(times)
print(meets)
print(dates)
print(len(times))
print(len(meets))
print(len(dates))
print("###################################################################")


year = "2022"
j = 0
b = 100000.0
bests_t = []
bests_m = []
bests_d = []
for y in dates:
    if y[-4:] == year:
        if float(times[j]) < b:
            b = float(times[j])
            m = meets[j]
            d = dates[j]
    else:
        bests_t.append(b)
        bests_m.append(m)
        bests_d.append(d)
        year = str(int(year) - 1)
        b = float(times[j])
        m = meets[j]
        d = dates[j]
    j += 1

print(bests_t)
print(bests_m)
print(bests_d)'''










#years = soup.find("div", {"id": "js-swimmer-profile-times-container"})

#times = soup.find("div", {"id": "o-grid o-grid--cols-1 o-grid--cols-2@md o-grid--gap-45"})

#print(years)

#js-swimmer-profile-times-container

#js-swimmer-profile-times-container > div.o-grid.o-grid--cols-1.o-grid--cols-2\@md.o-grid--gap-45 > div.o-table-group > div > table

