
import pandas as pd
import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# import datetime

# from statsmodels.tools.sequences import primes_from_2_to
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('Walmart.csv')

# check the data in table
# print(df.head)
# print(df.shape)
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())
# print(df.dtypes)

# тут перетвории в формат дати зрозумілого для пайтон
df['Date'] = pd.to_datetime(df['Date'], format = '%d-%m-%Y')

def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'

# тут додали нову колонку - сезони до таблиці
season = ['Winter', 'Summer', 'Autumn', 'Spring']
df['Season'] = df['Date'].apply(get_season)

# тут створюємо медіану продажів для кожного сезону,
# від неї будемо відштовхуватися і робити аналіз усіх продажів

#спочатку групуємо дані за значенням у cтовбці Season
grouped_season = df.groupby('Season')

for season, group in grouped_season:
    if season == 'Winter':
        winter_median = group['Weekly_Sales'].median()
    elif season == 'Summer':
        summer_median = group['Weekly_Sales'].median()
    elif season == 'Autumn':
        autumn_median = group['Weekly_Sales'].median()
    else:
        spring_median = group['Weekly_Sales'].median()


# перевірка чи в сезоні є святкові дні
# якщо є то яку частину прибутку вони становлять,
# на скільки відсотків вони підвищують прибуток магазину

def check_for_holiday_flag(group, season_median):
    holiday_sales = df[df['Holiday_Flag'] == 1]['Weekly_Sales']
    if not holiday_sales.empty:
        holiday_median=holiday_sales.median()
        holiday_share = holiday_sales/season_median
        increase_percentage = ((holiday_median - season_median)/season_median)* 100
        return holiday_share, increase_percentage
    else:
        return 0,0












#цей блок коду робить візуалізацію для дати та кількості продажів 21.01.25
#-----------------------------------------------------------------------------
#function for formating Y(present numbers withiut scientiestic notation)
# def millions(x, pos):
#     return f'{int(x/1e6)}M'
# formatter = FuncFormatter(millions)
#
# #print(df.to_string())
#
# x = df['Date']
# y = df['Weekly_Sales']
#
# plt.figure(figsize=(12,6))
# plt.bar(x, y, label ='Weekly Sales')
#
# plt.title('Sales')
# plt.xlabel('Season')
# plt.ylabel('Weekly Sales')
#
# plt.gca().yaxis.set_major_formatter(formatter)
#
# plt.xticks(rotation = 45)
# plt.ylim(0,y.max()*1.1)
# plt.legend()
# plt.tight_layout()
# plt.show()
#-------------------------------------------------------------------------------




