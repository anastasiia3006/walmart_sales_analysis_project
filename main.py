import pandas as pd
import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# import datetime
#
# from statsmodels.tools.sequences import primes_from_2_to
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv('Walmart.csv')

#chaek the data in table
# print(df.head)
# print(df.shape)
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())

print(df.dtypes)

df['Date'] = pd.to_datetime(df['Date'], format = '%d-%m-%Y')
df['day_of_week'] = df['Date'].dt.strftime('%A') # created column with days of weeks

#function for formating Y(present numbers withiut scientiestic notation)
def millions(x, pos):
    return f'{int(x/1e6)}M'
formatter = FuncFormatter(millions)

#print(df.to_string())

x = df['Date']
y = df['Weekly_Sales']

plt.figure(figsize=(12,6))
plt.bar(x, y, label ='Weekly Sales')

plt.title('Sales')
plt.xlabel('Season')
plt.ylabel('Weekly Sales')

plt.gca().yaxis.set_major_formatter(formatter)

plt.xticks(rotation = 45)
plt.ylim(0,y.max()*1.1)
plt.legend()
plt.tight_layout()
plt.show()

# df['Date'] = pd.to_datetime(df['Date'], errors = 'coerce')
#
# def get_season(date):
#     month = date.month
#     if month in [12, 1, 2]:
#         return 'Winter'
#     elif month in [3, 4, 5]:
#         return 'Spring'
#     elif month in [6, 7, 8]:
#         return 'Summer'
#     elif month in [9, 10, 11]:
#         return 'Autumn'
#
# season = ['Winter', 'Summer', 'Autumn', 'Spring']
# df['Season'] = df['Date'].apply(get_season)
# print(df)
#
# seasonal_sales = df.groupby('Season')['Weekly_Sales'].sum()
#
# seasonal_sales = seasonal_sales.reindex(['Winter', 'Spring', 'Summer', 'Autumn'])
#
# custom_palette = {'Winter': 'red', 'Spring': 'blue', 'Summer': 'green', 'Autumn': 'pink'}
#
# sns.set(rc={'figure.figsize':(10,6)})
# seasonal_sales.plot(kind='bar',color=[custom_palette[season] for season in seasonal_sales.index])
#
#
# plt.title('Sales by seasons', fontsize = 16)
# plt.xlabel('Season', fontsize = 14)
# plt.ylabel('Sales (Weekly Sales)', fontsize = 16)
# plt.xticks(rotation=60)
# plt.grid(True)
# plt.show()



