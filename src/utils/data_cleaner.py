"""
Data Cleaning Utilities

This module provides reusable functions for cleaning and preprocessing
solar radiation data. It includes utilities for:
- Outlier detection and handling (Z-score, IQR methods)
- Missing value detection and handling
- Negative value cleaning for solar radiation data
- Data quality reporting
- Column-specific cleaning strategies

All functions are designed to be composable and work with pandas DataFrames.
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict, Tuple, Optional, Callable
import warnings


class DataCleaner:
    """
    A collection of data cleaning methods for solar radiation datasets.
    
    This class provides methods for detecting and handling various data quality
    issues including outliers, missing values, and invalid measurements.
    
    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to clean
    
    Attributes
    ----------
    df : pd.DataFrame
        The DataFrame being cleaned
    cleaning_log : List[str]
        Log of cleaning operations performed
    """
    
    def __init__(self, df: pd.DataFrame):
        """Initialize DataCleaner with a DataFrame."""
        self.df = df.copy()
        self.cleaning_log = []
    
    def detect_outliers_zscore(
        self,
        column: str,
        threshold: float = 3.0
    ) -> pd.Series:
        """
        Detect outliers using Z-score method.
        
        Parameters
        ----------
        column : str
            Column name to check for outliers
        threshold : float, default 3.0
            Z-score threshold (typically 2.5 or 3.0)
            
        Returns
        -------
        pd.Series
            Boolean series where True indicates an outlier
            
        Examples
        --------
        >>> cleaner = DataCleaner(df)
        >>> outliers = cleaner.detect_outliers_zscore('GHI', threshold=3.0)
        >>> print(f"Found {outliers.sum()} outliers")
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        data = self.df[column]
        
        # Remove NaN values for calculation
        data_clean = data.dropna()
        
        if len(data_clean) == 0:
            return pd.Series([False] * len(data), index=data.index)
        
        # Calculate Z-scores
        mean = data_clean.mean()
        std = data_clean.std()
        
        if std == 0:
            return pd.Series([False] * len(data), index=data.index)
        
        z_scores = np.abs((data - mean) / std)
        outliers = z_scores > threshold
        
        return outliers
    
    def detect_outliers_iqr(
        self,
        column: str,
        multiplier: float = 1.5
    ) -> pd.Series:
        """
        Detect outliers using Interquartile Range (IQR) method.
        
        Parameters
        ----------
        column : str
            Column name to check for outliers
        multiplier : float, default 1.5
            IQR multiplier (1.5 for outliers, 3.0 for extreme outliers)
            
        Returns
        -------
        pd.Series
            Boolean series where True indicates an outlier
            
        Examples
        --------
        >>> cleaner = DataCleaner(df)
        >>> outliers = cleaner.detect_outliers_iqr('Tamb', multiplier=1.5)
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        data = self.df[column]
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outliers = (data < lower_bound) | (data > upper_bound)
        
        return outliers
    
    def handle_outliers(
        self,
        column: str,
        method: str = 'zscore',
        threshold: float = 3.0,
        strategy: str = 'nan'
    ) -> 'DataCleaner':
        """
        Handle outliers in a column using specified strategy.
        
        Parameters
        ----------
        column : str
            Column name to process
        method : str, default 'zscore'
            Detection method: 'zscore' or 'iqr'
        threshold : float, default 3.0
            Threshold for outlier detection
        strategy : str, default 'nan'
            How to handle outliers:
            - 'nan': Replace with NaN
            - 'median': Replace with median
            - 'mean': Replace with mean
            - 'clip': Clip to threshold boundaries
            
        Returns
        -------
        DataCleaner
            Self for method chaining
            
        Examples
        --------
        >>> cleaner = DataCleaner(df)
        >>> cleaner.handle_outliers('GHI', method='zscore', strategy='nan')
        """
        # Detect outliers
        if method == 'zscore':
            outliers = self.detect_outliers_zscore(column, threshold)
        elif method == 'iqr':
            outliers = self.detect_outliers_iqr(column, threshold)
        else:
            raise ValueError(f"Unknown method '{method}'. Use 'zscore' or 'iqr'")
        
        num_outliers = outliers.sum()
        
        if num_outliers == 0:
            self.cleaning_log.append(f"{column}: No outliers detected")
            return self
        
        # Handle outliers based on strategy
        if strategy == 'nan':
            self.df.loc[outliers, column] = np.nan
            
        elif strategy == 'median':
            median_val = self.df[column].median()
            self.df.loc[outliers, column] = median_val
            
        elif strategy == 'mean':
            mean_val = self.df[column].mean()
            self.df.loc[outliers, column] = mean_val
            
        elif strategy == 'clip':
            if method == 'zscore':
                mean = self.df[column].mean()
                std = self.df[column].std()
                lower = mean - threshold * std
                upper = mean + threshold * std
            else:  # iqr
                Q1 = self.df[column].quantile(0.25)
                Q3 = self.df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR
            
            self.df[column] = self.df[column].clip(lower, upper)
        else:
            raise ValueError(f"Unknown strategy '{strategy}'")
        
        self.cleaning_log.append(
            f"{column}: Handled {num_outliers} outliers using {method}/{strategy}"
        )
        
        return self
    
    def handle_missing_values(
        self,
        column: str,
        strategy: str = 'drop'
    ) -> 'DataCleaner':
        """
        Handle missing values in a column.
        
        Parameters
        ----------
        column : str
            Column name to process
        strategy : str, default 'drop'
            How to handle missing values:
            - 'drop': Remove rows with missing values
            - 'forward_fill': Forward fill (use previous value)
            - 'backward_fill': Backward fill (use next value)
            - 'interpolate': Linear interpolation
            - 'mean': Fill with column mean
            - 'median': Fill with column median
            - 'zero': Fill with zero
            
        Returns
        -------
        DataCleaner
            Self for method chaining
            
        Examples
        --------
        >>> cleaner = DataCleaner(df)
        >>> cleaner.handle_missing_values('GHI', strategy='interpolate')
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        num_missing = self.df[column].isna().sum()
        
        if num_missing == 0:
            self.cleaning_log.append(f"{column}: No missing values")
            return self
        
        if strategy == 'drop':
            self.df = self.df.dropna(subset=[column])
            
        elif strategy == 'forward_fill':
            self.df[column] = self.df[column].fillna(method='ffill')
            
        elif strategy == 'backward_fill':
            self.df[column] = self.df[column].fillna(method='bfill')
            
        elif strategy == 'interpolate':
            self.df[column] = self.df[column].interpolate(method='linear')
            
        elif strategy == 'mean':
            mean_val = self.df[column].mean()
            self.df[column] = self.df[column].fillna(mean_val)
            
        elif strategy == 'median':
            median_val = self.df[column].median()
            self.df[column] = self.df[column].fillna(median_val)
            
        elif strategy == 'zero':
            self.df[column] = self.df[column].fillna(0)
        else:
            raise ValueError(f"Unknown strategy '{strategy}'")
        
        self.cleaning_log.append(
            f"{column}: Handled {num_missing} missing values using {strategy}"
        )
        
        return self
    
    def clean_negative_values(
        self,
        columns: Union[str, List[str]],
        strategy: str = 'zero'
    ) -> 'DataCleaner':
        """
        Clean negative values in solar radiation columns.
        
        Solar radiation values (GHI, DNI, DHI) should not be negative during
        daylight hours. This method handles such invalid values.
        
        Parameters
        ----------
        columns : str or List[str]
            Column name(s) to process
        strategy : str, default 'zero'
            How to handle negative values:
            - 'zero': Replace with 0
            - 'nan': Replace with NaN
            - 'abs': Take absolute value
            
        Returns
        -------
        DataCleaner
            Self for method chaining
            
        Examples
        --------
        >>> cleaner = DataCleaner(df)
        >>> cleaner.clean_negative_values(['GHI', 'DNI', 'DHI'], strategy='zero')
        """
        if isinstance(columns, str):
            columns = [columns]
        
        for column in columns:
            if column not in self.df.columns:
                warnings.warn(f"Column '{column}' not found, skipping")
                continue
            
            negative_mask = self.df[column] < 0
            num_negative = negative_mask.sum()
            
            if num_negative == 0:
                self.cleaning_log.append(f"{column}: No negative values")
                continue
            
            if strategy == 'zero':
                self.df.loc[negative_mask, column] = 0
            elif strategy == 'nan':
                self.df.loc[negative_mask, column] = np.nan
            elif strategy == 'abs':
                self.df.loc[negative_mask, column] = self.df.loc[negative_mask, column].abs()
            else:
                raise ValueError(f"Unknown strategy '{strategy}'")
            
            self.cleaning_log.append(
                f"{column}: Cleaned {num_negative} negative values using {strategy}"
            )
        
        return self
    
    def remove_duplicates(
        self,
        subset: Optional[List[str]] = None,
        keep: str = 'first'
    ) -> 'DataCleaner':
        """
        Remove duplicate rows.
        
        Parameters
        ----------
        subset : List[str], optional
            Columns to consider for identifying duplicates
        keep : str, default 'first'
            Which duplicates to keep: 'first', 'last', or False (remove all)
            
        Returns
        -------
        DataCleaner
            Self for method chaining
        """
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        after = len(self.df)
        
        removed = before - after
        self.cleaning_log.append(f"Removed {removed} duplicate rows")
        
        return self
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Get the cleaned DataFrame.
        
        Returns
        -------
        pd.DataFrame
            Cleaned DataFrame
        """
        return self.df
    
    def get_cleaning_report(self) -> str:
        """
        Get a report of all cleaning operations performed.
        
        Returns
        -------
        str
            Formatted cleaning report
        """
        if not self.cleaning_log:
            return "No cleaning operations performed"
        
        report = "Data Cleaning Report\n"
        report += "=" * 50 + "\n"
        for i, log_entry in enumerate(self.cleaning_log, 1):
            report += f"{i}. {log_entry}\n"
        
        return report


# Standalone utility functions

def detect_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of missing values in the DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to analyze
        
    Returns
    -------
    pd.DataFrame
        Summary with columns: Column, Missing_Count, Missing_Percent
        
    Examples
    --------
    >>> summary = detect_missing_summary(df)
    >>> print(summary)
    """
    missing_counts = df.isna().sum()
    missing_percent = (missing_counts / len(df)) * 100
    
    summary = pd.DataFrame({
        'Column': missing_counts.index,
        'Missing_Count': missing_counts.values,
        'Missing_Percent': missing_percent.values
    })
    
    # Only show columns with missing values
    summary = summary[summary['Missing_Count'] > 0]
    summary = summary.sort_values('Missing_Count', ascending=False)
    summary = summary.reset_index(drop=True)
    
    return summary


def get_data_quality_report(df: pd.DataFrame) -> Dict[str, any]:
    """
    Generate a comprehensive data quality report.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to analyze
        
    Returns
    -------
    Dict
        Dictionary containing various quality metrics
        
    Examples
    --------
    >>> report = get_data_quality_report(df)
    >>> print(f"Total rows: {report['total_rows']}")
    >>> print(f"Duplicate rows: {report['duplicate_rows']}")
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'duplicate_rows': df.duplicated().sum(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'missing_values': {},
        'negative_values': {},
        'data_types': df.dtypes.to_dict()
    }
    
    # Missing values per column
    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            report['missing_values'][col] = {
                'count': int(missing_count),
                'percent': float((missing_count / len(df)) * 100)
            }
    
    # Negative values in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        negative_count = (df[col] < 0).sum()
        if negative_count > 0:
            report['negative_values'][col] = {
                'count': int(negative_count),
                'percent': float((negative_count / len(df)) * 100)
            }
    
    return report


def quick_clean(
    df: pd.DataFrame,
    handle_negatives: bool = True,
    handle_outliers: bool = True,
    handle_missing: bool = True,
    outlier_columns: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, str]:
    """
    Perform a quick, standard cleaning pipeline.
    
    This is a convenience function that applies common cleaning operations
    in a sensible default order.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to clean
    handle_negatives : bool, default True
        Whether to clean negative values in radiation columns
    handle_outliers : bool, default True
        Whether to handle outliers using Z-score method
    handle_missing : bool, default True
        Whether to handle missing values
    outlier_columns : List[str], optional
        Specific columns to check for outliers. If None, uses common columns.
        
    Returns
    -------
    Tuple[pd.DataFrame, str]
        Cleaned DataFrame and cleaning report
        
    Examples
    --------
    >>> cleaned_df, report = quick_clean(df)
    >>> print(report)
    """
    cleaner = DataCleaner(df)
    
    # Remove duplicates
    cleaner.remove_duplicates(subset=['Timestamp'])
    
    # Handle negative values in radiation columns
    if handle_negatives:
        radiation_cols = ['GHI', 'DNI', 'DHI']
        existing_cols = [col for col in radiation_cols if col in df.columns]
        if existing_cols:
            cleaner.clean_negative_values(existing_cols, strategy='zero')
    
    # Handle outliers
    if handle_outliers:
        if outlier_columns is None:
            outlier_columns = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'RH']
        
        existing_outlier_cols = [col for col in outlier_columns if col in df.columns]
        for col in existing_outlier_cols:
            cleaner.handle_outliers(col, method='zscore', threshold=3.5, strategy='nan')
    
    # Handle missing values (interpolate for time series)
    if handle_missing:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if cleaner.df[col].isna().sum() > 0:
                cleaner.handle_missing_values(col, strategy='interpolate')
    
    return cleaner.get_cleaned_data(), cleaner.get_cleaning_report()
