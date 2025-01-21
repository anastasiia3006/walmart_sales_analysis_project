
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
    holiday_sales = group[group['Holiday_Flag'] == 1]['Weekly_Sales']
    non_holiday_sales = group[group['Holiday_Flag'] == 0]['Weekly_Sales']

    if not holiday_sales.empty:
        holiday_total=holiday_sales.sum()
        holiday_share = holiday_total/season_total_sales
        increase_percentage = ((holiday_total - season_total_sales)/season_total_sales)* 100

        if increase_percentage > 0:
            result = 'Holiday sales increase overall profits'
        elif increase_percentage < 0:
            result = 'The profit of the store does not change'
        else:
            result = 'Holiday sales have no impact on overall profits'

        increase_percentage_round = round(increase_percentage, 2)
        
        print("Holiday Sales Analysis:")
        print(f"- The share of sales during holidays: {holiday_share:.2%}")
        print(f"- {result}: {increase_percentage_round}%")

        # Виконання t-тесту
        if not non_holiday_sales.empty:
            t_stat, p_value = ttest_ind(holiday_sales, non_holiday_sales, equal_var=False)

            print("\nT-Test Analysis:")
            print(f"- T-statistic: {t_stat:.2f}")
            print(f"- P-value: {p_value:.4f}")

            # Інтерпретація результату
            alpha = 0.05  # Рівень значущості
            if p_value < alpha:
                print("There is a statistically significant difference between holiday and non-holiday sales.")
            else:
                print("There is no statistically significant difference between holiday and non-holiday sales.")
        else:
            print("\nNo non-holiday sales available for comparison.")
    else:
        print('No holiday sales in this season.')

        
# ініціалізуємо словник для збереженнярезультатів
seasonal_holiday_sales = {}

winter_holiday_sales = check_for_holiday_flag(grouped_season.get_group('Winter'), winter_total_sales)
summer_holiday_sales = check_for_holiday_flag(grouped_season.get_group('Summer'), summer_total_sales)
autumn_holiday_sales = check_for_holiday_flag(grouped_season.get_group('Autumn'), autumn_total_sales)
spring_holiday_sales = check_for_holiday_flag(grouped_season.get_group('Spring'), spring_total_sales)

def to_check_the_season(season):
    for season, analysis in seasonal_holiday_sales.items():
        print(f'{season} Holiday Sales Analysis: ')
        if analysis:
            print(f"- The share of sales during holidays: {analysis['share']}")
            print(f"- {analysis['result']}: {analysis['profit_change']}")
            print(f"T-Test Analysis:")
            print(f"- T-statistic: {analysis['t_stat']}")
            print(f"- P-value: {analysis['p_value']}")
        else:
            print("- No holiday sales in this season.")
        print("***")

print(to_check_the_season(summer_total_sales))

#print(check_for_holiday_flag(grouped_season.get_group('Winter'), season_total_sales))

'''Conclusions of the Analysis:

1. **Share of Sales During Holidays**:  
    Only 15.71% of the total seasonal sales occur during holidays.
    This indicates that holidays are not a major driver of revenue for the store.

2. **Overall Profit Change**:  
   Sales during holidays reduce overall profits by 84.29%.
   This suggests that the sales volumes on holidays are significantly lower than the average sales for the entire season.

3. **T-Test Results**:  
   - The **T-statistic (-1.82)** and **P-value (0.0691)** indicate that the difference 
   between holiday and non-holiday sales **is not statistically significant**.  
   - Since the P-value exceeds the commonly used significance level (α = 0.05), 
   we cannot confidently conclude that holidays have a significant impact on sales volumes.

### Main Conclusion:  
Holidays during the analyzed season are not a key driver of sales for the store. 
The sales volumes on these days are significantly lower than the overall seasonal average, 
but the difference is not statistically significant. This may imply that holiday promotions 
or strategies are not delivering the expected results, or customers do not consider this period 
as a time for active shopping.'''










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




