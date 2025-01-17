import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('Walmart.csv')

# print(df.head)
# print(df.shape)
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())
# df.hist(figsize=(10,8)) #check for columns
# plt.show()

df['Date'] = pd.to_datetime(df['Date'], errors = 'coerce')

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

season = ['Winter', 'Summer', 'Autumn', 'Spring']
df['Season'] = df['Date'].apply(get_season)

seasonal_sales = df.groupby('Season')['Weekly_Sales'].sum()

seasonal_sales = seasonal_sales.reindex(['Winter', 'Spring', 'Summer', 'Autumn'])

custom_palette = {'Winter': 'red', 'Spring': 'blue', 'Summer': 'green', 'Autumn': 'pink'}

sns.set(rc={'figure.figsize':(10,6)})
seasonal_sales.plot(kind='bar',color=[custom_palette[season] for season in seasonal_sales.index])


plt.title('Sales by seasons', fontsize = 16)
plt.xlabel('Season', fontsize = 14)
plt.ylabel('Sales (Weekly Sales)', fontsize = 16)
plt.xticks(rotation=60)
plt.grid(True)
plt.show()



