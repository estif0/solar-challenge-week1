# Data Loader Usage Examples

This document provides examples of how to use the `data_loader` utility module.

## Quick Start

```python
# Add src to path (if running from notebooks)
import sys
sys.path.insert(0, '../src')

# Import the data loader
from utils.data_loader import DataLoader, load_country, load_all
```

## Example 1: Load Single Country Data

```python
from utils.data_loader import load_country

# Load raw data
benin_raw = load_country('benin', data_type='raw')

# Load cleaned data
benin_cleaned = load_country('benin', data_type='cleaned')

print(f"Loaded {len(benin_cleaned)} rows")
print(benin_cleaned.head())
```

## Example 2: Using DataLoader Class

```python
from utils.data_loader import DataLoader

# Initialize loader
loader = DataLoader()

# Load specific country
togo_data = loader.load_country_data('togo', data_type='cleaned')

# Load specific file
benin_data = loader.load_file('benin_cleaned.csv', data_type='cleaned')
```

## Example 3: Load All Countries

```python
from utils.data_loader import load_all

# Get dictionary of all country data
all_countries = load_all(data_type='cleaned')

# Access individual countries
benin_df = all_countries['benin']
togo_df = all_countries['togo']
sierraleone_df = all_countries['sierraleone']

# Iterate through all
for country, df in all_countries.items():
    print(f"{country}: {len(df)} rows")
```

## Example 4: Working with Datetime

```python
from utils.data_loader import load_country

# Data is automatically loaded with parsed datetime
df = load_country('benin', data_type='cleaned')

# Timestamp is already datetime type
print(df['Timestamp'].dtype)  # datetime64[ns]

# You can immediately use datetime operations
df['Month'] = df['Timestamp'].dt.month
df['Hour'] = df['Timestamp'].dt.hour
df['Date'] = df['Timestamp'].dt.date

# Filter by date range
import pandas as pd
start_date = pd.Timestamp('2021-11-01')
end_date = pd.Timestamp('2021-11-30')
november_data = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]
```

## Example 5: Load Processed/Dashboard Data

```python
from utils.data_loader import DataLoader

loader = DataLoader()

# Load processed dashboard data
monthly = loader.load_file('dashboard_monthly_data.csv', data_type='processed')
patterns = loader.load_file('dashboard_daily_patterns.csv', data_type='processed')
comparison = loader.load_file('dashboard_comparison.csv', data_type='processed')
```

## Example 6: Custom Data Directory

```python
from utils.data_loader import DataLoader

# Use custom data directory
loader = DataLoader(data_dir='/custom/path/to/data')
df = loader.load_country_data('benin')
```

## Example 7: Additional pandas Arguments

```python
from utils.data_loader import load_country

# Pass additional arguments to pd.read_csv()
df = load_country('togo', data_type='raw', nrows=1000)  # Only first 1000 rows
df = load_country('benin', data_type='cleaned', usecols=['Timestamp', 'GHI', 'DNI'])
```

## Example 8: Error Handling

```python
from utils.data_loader import load_country

try:
    df = load_country('invalid_country', data_type='raw')
except ValueError as e:
    print(f"Error: {e}")
    # Handle the error appropriately

try:
    df = load_country('benin', data_type='nonexistent_type')
except ValueError as e:
    print(f"Error: {e}")
```

## Benefits

1. **Consistency**: All notebooks use the same loading logic
2. **Type Safety**: Automatic datetime parsing and numeric conversion
3. **Error Handling**: Clear error messages for missing files
4. **Convenience**: Simple functions for common tasks
5. **Flexibility**: Class-based design allows customization
6. **Documentation**: Full docstrings with examples

## Replacing Old Loading Code

### Before (in notebooks):

```python
import pandas as pd
benin_df = pd.read_csv('../data/benin-malanville.csv')
benin_df['Timestamp'] = pd.to_datetime(benin_df['Timestamp'])
# Repeat for each country...
```

### After:

```python
from utils.data_loader import load_country
benin_df = load_country('benin', data_type='raw')
```

Much cleaner and consistent! ✨
