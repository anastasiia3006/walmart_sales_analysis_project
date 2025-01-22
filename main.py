
import pandas as pd
import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# import datetime
from scipy.stats import ttest_ind

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

for season, group in grouped_season:
    if season == 'Winter':
        winter_total_sales = group['Weekly_Sales'].sum()
    elif season == 'Summer':
        summer_total_sales = group['Weekly_Sales'].sum()
    elif season == 'Autumn':
        autumn_total_sales = group['Weekly_Sales'].sum()
    else:
        spring_total_sales = group['Weekly_Sales'].sum()

# перевірка чи в сезоні є святкові дні
# якщо є то яку частину прибутку вони становлять,
# на скільки відсотків вони підвищують прибуток магазину

def check_for_holiday_flag(group, season_total_sales):
    # Calculation of the share of holiday sales    
    holiday_sales = group[group['Holiday_Flag'] == 1]['Weekly_Sales']
    non_holiday_sales = group[group['Holiday_Flag'] == 0]['Weekly_Sales']

    if not holiday_sales.empty:
        # Calculation of the share of holiday sales
        holiday_total = holiday_sales.sum()
        holiday_share = holiday_total/season_total_sales
        increase_percentage = (holiday_total - season_total_sales)* 100

        result = 'Holiday sales increase overall profits' if increase_percentage > 0 else 'Holiday sales have no impact on overall profits'

        increase_percentage_round = round(increase_percentage, 2)

        # Виконання t-тесту
        t_stat, p_value = (None, None)
        if not non_holiday_sales.empty:
            t_stat, p_value = ttest_ind(holiday_sales, non_holiday_sales, equal_var=False)


        return {
            "share": round(holiday_share, 2),
            "profit_change": f"{increase_percentage_round}%",
            "result": result,
            "t_stat": round(t_stat, 2) if t_stat is not None else None,
            "p_value": round(p_value, 4) if p_value is not None else None
        }
    else:
        return None

        
# ініціалізуємо словник для збереження результатів
seasonal_holiday_sales = {}

seasons = ['Winter', 'Summer', 'Autumn', 'Spring']
totals = [winter_total_sales, summer_total_sales, autumn_total_sales, spring_total_sales]

for season, total in zip(seasons, totals):
    seasonal_holiday_sales[season] = check_for_holiday_flag(grouped_season.get_group(season), total)

def to_check_the_season(season):
    for season, analysis in seasonal_holiday_sales.items():
        print(f'{season} Holiday Sales Analysis: ')
        if analysis:
            print(f"- The share of sales during holidays: {analysis['share']}")
            print(f"- {analysis['result']}: {analysis['profit_change']}")
            if analysis['t_stat'] is not None:
                print(f"T-Test Analysis:")
                print(f"- T-statistic: {analysis['t_stat']}")
                print(f"- P-value: {analysis['p_value']}")
        else:
            print("- No holiday sales in this season.")

#visualisation 

def plot_sales_by_season(season, total_sales):
    if total_sales>0:
        plt.figure(figsize= (12,6))
        plt.bar([season], [total_sales], color = 'b')
        plt.title(f'Sales in {season}')
        plt.xlabel('Season')
        plt.ylabel('Total Sales')
        plt.show()
    else:
        print(f'No sales data available for {season}.')

season = input(str('Enter a season of the year ->   '))

# Перевірка, чи введений сезон є в доступному списку
if season in seasonal_holiday_sales:
    analysis = seasonal_holiday_sales[season]
    total_sales = {
        'Winter': winter_total_sales,
        'Summer': summer_total_sales,
        'Autumn': autumn_total_sales,
        'Spring': spring_total_sales
    }[season]

    if analysis:
        print(f'{season} Holiday Sales Analysis:')
        print(f"- The share of sales during holidays: {analysis['share']}")
        print(f"- {analysis['result']}: {analysis['profit_change']}")
        if analysis['t_stat'] is not None:
            print(f"T-Test Analysis:")
            print(f"- T-statistic: {analysis['t_stat']}")
            print(f"- P-value: {analysis['p_value']}")
    else:
        print(f'- No holiday sales in the {season} season.')

    #sales visualisation
    plot_sales_by_season(season, total_sales)

else:
    print('Invalid season name. Please enter one of the following: Winter, Summer, Autumn, Spring.')













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




