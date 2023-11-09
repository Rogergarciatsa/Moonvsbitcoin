from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime as dt
import os

#import matrix csv
dataFrame = pd.read_csv(r'D:\Python\Moonvsbitcoin\HistoricalData\BitcoinHistoricalData.csv')
#import date today
datetoday = dt.datetime.today().strftime("%m/%d/%Y")

driver = webdriver.Chrome()
driver.get('https://www.investing.com/crypto/bitcoin/historical-data')

#click cookies
CookiesAccept = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
CookiesAccept.click()

#find BTC Price and convrt to int
BTCpriceToday = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]')
BTCpriceToday = BTCpriceToday.text

print(BTCpriceToday)
print(datetoday)
print(dataFrame)

#insert date today and today price
new_row = pd.DataFrame({'Date':(datetoday), 'Price':(BTCpriceToday)}, index=[0])
df2 = pd.concat([new_row,dataFrame.loc[:]]).reset_index(drop=True)
print(df2)

#drop unwanted columns, transform str to float and currency
df2 = df2.drop(columns=['Open', 'High', 'Low', 'Vol.', 'Change %'])
df2['Price'] = df2['Price'].replace(',', '', regex=True).astype(float)
df2['Price'] = df2['Price'].map('${:,.2f}'.format)
print(df2)
