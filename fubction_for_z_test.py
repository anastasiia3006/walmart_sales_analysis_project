import numpy as np
import scipy.stats as stats


def z_test_two_samples(df, group_col, value_col, alpha=0.05):
    """
    Function to perform a two-tailed z-test for two selections.

    Parameters:
    - df: DataFrame, data to analyze.
    - group_col: str, column to group (e.g., 'Unemployment').
    - value_col: str, column to test (e.g., 'Weekly_Sales').
    - alpha: significance level for the test (default 0.05).

    Returns:
    - hypothesis result: whether to reject the null hypothesis or not.
    """

    # Split the data into two groups by the median
    median_value = df[group_col].median()
    low_group = df[df[group_col] <= median_value]
    high_group = df[df[group_col] > median_value]

    # Calculate the average values ​​for each group
    mean_low = low_group[value_col].mean()
    mean_high = high_group[value_col].mean()

    # Calculate standard deviations for each group
    low_std = low_group[value_col].std()
    high_std = high_group[value_col].std()

    # Sample sizes
    n_low = len(low_group)
    n_high = len(high_group)

    # Calculate the Z-statistic
    z_score = (mean_low - mean_high) / np.sqrt((low_std ** 2 / n_low) + (high_std ** 2 / n_high))

    # Critical Z value for a two-tailed test
    z_critical = stats.norm.ppf(1 - alpha / 2)  # for a two-tailed test, divide alpha by 2

    # Calculate p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # two-tailed test

    # Test the hypothesis using the critical value of Z
    print('Z-Score:', z_score)
    print('Critical Z-Score:', z_critical)
    print('P-value:', p_value)

    if p_value < alpha:
        return "Reject Null Hypothesis: The variable affects the target variable."
    else:
        return "Fail to Reject Null Hypothesis: The variable does not affect the target variable."
