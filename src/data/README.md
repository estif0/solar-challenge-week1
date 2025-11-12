# Data Directory Structure

This directory contains all data files organized by processing stage.

## Directory Organization

### `raw/`

Contains original, unmodified data files as received from data sources.

-   **benin-malanville.csv**: Original solar radiation data from Benin
-   **sierraleone-bumbuna.csv**: Original solar radiation data from Sierra Leone
-   **togo-dapaong_qc.csv**: Original solar radiation data from Togo

**Note**: Files in this directory should never be modified directly. Always work with copies.

### `cleaned/`

Contains cleaned versions of raw data with:

-   Missing values handled
-   Outliers detected and treated
-   Data types standardized
-   Quality control flags applied

Files:

-   **benin_cleaned.csv**: Cleaned Benin data
-   **sierraleone_cleaned.csv**: Cleaned Sierra Leone data
-   **togo_cleaned.csv**: Cleaned Togo data

### `processed/`

Contains aggregated, transformed, or derived datasets ready for analysis or visualization.

-   **dashboard_comparison.csv**: Cross-country comparison metrics
-   **dashboard_daily_patterns.csv**: Daily aggregated patterns
-   **dashboard_monthly_data.csv**: Monthly aggregated data
-   **dashboard_statistics.json**: Summary statistics for all datasets

### `external/`

Reserved for external reference data, such as:

-   Geographic coordinates
-   Climate zone definitions
-   Solar irradiance standards
-   Any third-party datasets

## Data Flow

```
raw/ → cleaned/ → processed/
         ↑            ↑
         |            |
    [cleaning]   [aggregation]
    [validation] [transformation]
```

## Usage Guidelines

1. **Never modify files in `raw/`** - these are your source of truth
2. **Cleaning scripts** should read from `raw/` and write to `cleaned/`
3. **Analysis scripts** should primarily use `cleaned/` data
4. **Dashboard/reporting** should use `processed/` data
5. **Version control**: Only commit small sample files or data schemas, not full datasets
