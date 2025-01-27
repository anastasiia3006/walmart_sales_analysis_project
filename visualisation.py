import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('updated_walmart_products.csv')

# 1. Total sales by season (Bar Plot)
season_sales = df.groupby('Season')['Weekly_Sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
season_sales.plot(kind='bar', color=['blue', 'orange', 'green', 'red'], edgecolor='black')
plt.title('Total sales by season', fontsize=14)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Total sales', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# 2. Popular and not popular Products by Season (Stacked Bar Plot)
max_sales_df = pd.read_csv('max_season_sales.csv')
min_sales_df = pd.read_csv('min_season_sales.csv')

# We create a canvas for two graphs
fig, ax = plt.subplots(1, 2, figsize=(14, 6))  # 1 рядок, 2 стовпці

# Графік для максимальних продажів
ax[0].bar(max_sales_df['Season'], max_sales_df['Weekly Sales'], color='green', edgecolor='black')
ax[0].set_title('Maximum Sales by Season', fontsize=14)
ax[0].set_xlabel('Season', fontsize=12)
ax[0].set_ylabel('Maximum Sales', fontsize=12)
ax[0].grid(axis='y', linestyle='--', alpha=0.7)

# We add signatures for maximum sales
for index, row in max_sales_df.iterrows():
    ax[0].text(row['Season'], row['Weekly Sales'] + 50, row['Product Name'], ha='center', fontsize=10, color='black')

# A schedule for minimal sales
ax[1].bar(min_sales_df['Season'], min_sales_df['Weekly Sales'], color='red', edgecolor='black')
ax[1].set_title('Minimum Sales by Season', fontsize=14)
ax[1].set_xlabel('Season', fontsize=12)
ax[1].set_ylabel('Minimum Sales', fontsize=12)
ax[1].grid(axis='y', linestyle='--', alpha=0.7)

# We add signatures for minimum sales
for index, row in min_sales_df.iterrows():
    ax[1].text(row['Season'], row['Weekly Sales'] + 50, row['Product Name'], ha='center', fontsize=10, color='black')

plt.tight_layout()
plt.show()


# 3. Share of Holiday Sales (Pie Chart)
holiday_sales = df[df['Holiday_Flag'] == 1]['Weekly_Sales'].sum()
non_holiday_sales = df[df['Holiday_Flag'] == 0]['Weekly_Sales'].sum()

sales_data = [holiday_sales, non_holiday_sales]
labels = ['Holiday Sales', 'Non-Holiday Sales']

plt.figure(figsize=(8, 8))
plt.pie(sales_data, labels=labels, autopct='%1.1f%%', startangle=140, colors=['gold', 'skyblue'], explode=(0.1, 0))
plt.title('Part of the holiday sales', fontsize=14)
plt.show()