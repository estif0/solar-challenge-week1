# Solar Metrics Usage Guide

This guide demonstrates how to use the solar metrics calculation utilities for solar radiation analysis.

## Quick Start

```python
import sys
sys.path.insert(0, '../src')

from utils.data_loader import load_country, load_all
from analysis.solar_metrics import (
    SolarMetrics,
    calculate_clearness_index,
    calculate_diffuse_fraction,
    categorize_sky_condition,
    aggregate_daily_energy
)
```

## Example 1: Basic Solar Metrics Calculator

```python
from analysis.solar_metrics import SolarMetrics

# Initialize calculator with location parameters
metrics = SolarMetrics(
    latitude=9.3,     # Benin latitude
    longitude=2.6,    # Benin longitude
    timezone='UTC'
)

# Load data
df = load_country('benin', data_type='cleaned')
```

## Example 2: Calculate Clearness Index (Kt)

```python
# Add clearness index to DataFrame
df = metrics.add_clearness_index(df)
print(df[['GHI', 'clearness_index']].head())

# Or calculate directly
from analysis.solar_metrics import calculate_clearness_index

kt = calculate_clearness_index(
    ghi=df['GHI'],
    extraterrestrial_irradiance=1361  # Solar constant
)
print(f"Average Kt: {kt.mean():.3f}")

# Analyze clearness by time of day
df['Hour'] = df['Timestamp'].dt.hour
daytime = df[(df['Hour'] >= 6) & (df['Hour'] <= 18)]
print(f"Daytime average Kt: {daytime['clearness_index'].mean():.3f}")
```

## Example 3: Calculate Diffuse Fraction (Kd)

```python
# Add diffuse fraction
df = metrics.add_diffuse_fraction(df)
print(df[['GHI', 'DHI', 'diffuse_fraction']].head())

# Or calculate directly
from analysis.solar_metrics import calculate_diffuse_fraction

kd = calculate_diffuse_fraction(
    dhi=df['DHI'],
    ghi=df['GHI']
)
print(f"Average Kd: {kd.mean():.3f}")

# Analyze relationship between Kt and Kd
import matplotlib.pyplot as plt
plt.scatter(df['clearness_index'], df['diffuse_fraction'], alpha=0.1, s=1)
plt.xlabel('Clearness Index (Kt)')
plt.ylabel('Diffuse Fraction (Kd)')
plt.title('Kt vs Kd Relationship')
plt.show()
```

## Example 4: Sky Condition Classification

```python
# Classify sky conditions
df = metrics.classify_sky_condition(df)
print(df['sky_condition'].value_counts())

# Or use convenience function
from analysis.solar_metrics import categorize_sky_condition

sky_category = categorize_sky_condition(df['clearness_index'])
print(sky_category.value_counts(normalize=True))

# Analyze GHI by sky condition
sky_analysis = df.groupby('sky_condition')['GHI'].agg(['mean', 'std', 'count'])
print(sky_analysis)
```

## Example 5: Calculate Daily Energy

```python
# Calculate daily energy yield
from analysis.solar_metrics import aggregate_daily_energy

daily_energy = aggregate_daily_energy(
    df,
    ghi_column='GHI',
    time_column='Timestamp'
)

print(daily_energy.head())
print(f"\nAverage daily energy: {daily_energy['daily_energy_kwh_m2'].mean():.2f} kWh/m²")

# Plot daily energy over time
import matplotlib.pyplot as plt
plt.figure(figsize=(14, 6))
plt.plot(daily_energy['date'], daily_energy['daily_energy_kwh_m2'])
plt.xlabel('Date')
plt.ylabel('Daily Energy (kWh/m²)')
plt.title('Daily Solar Energy Yield')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Example 6: Compare Solar Metrics Across Countries

```python
from analysis.solar_metrics import compare_solar_metrics

# Load all countries
all_data = load_all(data_type='cleaned')

# Compare metrics
comparison = compare_solar_metrics(
    all_data,
    metrics_list=['GHI', 'DNI', 'DHI', 'clearness_index']
)

print(comparison)

# Visualize comparison
import seaborn as sns
comparison_melted = comparison.reset_index().melt(id_vars='index', var_name='Country', value_name='Value')
comparison_melted.rename(columns={'index': 'Metric'}, inplace=True)

plt.figure(figsize=(12, 6))
sns.barplot(data=comparison_melted, x='Metric', y='Value', hue='Country')
plt.title('Solar Metrics Comparison Across Countries')
plt.ylabel('Mean Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Example 7: Add All Solar Metrics at Once

```python
# Add all metrics to DataFrame
df_enriched = metrics.add_all_metrics(df)

print("Added columns:")
print([col for col in df_enriched.columns if col not in df.columns])

# Columns added:
# - clearness_index
# - diffuse_fraction
# - sky_condition
```

## Example 8: Daytime vs Nighttime Analysis

```python
# Filter daytime data (GHI > 0)
daytime = df[df['GHI'] > 0].copy()
nighttime = df[df['GHI'] <= 0].copy()

print(f"Daytime records: {len(daytime):,}")
print(f"Nighttime records: {len(nighttime):,}")

# Calculate metrics only for daytime
daytime = metrics.add_all_metrics(daytime)

# Analyze daytime clearness
print("\nDaytime Sky Conditions:")
print(daytime['sky_condition'].value_counts(normalize=True))

# Average metrics during daytime
print("\nDaytime Averages:")
print(f"GHI: {daytime['GHI'].mean():.2f} W/m²")
print(f"Clearness Index: {daytime['clearness_index'].mean():.3f}")
print(f"Diffuse Fraction: {daytime['diffuse_fraction'].mean():.3f}")
```

## Example 9: Monthly Solar Metrics Analysis

```python
# Add month column
df['Month'] = df['Timestamp'].dt.month
df['MonthName'] = df['Timestamp'].dt.strftime('%B')

# Add metrics
df = metrics.add_all_metrics(df)

# Monthly aggregation
monthly_metrics = df[df['GHI'] > 0].groupby('MonthName').agg({
    'GHI': 'mean',
    'DNI': 'mean',
    'DHI': 'mean',
    'clearness_index': 'mean',
    'diffuse_fraction': 'mean'
}).round(2)

print(monthly_metrics)

# Reorder by month
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
monthly_metrics = monthly_metrics.reindex([m for m in month_order if m in monthly_metrics.index])

# Plot monthly patterns
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

monthly_metrics['GHI'].plot(ax=axes[0,0], marker='o', title='Monthly Average GHI')
axes[0,0].set_ylabel('GHI (W/m²)')

monthly_metrics['clearness_index'].plot(ax=axes[0,1], marker='o', title='Monthly Average Clearness Index')
axes[0,1].set_ylabel('Kt')

monthly_metrics['diffuse_fraction'].plot(ax=axes[1,0], marker='o', title='Monthly Average Diffuse Fraction')
axes[1,0].set_ylabel('Kd')

# Sky condition distribution by month
sky_by_month = df[df['GHI'] > 0].groupby(['MonthName', 'sky_condition']).size().unstack(fill_value=0)
sky_by_month = sky_by_month.reindex([m for m in month_order if m in sky_by_month.index])
sky_by_month.plot(kind='bar', stacked=True, ax=axes[1,1], title='Sky Conditions by Month')
axes[1,1].set_ylabel('Count')

plt.tight_layout()
plt.show()
```

## Example 10: Solar Resource Assessment

```python
from analysis.solar_metrics import SolarMetrics
import numpy as np

# Calculate annual solar resource
df = load_country('benin', data_type='cleaned')
metrics = SolarMetrics(latitude=9.3, longitude=2.6)
df = metrics.add_all_metrics(df)

# Daily energy
daily = aggregate_daily_energy(df)

print("="*60)
print("SOLAR RESOURCE ASSESSMENT")
print("="*60)

# Annual metrics
print(f"\nAnnual GHI Sum: {df[df['GHI'] > 0]['GHI'].sum() / 1000:.2f} kWh/m²")
print(f"Annual Average GHI: {df[df['GHI'] > 0]['GHI'].mean():.2f} W/m²")
print(f"Peak GHI: {df['GHI'].max():.2f} W/m²")

# Daily averages
print(f"\nAverage Daily Energy: {daily['daily_energy_kwh_m2'].mean():.2f} kWh/m²/day")
print(f"Max Daily Energy: {daily['daily_energy_kwh_m2'].max():.2f} kWh/m²/day")
print(f"Min Daily Energy: {daily['daily_energy_kwh_m2'].min():.2f} kWh/m²/day")

# Clearness statistics
print(f"\nAverage Clearness Index: {df[df['GHI'] > 0]['clearness_index'].mean():.3f}")
print(f"Average Diffuse Fraction: {df[df['GHI'] > 0]['diffuse_fraction'].mean():.3f}")

# Sky conditions
print("\nSky Condition Distribution:")
sky_dist = df[df['GHI'] > 0]['sky_condition'].value_counts(normalize=True) * 100
for condition, percent in sky_dist.items():
    print(f"  {condition}: {percent:.1f}%")

# Seasonal analysis
df['Season'] = df['Timestamp'].dt.month % 12 // 3 + 1
season_names = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
df['SeasonName'] = df['Season'].map(season_names)

print("\nSeasonal Analysis:")
seasonal = df[df['GHI'] > 0].groupby('SeasonName')['GHI'].mean()
for season, ghi in seasonal.items():
    print(f"  {season}: {ghi:.2f} W/m²")

print("="*60)
```

## Example 11: Performance Comparison

```python
# Compare solar performance across locations
all_data = load_all(data_type='cleaned')

performance = {}
for country, df in all_data.items():
    # Calculate metrics
    lat_dict = {'benin': 9.3, 'togo': 10.2, 'sierraleone': 9.0}
    lon_dict = {'benin': 2.6, 'togo': 0.2, 'sierraleone': -12.1}

    metrics = SolarMetrics(
        latitude=lat_dict[country],
        longitude=lon_dict[country]
    )
    df = metrics.add_all_metrics(df)

    # Filter daytime
    daytime = df[df['GHI'] > 0]

    performance[country] = {
        'avg_ghi': daytime['GHI'].mean(),
        'avg_dni': daytime['DNI'].mean(),
        'avg_dhi': daytime['DHI'].mean(),
        'clearness': daytime['clearness_index'].mean(),
        'diffuse_frac': daytime['diffuse_fraction'].mean(),
        'clear_days_pct': (daytime['sky_condition'] == 'Clear').sum() / len(daytime) * 100
    }

# Display comparison
import pandas as pd
perf_df = pd.DataFrame(performance).T
print(perf_df.round(2))

# Rank countries by solar resource
perf_df['rank'] = perf_df['avg_ghi'].rank(ascending=False)
print("\nRanking by Average GHI:")
print(perf_df.sort_values('rank')[['avg_ghi', 'clearness', 'clear_days_pct']])
```

## Example 12: Complete Analysis Workflow

```python
from utils import load_country, quick_clean
from analysis import SolarMetrics
from utils.visualization import SolarVisualizer

# 1. Load and clean data
df = load_country('benin', data_type='raw')
df_clean, report = quick_clean(df)

# 2. Calculate solar metrics
metrics = SolarMetrics(latitude=9.3, longitude=2.6)
df_clean = metrics.add_all_metrics(df_clean)

# 3. Analyze
daytime = df_clean[df_clean['GHI'] > 0]
print(f"Average Clearness Index: {daytime['clearness_index'].mean():.3f}")
print(f"Sky Conditions:\n{daytime['sky_condition'].value_counts()}")

# 4. Visualize
viz = SolarVisualizer()

# Time series of clearness index
fig = viz.plot_time_series(
    daytime.head(2000),
    'clearness_index',
    title='Clearness Index Over Time'
)
plt.show()

# Distribution of clearness index
fig = viz.plot_distribution(daytime, 'clearness_index', kind='hist')
plt.show()

# Sky condition comparison
sky_stats = daytime.groupby('sky_condition')['GHI'].agg(['mean', 'count'])
print(sky_stats)
```

## Available Metrics

| Metric                | Formula                | Range  | Description                     |
| --------------------- | ---------------------- | ------ | ------------------------------- |
| Clearness Index (Kt)  | GHI / Extraterrestrial | 0-1    | Atmospheric transparency        |
| Diffuse Fraction (Kd) | DHI / GHI              | 0-1    | Proportion of diffuse radiation |
| Daily Energy          | ∫GHI dt                | kWh/m² | Integrated daily radiation      |

## Sky Condition Classifications

| Condition     | Clearness Index (Kt) Range |
| ------------- | -------------------------- |
| Overcast      | Kt < 0.3                   |
| Partly Cloudy | 0.3 ≤ Kt < 0.65            |
| Clear         | Kt ≥ 0.65                  |

## Tips

1. **Filter daytime data** (GHI > 0) before calculating clearness metrics
2. **Handle missing values** in DNI/DHI before calculations
3. **Consider seasonal patterns** in solar metrics
4. **Use appropriate location parameters** (latitude, longitude)
5. **Aggregate to daily/monthly** for cleaner patterns
6. **Compare across locations** for resource assessment
7. **Validate extreme values** (Kt > 1 indicates issues)

## Common Patterns

### Pattern 1: Add All Metrics

```python
metrics = SolarMetrics(latitude=9.3, longitude=2.6)
df = metrics.add_all_metrics(df)
```

### Pattern 2: Daily Energy Calculation

```python
daily = aggregate_daily_energy(df, 'GHI', 'Timestamp')
```

### Pattern 3: Sky Condition Analysis

```python
df = metrics.classify_sky_condition(df)
distribution = df['sky_condition'].value_counts(normalize=True)
```

### Pattern 4: Cross-Country Comparison

```python
comparison = compare_solar_metrics(all_data, ['GHI', 'DNI', 'clearness_index'])
```

## Integration with Statistical Tests

```python
from analysis import SolarMetrics, StatisticalAnalyzer

# Calculate metrics
metrics = SolarMetrics(latitude=9.3, longitude=2.6)
df = metrics.add_all_metrics(df)

# Test if clearness index differs by sky condition
analyzer = StatisticalAnalyzer()
clear = df[df['sky_condition'] == 'Clear']['clearness_index']
cloudy = df[df['sky_condition'] == 'Partly Cloudy']['clearness_index']
overcast = df[df['sky_condition'] == 'Overcast']['clearness_index']

result = analyzer.anova_oneway(
    clear, cloudy, overcast,
    group_names=['Clear', 'Partly Cloudy', 'Overcast']
)
print(result['interpretation'])
```
