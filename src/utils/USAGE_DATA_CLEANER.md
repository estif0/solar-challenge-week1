# Data Cleaner Usage Guide

This guide demonstrates how to use the data cleaning utilities for solar radiation data.

## Quick Start

```python
import sys
sys.path.insert(0, '../src')

from utils.data_loader import load_country
from utils.data_cleaner import DataCleaner, quick_clean, get_data_quality_report
```

## Example 1: Quick Data Quality Assessment

```python
from utils.data_loader import load_country
from utils.data_cleaner import get_data_quality_report, detect_missing_summary

# Load data
df = load_country('benin', data_type='raw')

# Get comprehensive quality report
report = get_data_quality_report(df)
print(f"Total rows: {report['total_rows']}")
print(f"Duplicates: {report['duplicate_rows']}")
print(f"Missing values in: {list(report['missing_values'].keys())}")
print(f"Negative values in: {list(report['negative_values'].keys())}")

# Get detailed missing values summary
missing_summary = detect_missing_summary(df)
print(missing_summary)
```

## Example 2: Quick Clean (Recommended for Most Cases)

The `quick_clean()` function applies a standard cleaning pipeline:

```python
from utils.data_cleaner import quick_clean

# Apply standard cleaning
cleaned_df, report = quick_clean(df)

print(report)
print(f"\nOriginal rows: {len(df)}")
print(f"Cleaned rows: {len(cleaned_df)}")
```

## Example 3: Custom Cleaning with DataCleaner Class

For more control, use the `DataCleaner` class:

```python
from utils.data_cleaner import DataCleaner

# Initialize cleaner
cleaner = DataCleaner(df)

# Step 1: Remove duplicates
cleaner.remove_duplicates(subset=['Timestamp'])

# Step 2: Clean negative values (solar radiation shouldn't be negative)
cleaner.clean_negative_values(['GHI', 'DNI', 'DHI'], strategy='zero')

# Step 3: Handle outliers
cleaner.handle_outliers('GHI', method='zscore', threshold=3.0, strategy='nan')
cleaner.handle_outliers('Tamb', method='iqr', multiplier=1.5, strategy='clip')

# Step 4: Handle missing values
cleaner.handle_missing_values('GHI', strategy='interpolate')
cleaner.handle_missing_values('Tamb', strategy='forward_fill')

# Get results
cleaned_df = cleaner.get_cleaned_data()
print(cleaner.get_cleaning_report())
```

## Example 4: Detecting Outliers Only

```python
from utils.data_cleaner import DataCleaner

cleaner = DataCleaner(df)

# Detect outliers using Z-score (doesn't modify data)
zscore_outliers = cleaner.detect_outliers_zscore('GHI', threshold=3.0)
print(f"Z-score outliers: {zscore_outliers.sum()}")

# Detect outliers using IQR
iqr_outliers = cleaner.detect_outliers_iqr('GHI', multiplier=1.5)
print(f"IQR outliers: {iqr_outliers.sum()}")

# View the outlier values
print(df[zscore_outliers]['GHI'].describe())
```

## Example 5: Method Chaining

The `DataCleaner` class supports method chaining for clean, readable code:

```python
from utils.data_cleaner import DataCleaner

cleaned_df = (DataCleaner(df)
    .remove_duplicates(subset=['Timestamp'])
    .clean_negative_values(['GHI', 'DNI', 'DHI'], strategy='zero')
    .handle_outliers('GHI', method='zscore', threshold=3.5, strategy='nan')
    .handle_outliers('Tamb', method='zscore', threshold=3.5, strategy='nan')
    .handle_missing_values('GHI', strategy='interpolate')
    .handle_missing_values('Tamb', strategy='interpolate')
    .get_cleaned_data()
)
```

## Example 6: Cleaning All Countries

```python
from utils.data_loader import load_all
from utils.data_cleaner import quick_clean

# Load all country data
all_data = load_all(data_type='raw')

# Clean each country's data
cleaned_data = {}
for country, df in all_data.items():
    cleaned_df, report = quick_clean(df)
    cleaned_data[country] = cleaned_df
    print(f"\n{country.upper()} Cleaning Report:")
    print(report)
```

## Outlier Detection Methods

### Z-Score Method

-   Good for normally distributed data
-   Threshold typically 2.5-3.5
-   `threshold=3.0` means values >3 standard deviations from mean

```python
cleaner.handle_outliers('GHI', method='zscore', threshold=3.0, strategy='nan')
```

### IQR Method

-   More robust to extreme values
-   `multiplier=1.5` for outliers, `3.0` for extreme outliers
-   Based on interquartile range

```python
cleaner.handle_outliers('Tamb', method='iqr', multiplier=1.5, strategy='clip')
```

## Missing Value Strategies

| Strategy        | Description           | Best For                       |
| --------------- | --------------------- | ------------------------------ |
| `drop`          | Remove rows           | Small amounts of missing data  |
| `forward_fill`  | Use previous value    | Time series with slow changes  |
| `backward_fill` | Use next value        | Time series gaps               |
| `interpolate`   | Linear interpolation  | Time series data (recommended) |
| `mean`          | Fill with column mean | Random missing values          |
| `median`        | Fill with median      | Skewed distributions           |
| `zero`          | Fill with 0           | Specific domain requirements   |

## Outlier Handling Strategies

| Strategy | Description         | Best For                                |
| -------- | ------------------- | --------------------------------------- |
| `nan`    | Replace with NaN    | Will handle later with interpolation    |
| `median` | Replace with median | Conservative approach                   |
| `mean`   | Replace with mean   | Normally distributed data               |
| `clip`   | Clip to boundaries  | Preserving data while limiting extremes |

## Negative Value Strategies

For solar radiation data (GHI, DNI, DHI):

| Strategy | Description         | Recommended                |
| -------- | ------------------- | -------------------------- |
| `zero`   | Replace with 0      | ✓ Yes (nighttime readings) |
| `nan`    | Replace with NaN    | If will interpolate later  |
| `abs`    | Take absolute value | Not recommended            |

## Complete Cleaning Pipeline Example

```python
from utils.data_loader import load_country
from utils.data_cleaner import DataCleaner

# Load data
df = load_country('benin', data_type='raw')

# Define cleaning pipeline
cleaner = DataCleaner(df)

# Execute pipeline
cleaned_df = (cleaner
    # 1. Remove duplicates
    .remove_duplicates(subset=['Timestamp'])

    # 2. Clean negative radiation values
    .clean_negative_values(['GHI', 'DNI', 'DHI'], strategy='zero')

    # 3. Handle outliers in radiation data
    .handle_outliers('GHI', method='zscore', threshold=3.5, strategy='nan')
    .handle_outliers('DNI', method='zscore', threshold=3.5, strategy='nan')
    .handle_outliers('DHI', method='zscore', threshold=3.5, strategy='nan')

    # 4. Handle outliers in meteorological data
    .handle_outliers('Tamb', method='zscore', threshold=4.0, strategy='clip')
    .handle_outliers('RH', method='zscore', threshold=4.0, strategy='clip')
    .handle_outliers('WS', method='iqr', multiplier=2.0, strategy='clip')

    # 5. Interpolate missing values
    .handle_missing_values('GHI', strategy='interpolate')
    .handle_missing_values('DNI', strategy='interpolate')
    .handle_missing_values('DHI', strategy='interpolate')
    .handle_missing_values('Tamb', strategy='interpolate')
    .handle_missing_values('RH', strategy='interpolate')
    .handle_missing_values('WS', strategy='interpolate')

    .get_cleaned_data()
)

# Print report
print(cleaner.get_cleaning_report())

# Save cleaned data
# cleaned_df.to_csv('../data/cleaned/benin_cleaned.csv', index=False)
```

## Tips

1. **Always check data quality first** using `get_data_quality_report()`
2. **Use method chaining** for readable pipelines
3. **Clean negatives before outliers** - negatives are definitely invalid
4. **Be conservative with outlier thresholds** - start with 3.5 or 4.0
5. **Prefer interpolation for time series** missing values
6. **Document your cleaning decisions** in notebooks
7. **Save cleaning reports** for reproducibility

## Integration with Data Loader

```python
# Seamless integration
from utils import load_country, quick_clean

# Load and clean in two lines
df = load_country('togo', data_type='raw')
cleaned_df, report = quick_clean(df)
```
