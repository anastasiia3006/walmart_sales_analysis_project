
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
 

    # Distribution of data into two groups by median

    median_value = df[group_col].median()
    low_group = df[df[group_col] <= median_value]
    high_group = df[df[group_col] > median_value]
    
    # Calculate the average values ​​for each group
    mean_low = low_group[value_col].mean()
    mean_high = high_group[value_col].mean()
    
    # Calculating standard deviations for each group
    low_std = low_group[value_col].std()
    high_std = high_group[value_col].std()
    
    # Sample sizes
    n_low = len(low_group)
    n_high = len(high_group)
    
    # Calculating the Z-statistic
    z_score = (mean_low - mean_high) / np.sqrt((low_std**2 / n_low) + (high_std**2 / n_high))
    
    # Critical Z value for a two-tailed test
    z_critical = stats.norm.ppf(1 - alpha / 2)  # for a two-tailed test, divide alpha by 2
    
    # Calculating the p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # two-tailed test
    
    # Test the hypothesis using the critical value of Z
    print('Z-Score:', z_score)
    print('Critical Z-Score:', z_critical)
    print('P-value:', p_value)
    
    if p_value < alpha:
        print( f"Reject Null Hypothesis: The {variable1} affects the target {variable2}.")
    else:
        print(f"Fail to Reject Null Hypothesis: The {variable1}  does not affect the target {variable2}.")