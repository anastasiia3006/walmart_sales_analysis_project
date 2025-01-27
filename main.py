
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy import stats
from scipy.stats import ttest_ind

#add db walmart with list of products

df = pd.read_excel('walmart_productts.xlsx')
df.to_csv('walmart_products.csv', index = False)

# check the data in table

# print(df.head)
# print(df.shape)
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())
# print(df.dtypes)


# remove missing values
df['SELLER'] = df['SELLER'].fillna('Unknown')
df['BRAND'] = df['BRAND'].fillna('Unknown')

# to check missing values
#print(df.describe())
#print('Is not null',df.isnull().sum())

# convert date to date type in .py
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

# add new column to db
season = ['Winter', 'Summer', 'Autumn', 'Spring']
df['Season'] = df['Date'].apply(get_season)

# update this in db
df.to_csv('updated_walmart_products.csv', index=False)

# here we create a median of sales for each season,
# we will start from it and analyze all sales

# first we group the data by the value in the Season column
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

# check if there are holidays in the season
# if there are, what part of the profit do they make up,
# by how much percent do they increase the store's profit

def check_for_holiday_flag(group, season_total_sales):
    # Calculation of the share of holiday sales    
    holiday_sales = group[group['Holiday_Flag'] == 1]['Weekly_Sales']
    non_holiday_sales = group[group['Holiday_Flag'] == 0]['Weekly_Sales']

    if not holiday_sales.empty:
        # Calculation of the share of holiday sales
        holiday_total = holiday_sales.sum()
        holiday_share = holiday_total/season_total_sales
        increase_percentage = (holiday_total - season_total_sales)* 100

        result = 'Holiday sales increase overall profits' if increase_percentage > 0 else 'Holiday sales did not boost profits'

        increase_percentage_round = round(increase_percentage, 2)

        # Performing a t-test
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

        
# initialize the dictionary to store the results
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


season = input(str('Enter a season of the year ->   '))

# Check if the entered season is in the available list
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
else:
    print('Invalid season name. Please enter one of the following: Winter, Summer, Autumn, Spring.')



# 2
# in the next block of code we will analyze which products sell best in which season
# a function that will take a season and output the product that was bought the most in
# a certain season, and the amount of the product that was sold

max_sales_dict = {}

def max_season_sales(grouped_season):
    for season, group in grouped_season:
        max_sales = group.loc[group['Weekly_Sales'].idxmax()]
        max_sales_dict [season] = {
            'Product Name': max_sales['PRODUCT_NAME'],
            'Weekly Sales': max_sales['Weekly_Sales']
        }
    for season, product in max_sales_dict.items():
        print(f'In {season} season, the product with maximum sales is {product['Product Name']} with {product['Weekly Sales']} sales in the week.')

max_season_sales(grouped_season)


min_sales_dict = {}

def min_season_sales(grouped_season):
    for season, group in grouped_season:
        min_sales = group.loc[group['Weekly_Sales'].idxmin()]
        min_sales_dict [season] = {
            'Product Name': min_sales['PRODUCT_NAME'],
            'Weekly Sales': min_sales['Weekly_Sales']
        }
    for season, product in min_sales_dict.items():
        print(f'In {season} season, the product with minimum sales is {product['Product Name']} with {product['Weekly Sales']} sales in the week.')

min_season_sales(grouped_season)

max_sales_df = pd.DataFrame(max_sales_dict).T.reset_index()
max_sales_df.columns = ['Season', 'Product Name', 'Weekly Sales']

# Створюємо DataFrame з мінімальними продажами
min_sales_df = pd.DataFrame(min_sales_dict).T.reset_index()
min_sales_df.columns = ['Season', 'Product Name', 'Weekly Sales']

# Зберігаємо дані в CSV файли
max_sales_df.to_csv('max_season_sales.csv', index=False)
min_sales_df.to_csv('min_season_sales.csv', index=False)

# - which products are most often purchased, which products of these brands account for a high share of sales in stores: BRAND, Weekly_Sales, Store, product_name
# - add the product brand when selecting

grouped_product = df.groupby('PRODUCT_NAME')['Weekly_Sales'].sum()

def most_frequent_product(grouped_product):
    best_selling_product = grouped_product.idxmax()
    best_selling_sales = grouped_product.max()
    best_selling_brand = df[df['PRODUCT_NAME'] == best_selling_product]['BRAND'].iloc[0]

    print(f"The best selling product is: {best_selling_product}")
    print(f"Brand: {best_selling_brand}")
    print(f"Total Weekly Sales: {best_selling_sales}")

most_frequent_product(grouped_product)
print('***')


# sorting products from those that are purchased the most to those that are not often in demand

sorted_products = grouped_product.sort_values(ascending=False)

product_rank = {product: rank+1 for rank, product in enumerate(sorted_products.index)}

df['Popular_products'] = df['PRODUCT_NAME'].apply(lambda x: product_rank.get(x, None))

popular_product = df[df['Popular_products'] > df['Popular_products'].mean()]
not_popular_product = df[df['Popular_products']<= df['Popular_products'].mean()]

df['Popular_products'] = df['Popular_products'].apply(lambda x: 'Popular product' if x > df['Popular_products'].mean() else 'Not popular product')
df['Popular_products'] = df['Popular_products'].fillna('Not popular product')

#print(df.to_string())
df.to_csv('updated_walmart_products.csv', index=False)


