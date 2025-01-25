import pandas as pd
import numpy as np
import scipy.stats as stats
from func import z_test_two_samples
import scipy

df = pd.read_csv('updated_walmart_products.csv')

# 3 - What factors affect sales?

# 3.1 - Does the unemployment rate affect sales?

# z-test with two samples

# My hypotheses:
# - the unemployment rate does not affect sales
# - the unemployment rate affects sales

# divide df for 2 groups, 1 for low unemplyoment, 2 for high unemplyoment
low_unemplyoment = df[df['Unemployment'] <= df['Unemployment'].median()]
high_unemployment = df[df['Unemployment'] > df['Unemployment'].median()]

# sample mean
mean_low_sales = low_unemplyoment['Weekly_Sales'].mean()
mean_high_sales = high_unemployment['Weekly_Sales'].mean()

# standart deviation
low_pop_std = low_unemplyoment['Weekly_Sales'].std()
high_pop_std = high_unemployment['Weekly_Sales'].std()

# simple size
n_low = len(low_unemplyoment)
n_high = len(high_unemployment)

alpha = 0.05

z_score = (mean_high_sales - mean_high_sales)/np.sqrt((low_pop_std**2/n_low)+(high_pop_std**2/n_high))
print('Z-score: ', np.abs(z_score))

z_critical = stats.norm.ppf(1-alpha/2)
print('Critical Z-Score: ',z_critical)

p_value = 2*(1-stats.norm.cdf(np.abs(z_score)))
print('P-value: ', p_value)

if p_value<alpha:
   print('Reject Null Hypothesis. The unemployment rate affects sales')
else:
   print('Fail the reject the null hypothesis. The unemployment rate does not affect sales')



# 3.2 - Чи впливає температура в регіоні на продажі?
# use z-test 
temp_sales_effect = z_test_two_samples(df, 'Temperature', 'Weekly_Sales', alpha = 0.05, variable1 = 'temperature', variable2 = 'sales')
#print(temp_sales_effect)




# 3.3 - Чи впливає сезон на продажі конкретного товару?

#ANOVA - test

seasons =df['Season'].unique()
sales_by_season = [df[df['Season']==season]['Weekly_Sales'] for season in seasons]

f_stat, p_value = stats.f_oneway(*sales_by_season)
print('F-statistic: ', f_stat)
print('P-value: ', p_value)

if p_value < 0.05:
    print('The season significantly affects sales')
else:
    print('The season does not significantly affect sales')