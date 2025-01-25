
from datetime import date
import pandas as pd
import numpy as np
import scipy.stats as stats


# z-test
def z_test_two_samples(df, group_col, value_col, variable1, variable2, alpha=0.05):
    """
    A function to perform a two-tailed z-test for two samples.
    
    Parameters:
    - df: DataFrame, data for analysis.
    - group_col: str, the column to group by (eg 'Unemployment').
    - value_col: str, the column to check (eg 'Weekly_Sales').
    - alpha: significance level for the test (default 0.05).
    
    Returns:
    - the result of the hypothesis: whether we reject the null hypothesis or not.
    """
 

    # Розподіляємо дані на дві групи за медіаною

    median_value = df[group_col].median()
    low_group = df[df[group_col] <= median_value]
    high_group = df[df[group_col] > median_value]
    
    # Обчислюємо середні значення для кожної групи
    mean_low = low_group[value_col].mean()
    mean_high = high_group[value_col].mean()
    
    # Обчислюємо стандартні відхилення для кожної групи
    low_std = low_group[value_col].std()
    high_std = high_group[value_col].std()
    
    # Розміри вибірок
    n_low = len(low_group)
    n_high = len(high_group)
    
    # Обчислюємо Z-статистику
    z_score = (mean_low - mean_high) / np.sqrt((low_std**2 / n_low) + (high_std**2 / n_high))
    
    # Критичне значення Z для двостороннього тесту
    z_critical = stats.norm.ppf(1 - alpha / 2)  # для двостороннього тесту ділимо alpha на 2
    
    # Обчислюємо p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # двосторонній тест
    
    # Перевіряємо гіпотезу за критичним значенням Z
    print('Z-Score:', z_score)
    print('Critical Z-Score:', z_critical)
    print('P-value:', p_value)
    
    if p_value < alpha:
        print( f"Reject Null Hypothesis: The {variable1} affects the target {variable2}.")
    else:
        print(f"Fail to Reject Null Hypothesis: The {variable1}  does not affect the target {variable2}.")