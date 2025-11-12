# Statistical Tests Usage Guide

This guide demonstrates how to use the statistical analysis utilities for solar radiation data.

## Quick Start

```python
import sys
sys.path.insert(0, '../src')

from utils.data_loader import load_country, load_all
from analysis.statistical_tests import (
    StatisticalAnalyzer,
    compare_groups,
    quick_correlation_test,
    summary_statistics
)
```

## Example 1: Basic Statistical Analyzer

```python
from analysis.statistical_tests import StatisticalAnalyzer

# Initialize analyzer with significance level
analyzer = StatisticalAnalyzer(significance_level=0.05)

# Load data
df = load_country('benin', data_type='cleaned')
```

## Example 2: Normality Testing

```python
# Test if GHI follows normal distribution
result = analyzer.test_normality(df['GHI'], method='shapiro')
print(result['interpretation'])
print(f"Is normal: {result['is_normal']}")
print(f"P-value: {result['p_value']:.4f}")

# Try different methods
shapiro = analyzer.test_normality(df['GHI'], method='shapiro')
ks = analyzer.test_normality(df['GHI'], method='kstest')
anderson = analyzer.test_normality(df['Tamb'], method='anderson')

# Check multiple variables
for col in ['GHI', 'DNI', 'DHI', 'Tamb']:
    result = analyzer.test_normality(df[col])
    print(f"{col}: {result['interpretation']}")
```

## Example 3: Correlation Analysis with Significance

```python
# Full correlation matrix with p-values
result = analyzer.correlation_analysis(
    df,
    columns=['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS'],
    method='pearson'
)

print("Correlation Matrix:")
print(result['correlation'])
print("\nP-values:")
print(result['p_values'])
print(f"\nNumber of significant correlations: {result['significant_at_alpha']}")

# Spearman correlation (for non-normal data)
spearman_result = analyzer.correlation_analysis(
    df,
    columns=['GHI', 'Tamb'],
    method='spearman'
)
```

## Example 4: Quick Correlation Test

```python
from analysis.statistical_tests import quick_correlation_test

# Test correlation between two variables
result = quick_correlation_test(df['GHI'], df['Tamb'], method='pearson')
print(result['interpretation'])
print(f"Correlation: {result['correlation']:.3f}")
print(f"P-value: {result['p_value']:.4e}")
print(f"Significant: {result['significant']}")

# Test multiple pairs
pairs = [('GHI', 'Tamb'), ('GHI', 'RH'), ('DNI', 'Tamb')]
for var1, var2 in pairs:
    result = quick_correlation_test(df[var1], df[var2])
    print(f"{var1} vs {var2}: {result['interpretation']}")
```

## Example 5: Independent T-Test (Two Groups)

```python
# Load data from two countries
benin = load_country('benin', data_type='cleaned')
togo = load_country('togo', data_type='cleaned')

# Compare GHI between countries
result = analyzer.ttest_independent(
    benin['GHI'],
    togo['GHI'],
    equal_var=True  # Use False for Welch's t-test
)

print(result['interpretation'])
print(f"Test: {result['test']}")
print(f"Benin mean: {result['group1_mean']:.2f}")
print(f"Togo mean: {result['group2_mean']:.2f}")
print(f"P-value: {result['p_value']:.4f}")
print(f"Significant difference: {result['significant_difference']}")
```

## Example 6: One-Way ANOVA (Multiple Groups)

```python
# Load all countries
all_data = load_all(data_type='cleaned')

# Perform ANOVA
result = analyzer.anova_oneway(
    all_data['benin']['GHI'],
    all_data['togo']['GHI'],
    all_data['sierraleone']['GHI'],
    group_names=['Benin', 'Togo', 'Sierra Leone']
)

print(result['interpretation'])
print(f"F-statistic: {result['f_statistic']:.4f}")
print(f"P-value: {result['p_value']:.4e}")

# View group statistics
for group, stats in result['group_statistics'].items():
    print(f"\n{group}:")
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Std: {stats['std']:.2f}")
    print(f"  N: {stats['n']}")
```

## Example 7: Compare Groups (Convenience Function)

```python
from analysis.statistical_tests import compare_groups

# Prepare data dictionary
data_dict = {
    'Benin': all_data['benin']['GHI'],
    'Togo': all_data['togo']['GHI'],
    'Sierra Leone': all_data['sierraleone']['GHI']
}

# Parametric test (ANOVA)
result = compare_groups(data_dict, parametric=True)
print(result['interpretation'])

# Non-parametric test (Kruskal-Wallis)
result = compare_groups(data_dict, parametric=False)
print(result['interpretation'])
```

## Example 8: Mann-Whitney U Test (Non-Parametric)

```python
# For non-normal data, use Mann-Whitney U
result = analyzer.mann_whitney_u(
    benin['GHI'],
    togo['GHI'],
    alternative='two-sided'
)

print(result['interpretation'])
print(f"U-statistic: {result['u_statistic']:.2f}")
print(f"Benin median: {result['group1_median']:.2f}")
print(f"Togo median: {result['group2_median']:.2f}")
```

## Example 9: Kruskal-Wallis Test (Non-Parametric ANOVA)

```python
# Non-parametric alternative to ANOVA
result = analyzer.kruskal_wallis(
    all_data['benin']['GHI'],
    all_data['togo']['GHI'],
    all_data['sierraleone']['GHI'],
    group_names=['Benin', 'Togo', 'Sierra Leone']
)

print(result['interpretation'])
print(f"H-statistic: {result['h_statistic']:.4f}")

# View group medians
for group, stats in result['group_statistics'].items():
    print(f"{group} median: {stats['median']:.2f}")
```

## Example 10: Summary Statistics

```python
from analysis.statistical_tests import summary_statistics

# Basic summary
summary = summary_statistics(df, columns=['GHI', 'DNI', 'DHI', 'Tamb'])
print(summary)

# Summary by group
df_combined = pd.concat([
    all_data['benin'].assign(Country='Benin'),
    all_data['togo'].assign(Country='Togo'),
    all_data['sierraleone'].assign(Country='Sierra Leone')
])

summary = summary_statistics(
    df_combined,
    columns=['GHI', 'DNI', 'DHI'],
    group_by='Country'
)
print(summary)
```

## Example 11: Complete Analysis Workflow

```python
from utils import load_all
from analysis.statistical_tests import StatisticalAnalyzer, compare_groups

# Load data
all_data = load_all(data_type='cleaned')
analyzer = StatisticalAnalyzer()

print("="*60)
print("STATISTICAL ANALYSIS REPORT")
print("="*60)

# 1. Test normality for each country
print("\n1. NORMALITY TESTS (GHI)")
print("-"*60)
for country, df in all_data.items():
    result = analyzer.test_normality(df['GHI'].sample(5000))
    print(f"{country.capitalize()}: {result['interpretation']}")

# 2. Compare means across countries
print("\n2. COMPARISON ACROSS COUNTRIES (ANOVA)")
print("-"*60)
data_dict = {k.capitalize(): v['GHI'] for k, v in all_data.items()}
result = compare_groups(data_dict, parametric=True)
print(result['interpretation'])
for group, stats in result['group_statistics'].items():
    print(f"  {group}: μ={stats['mean']:.2f}, σ={stats['std']:.2f}")

# 3. Pairwise comparisons
print("\n3. PAIRWISE T-TESTS")
print("-"*60)
countries = list(all_data.keys())
for i in range(len(countries)):
    for j in range(i+1, len(countries)):
        c1, c2 = countries[i], countries[j]
        result = analyzer.ttest_independent(
            all_data[c1]['GHI'],
            all_data[c2]['GHI']
        )
        print(f"{c1.capitalize()} vs {c2.capitalize()}: {result['interpretation']}")

# 4. Correlation analysis
print("\n4. CORRELATION ANALYSIS (GHI with Weather Variables)")
print("-"*60)
df_sample = all_data['benin'].sample(5000)
weather_vars = ['Tamb', 'RH', 'WS']
for var in weather_vars:
    result = quick_correlation_test(df_sample['GHI'], df_sample[var])
    print(f"GHI vs {var}: {result['interpretation']}")

print("\n" + "="*60)
```

## Example 12: Testing Assumptions

```python
# Before running parametric tests, check assumptions

# 1. Normality (Shapiro-Wilk)
normality_results = {}
for country, df in all_data.items():
    result = analyzer.test_normality(df['GHI'].sample(5000))
    normality_results[country] = result['is_normal']

print("Normality check:", normality_results)

# 2. Homogeneity of variance (Levene's test)
from scipy import stats as sp_stats
benin_ghi = all_data['benin']['GHI'].dropna()
togo_ghi = all_data['togo']['GHI'].dropna()
stat, p = sp_stats.levene(benin_ghi, togo_ghi)
print(f"Equal variances: {p > 0.05} (p={p:.4f})")

# Choose appropriate test based on assumptions
if all(normality_results.values()) and p > 0.05:
    print("Using parametric tests (t-test/ANOVA)")
    result = analyzer.ttest_independent(benin_ghi, togo_ghi, equal_var=True)
else:
    print("Using non-parametric tests (Mann-Whitney/Kruskal-Wallis)")
    result = analyzer.mann_whitney_u(benin_ghi, togo_ghi)

print(result['interpretation'])
```

## Available Tests

| Test               | Parametric | Purpose           | Function                 |
| ------------------ | ---------- | ----------------- | ------------------------ |
| Shapiro-Wilk       | -          | Test normality    | `test_normality()`       |
| Pearson/Spearman   | Varies     | Correlation       | `correlation_analysis()` |
| Independent t-test | Yes        | Compare 2 groups  | `ttest_independent()`    |
| Mann-Whitney U     | No         | Compare 2 groups  | `mann_whitney_u()`       |
| One-way ANOVA      | Yes        | Compare 3+ groups | `anova_oneway()`         |
| Kruskal-Wallis     | No         | Compare 3+ groups | `kruskal_wallis()`       |

## When to Use Which Test

### Normality Tests

-   **Use**: Before choosing parametric vs non-parametric tests
-   **Shapiro-Wilk**: Most powerful for n < 5000
-   **Anderson-Darling**: More sensitive to tail deviations

### Correlation

-   **Pearson**: Linear relationships, normal data
-   **Spearman**: Monotonic relationships, ordinal or non-normal data
-   **Kendall**: Small samples, many tied ranks

### Two-Group Comparisons

-   **Independent t-test**: Normal data, equal/unequal variances
-   **Mann-Whitney U**: Non-normal data, ordinal data

### Multiple-Group Comparisons

-   **One-way ANOVA**: Normal data, equal variances
-   **Kruskal-Wallis**: Non-normal data, unequal variances

## Tips

1. **Always check assumptions** before parametric tests
2. **Use adequate sample sizes** for power
3. **Correct for multiple comparisons** (Bonferroni, FDR)
4. **Report effect sizes** along with p-values
5. **Consider practical significance** not just statistical
6. **Use non-parametric tests** when assumptions violated
7. **Visualize distributions** before testing

## Integration with Other Modules

```python
# Complete workflow: Load → Clean → Analyze → Visualize
from utils import load_country, quick_clean
from analysis import StatisticalAnalyzer
from utils.visualization import SolarVisualizer

# Load and clean
df = load_country('benin', data_type='raw')
cleaned_df, report = quick_clean(df)

# Statistical analysis
analyzer = StatisticalAnalyzer()
norm_result = analyzer.test_normality(cleaned_df['GHI'])
print(norm_result['interpretation'])

# Visualize
viz = SolarVisualizer()
fig = viz.plot_distribution(cleaned_df, 'GHI', kind='hist')
plt.title(f"GHI Distribution - {norm_result['interpretation']}")
plt.show()
```

## Common Patterns

### Pattern 1: Compare Countries

```python
data = {k: v['GHI'] for k, v in load_all(data_type='cleaned').items()}
result = compare_groups(data, parametric=True)
```

### Pattern 2: Test Correlation

```python
result = quick_correlation_test(df['GHI'], df['Tamb'])
```

### Pattern 3: Check Normality

```python
analyzer = StatisticalAnalyzer()
result = analyzer.test_normality(df['GHI'])
```
