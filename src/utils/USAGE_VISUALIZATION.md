# Visualization Utilities Usage Guide

This guide demonstrates how to use the visualization utilities for solar radiation data.

## Quick Start

```python
import sys
sys.path.insert(0, '../src')

from utils.data_loader import load_country, load_all
from utils.visualization import SolarVisualizer, quick_time_series, quick_distribution
import matplotlib.pyplot as plt
```

## Example 1: Quick Time Series Plot

```python
from utils import load_country, quick_time_series

# Load data
df = load_country('benin', data_type='cleaned')

# Create quick time series plot
fig = quick_time_series(df, ['GHI', 'DNI', 'DHI'], title='Solar Radiation - Benin')
plt.show()
```

## Example 2: Using SolarVisualizer Class

```python
from utils.visualization import SolarVisualizer

# Initialize visualizer
viz = SolarVisualizer(style='whitegrid', palette='husl')

# Create various plots
fig1 = viz.plot_time_series(df, ['GHI', 'DNI'], title='Solar Irradiance')
fig2 = viz.plot_distribution(df, 'GHI', kind='hist')
fig3 = viz.plot_correlation_heatmap(df, columns=['GHI', 'DNI', 'DHI', 'Tamb'])
```

## Example 3: Distribution Plots

```python
viz = SolarVisualizer()

# Histogram
fig = viz.plot_distribution(df, 'GHI', kind='hist', bins=50)
plt.show()

# KDE plot
fig = viz.plot_distribution(df, 'Tamb', kind='kde')
plt.show()

# Box plot
fig = viz.plot_distribution(df, 'WS', kind='box')
plt.show()

# Violin plot
fig = viz.plot_distribution(df, 'RH', kind='violin')
plt.show()
```

## Example 4: Correlation Analysis

```python
# Full correlation matrix
fig = viz.plot_correlation_heatmap(df)
plt.show()

# Specific columns
radiation_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB']
fig = viz.plot_correlation_heatmap(df, columns=radiation_cols, method='pearson')
plt.show()

# Different correlation methods
fig = viz.plot_correlation_heatmap(df, columns=radiation_cols, method='spearman')
plt.show()
```

## Example 5: Time-Based Patterns

```python
# Daily pattern (hourly aggregation)
fig = viz.plot_daily_pattern(df, 'GHI', agg_func='mean')
plt.show()

# Monthly pattern
fig = viz.plot_monthly_pattern(df, 'GHI', agg_func='mean')
plt.show()

# Different aggregations
fig = viz.plot_daily_pattern(df, 'Tamb', agg_func='max', title='Max Temperature by Hour')
plt.show()
```

## Example 6: Comparing Countries

```python
from utils import load_all

# Load all countries
all_data = load_all(data_type='cleaned')

# Compare mean GHI across countries
fig = viz.plot_comparison(all_data, 'GHI', agg_func='mean', kind='bar')
plt.show()

# Compare with different aggregation
fig = viz.plot_comparison(all_data, 'Tamb', agg_func='median', kind='bar')
plt.show()

# Horizontal bar chart
fig = viz.plot_comparison(all_data, 'WS', agg_func='mean', kind='barh')
plt.show()
```

## Example 7: Box Plot Comparisons

```python
# Compare distributions across countries
fig = viz.plot_box_comparison(all_data, 'GHI', title='GHI Distribution by Country')
plt.show()

# Compare other variables
fig = viz.plot_box_comparison(all_data, 'Tamb', title='Temperature Distribution')
plt.show()
```

## Example 8: Scatter Plots

```python
# Simple scatter
fig = viz.plot_scatter(df, 'Tamb', 'GHI', title='GHI vs Temperature')
plt.show()

# Scatter with color grouping
df['Hour'] = df['Timestamp'].dt.hour
df['Period'] = df['Hour'].apply(lambda x: 'Morning' if 6 <= x < 12 else 'Afternoon' if 12 <= x < 18 else 'Other')
fig = viz.plot_scatter(df, 'Tamb', 'GHI', hue_column='Period')
plt.show()
```

## Example 9: Custom Styling

```python
# Initialize with custom style
viz = SolarVisualizer(style='darkgrid', palette='Set2')

# Or change matplotlib settings directly
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 8)
plt.rcParams['font.size'] = 12

fig = viz.plot_time_series(df, 'GHI')
plt.show()
```

## Example 10: Saving Plots

```python
# Create and save plot
fig = viz.plot_time_series(df, ['GHI', 'DNI', 'DHI'])
fig.savefig('solar_radiation.png', dpi=300, bbox_inches='tight')
plt.close()

# Save multiple plots
plots = [
    ('time_series', viz.plot_time_series(df, 'GHI')),
    ('distribution', viz.plot_distribution(df, 'GHI')),
    ('daily_pattern', viz.plot_daily_pattern(df, 'GHI'))
]

for name, fig in plots:
    fig.savefig(f'{name}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
```

## Example 11: Multi-Panel Figures

```python
import matplotlib.pyplot as plt

# Create custom multi-panel layout
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Manually plot on each axis
df['Hour'] = df['Timestamp'].dt.hour
hourly = df.groupby('Hour')['GHI'].mean()

axes[0, 0].plot(hourly.index, hourly.values)
axes[0, 0].set_title('Daily Pattern - GHI')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].hist(df['GHI'].dropna(), bins=50)
axes[0, 1].set_title('GHI Distribution')

axes[1, 0].scatter(df['Tamb'], df['GHI'], alpha=0.5, s=10)
axes[1, 0].set_xlabel('Temperature')
axes[1, 0].set_ylabel('GHI')
axes[1, 0].set_title('GHI vs Temperature')

axes[1, 1].boxplot([df['GHI'].dropna()])
axes[1, 1].set_title('GHI Box Plot')

plt.tight_layout()
plt.savefig('multi_panel.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Example 12: Complete Analysis Workflow

```python
from utils import load_country, SolarVisualizer
import matplotlib.pyplot as plt

# Load data
df = load_country('benin', data_type='cleaned')
viz = SolarVisualizer()

# 1. Overview time series
print("Creating time series overview...")
fig = viz.plot_time_series(
    df.head(5000),  # First week
    ['GHI', 'DNI', 'DHI'],
    title='Solar Radiation Components - First Week'
)
plt.savefig('01_overview.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Distributions
print("Creating distribution plots...")
for col in ['GHI', 'DNI', 'DHI', 'Tamb']:
    fig = viz.plot_distribution(df, col, kind='hist')
    plt.savefig(f'02_dist_{col}.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. Daily patterns
print("Creating daily pattern plots...")
for col in ['GHI', 'DNI', 'DHI']:
    fig = viz.plot_daily_pattern(df, col)
    plt.savefig(f'03_daily_{col}.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. Monthly patterns
print("Creating monthly pattern plots...")
fig = viz.plot_monthly_pattern(df, 'GHI')
plt.savefig('04_monthly_GHI.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Correlations
print("Creating correlation heatmap...")
fig = viz.plot_correlation_heatmap(
    df,
    columns=['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS'],
    method='pearson'
)
plt.savefig('05_correlations.png', dpi=300, bbox_inches='tight')
plt.close()

print("Analysis complete! All plots saved.")
```

## Available Plot Types

| Function                   | Description              | Key Parameters       |
| -------------------------- | ------------------------ | -------------------- |
| `plot_time_series`         | Line plot over time      | columns, time_column |
| `plot_distribution`        | Histogram/KDE/Box/Violin | kind, bins           |
| `plot_correlation_heatmap` | Correlation matrix       | method, annot        |
| `plot_comparison`          | Compare across groups    | agg_func, kind       |
| `plot_box_comparison`      | Box plots for groups     | -                    |
| `plot_monthly_pattern`     | Monthly aggregation      | agg_func             |
| `plot_daily_pattern`       | Hourly aggregation       | agg_func             |
| `plot_scatter`             | Scatter plot             | hue_column           |

## Customization Options

### Styles

-   `whitegrid`, `darkgrid`, `white`, `dark`, `ticks`

### Color Palettes

-   `husl`, `Set1`, `Set2`, `Set3`, `Paired`, `tab10`, `coolwarm`

### Aggregation Functions

-   `mean`, `median`, `sum`, `std`, `min`, `max`, `count`

### Correlation Methods

-   `pearson`, `spearman`, `kendall`

## Tips

1. **Use appropriate plot types** for your data
2. **Sample large datasets** for faster plotting
3. **Save plots** with high DPI (300) for presentations
4. **Close figures** after saving to free memory
5. **Use tight_layout()** for better spacing
6. **Customize titles and labels** for clarity
7. **Consider color-blind friendly palettes**

## Integration with Other Utilities

```python
# Complete workflow: Load → Clean → Visualize
from utils import load_country, quick_clean, SolarVisualizer

# Load and clean
df = load_country('benin', data_type='raw')
cleaned_df, report = quick_clean(df.head(10000))

# Visualize
viz = SolarVisualizer()
fig = viz.plot_time_series(cleaned_df, ['GHI', 'DNI', 'DHI'])
plt.show()
```
