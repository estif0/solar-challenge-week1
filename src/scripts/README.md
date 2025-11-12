# Scripts Directory

This directory contains standalone scripts for data processing, validation, and analysis tasks.

## Available Scripts

### `data_validator.py`

Validates the structural integrity and format consistency of data files.

**Purpose**: Ensures all data files conform to the expected schema before analysis.

**What it checks**:

-   ✓ File format (must be .csv)
-   ✓ Column names and order
-   ✓ Data types compatibility
-   ✓ File encoding and structure

**What it does NOT check**:

-   ✗ Data quality (missing values, outliers)
-   ✗ Statistical properties
-   ✗ Business logic validation

**Usage**:

```bash
# Validate raw data files
python3 src/scripts/data_validator.py --dir raw

# Validate cleaned data files
python3 src/scripts/data_validator.py --dir cleaned

# Validate processed data files
python3 src/scripts/data_validator.py --dir processed

# Specify custom data directory
python3 src/scripts/data_validator.py --dir raw --data-path /path/to/data
```

**Exit codes**:

-   `0`: All files valid
-   `1`: One or more files have issues

**Example output**:

```
======================================================================
DATA VALIDATION REPORT
======================================================================
Directory: /path/to/data/raw
Files checked: 3
Files valid: 3
Status: ✓ ALL VALID
======================================================================

✓ benin-malanville.csv
  ✓ file_format: Valid CSV format
  ✓ columns: All columns present and in correct order
  ✓ data_types: All columns have compatible data types
```

## Expected Data Schema

All solar radiation CSV files should have the following columns in order:

1. `Timestamp` - Date and time of measurement
2. `GHI` - Global Horizontal Irradiance
3. `DNI` - Direct Normal Irradiance
4. `DHI` - Diffuse Horizontal Irradiance
5. `ModA` - Module A measurement
6. `ModB` - Module B measurement
7. `Tamb` - Ambient Temperature
8. `RH` - Relative Humidity
9. `WS` - Wind Speed
10. `WSgust` - Wind Speed Gust
11. `WSstdev` - Wind Speed Standard Deviation
12. `WD` - Wind Direction
13. `WDstdev` - Wind Direction Standard Deviation
14. `BP` - Barometric Pressure
15. `Cleaning` - Cleaning indicator
16. `Precipitation` - Precipitation amount
17. `TModA` - Temperature Module A
18. `TModB` - Temperature Module B
19. `Comments` - Additional comments

## Integration with CI/CD

You can integrate the validator into your workflow:

```bash
# In your CI pipeline or pre-commit hook
python3 src/scripts/data_validator.py --dir raw || exit 1
```
