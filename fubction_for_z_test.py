import numpy as np
import scipy.stats as stats


def z_test_two_samples(df, group_col, value_col, alpha=0.05):
    """
    Функція для проведення двостороннього z-тесту для двох вибірок.

    Параметри:
    - df: DataFrame, дані для аналізу.
    - group_col: str, стовпець для групування (наприклад, 'Unemployment').
    - value_col: str, стовпець для перевірки (наприклад, 'Weekly_Sales').
    - alpha: рівень значущості для тесту (за замовчуванням 0.05).

    Повертає:
    - результат гіпотези: чи відкидаємо нульову гіпотезу чи ні.
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
    z_score = (mean_low - mean_high) / np.sqrt((low_std ** 2 / n_low) + (high_std ** 2 / n_high))

    # Критичне значення Z для двостороннього тесту
    z_critical = stats.norm.ppf(1 - alpha / 2)  # для двостороннього тесту ділимо alpha на 2

    # Обчислюємо p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # двосторонній тест

    # Перевіряємо гіпотезу за критичним значенням Z
    print('Z-Score:', z_score)
    print('Critical Z-Score:', z_critical)
    print('P-value:', p_value)

    if p_value < alpha:
        return "Reject Null Hypothesis: The variable affects the target variable."
    else:
        return "Fail to Reject Null Hypothesis: The variable does not affect the target variable."

