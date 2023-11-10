from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import datetime as dt
import ephem
from skyfield.api import load, Topos
import os

#import matrix csv
dataFrame = pd.read_csv(r'D:\Python\Moonvsbitcoin\HistoricalData\BitcoinHistoricalData.csv')

# Convert the 'Date' column to a consistent format
dataFrame['Date'] = pd.to_datetime(dataFrame['Date'], format='%m/%d/%Y').dt.strftime("%m/%d/%Y")

#import date today
datetoday = dt.datetime.today().strftime("%m/%d/%Y")


driver = webdriver.Chrome()
driver.get('https://www.investing.com/crypto/bitcoin/historical-data')

# Wait for the "Accept Cookies" button to be clickable (up to 10 seconds)
cookies_accept_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
)

#click cookies
cookies_accept_button.click()

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

#moon phase calculation for today
def calculate_moon_phase(date):
    ephem_date = ephem.Date(date)
    return ephem.Moon(ephem_date).phase

#reset datetime format on dataframe
df2['Date'] = pd.to_datetime(df2['Date'], format='%m/%d/%Y')


# Apply the function to the 'Date' column and create a new 'Moon_Phase' column
df2['Moon_Phase'] = df2['Date'].apply(lambda x: ephem.Moon(x).phase)

print(df2)

#calculating full moons
df2['Moon_Status'] = np.where(df2['Moon_Phase'] > df2['Moon_Phase'].shift(1), 'Full Moon', np.where(df2['Moon_Phase'] < df2['Moon_Phase'].shift(1), 'New Moon', '='))


#adding calculations with price
df2['Price'] = df2['Price'].replace(',', '', regex=True).astype(float)
df2['Price_Difference'] = df2['Price'].diff(-1)
#df2 = pd.concat([df2, df2['Price_Difference']], axis=1)
#df2['Moon_Status'] = np.where(df2['Moon_Phase'] > 99, 'Full Moon', np.where(df2['Moon_Phase'] < 1, 'New Moon', ''))
last_moon_index = df2[df2['Moon_Status'].isin(['Full Moon', 'New Moon'])].index.max()
df2['Last_Moon_Index'] = last_moon_index
df2['Moon_Price_Difference'] = np.where(df2.index > last_moon_index, df2['Price_Difference'], np.nan)

print(df2)

#drop unwanted columns, transform str to float and currency
df2 = df2.drop(columns=['Open', 'High', 'Low', 'Vol.', 'Change %'])
df2['Price'] = df2['Price'].map('${:,.2f}'.format)
df2['Price_Difference'] = df2['Price_Difference'].map('${:,.2f}'.format)
print(df2.head(50))