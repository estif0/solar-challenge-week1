"""
Data Loading Utilities

This module provides standardized functions for loading solar radiation data
from various sources and formats. It ensures consistent data loading across
all analysis scripts and notebooks.

Features:
- Automatic path resolution for different data directories
- Consistent datetime parsing
- Proper data type handling
- Error handling and validation
- Support for single files and batch loading
"""

import pandas as pd
from pathlib import Path
from typing import Union, List, Optional, Dict
import warnings


class DataLoader:
    """
    Handles loading of solar radiation data files with consistent formatting.
    
    This class provides a unified interface for loading data from different
    directories (raw, cleaned, processed) with proper type handling and
    datetime parsing.
    
    Parameters
    ----------
    data_dir : str or Path, optional
        Base data directory path. If None, uses default 'src/data' path.
    
    Attributes
    ----------
    data_dir : Path
        Base directory containing data subdirectories
    raw_dir : Path
        Directory for raw data files
    cleaned_dir : Path
        Directory for cleaned data files
    processed_dir : Path
        Directory for processed data files
    external_dir : Path
        Directory for external reference data
    """
    
    # Standard column definitions for solar radiation data
    DATETIME_COLUMNS = ['Timestamp']
    NUMERIC_COLUMNS = [
        'GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 
        'WS', 'WSgust', 'WSstdev', 'WD', 'WDstdev', 
        'BP', 'Cleaning', 'Precipitation', 'TModA', 'TModB'
    ]
    STRING_COLUMNS = ['Comments']
    
    def __init__(self, data_dir: Optional[Union[str, Path]] = None):
        """Initialize DataLoader with data directory paths."""
        if data_dir is None:
            # Default to src/data directory relative to this file
            self.data_dir = Path(__file__).parent.parent / 'data'
        else:
            self.data_dir = Path(data_dir)
        
        # Set up subdirectory paths
        self.raw_dir = self.data_dir / 'raw'
        self.cleaned_dir = self.data_dir / 'cleaned'
        self.processed_dir = self.data_dir / 'processed'
        self.external_dir = self.data_dir / 'external'
    
    def _validate_file_exists(self, filepath: Path) -> None:
        """
        Check if file exists and raise informative error if not.
        
        Parameters
        ----------
        filepath : Path
            Path to file to validate
            
        Raises
        ------
        FileNotFoundError
            If file does not exist
        """
        if not filepath.exists():
            raise FileNotFoundError(
                f"Data file not found: {filepath}\n"
                f"Please ensure the file exists in the correct directory."
            )
    
    def _parse_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse datetime columns with proper error handling.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with datetime columns to parse
            
        Returns
        -------
        pd.DataFrame
            DataFrame with parsed datetime columns
        """
        for col in self.DATETIME_COLUMNS:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception as e:
                    warnings.warn(
                        f"Could not parse {col} as datetime: {str(e)}. "
                        f"Column will be left as-is."
                    )
        return df
    
    def _convert_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert numeric columns to appropriate types.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with numeric columns to convert
            
        Returns
        -------
        pd.DataFrame
            DataFrame with converted numeric columns
        """
        for col in self.NUMERIC_COLUMNS:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    warnings.warn(
                        f"Could not convert {col} to numeric: {str(e)}. "
                        f"Column will be left as-is."
                    )
        return df
    
    def load_file(
        self, 
        filename: str, 
        data_type: str = 'raw',
        parse_dates: bool = True,
        convert_numeric: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load a single data file from specified directory.
        
        Parameters
        ----------
        filename : str
            Name of the file to load (e.g., 'benin-malanville.csv')
        data_type : str, default 'raw'
            Type of data directory: 'raw', 'cleaned', 'processed', or 'external'
        parse_dates : bool, default True
            Whether to parse datetime columns
        convert_numeric : bool, default True
            Whether to convert numeric columns
        **kwargs : dict
            Additional arguments passed to pd.read_csv()
            
        Returns
        -------
        pd.DataFrame
            Loaded and formatted DataFrame
            
        Raises
        ------
        FileNotFoundError
            If the specified file does not exist
        ValueError
            If data_type is not valid
            
        Examples
        --------
        >>> loader = DataLoader()
        >>> df = loader.load_file('benin-malanville.csv', data_type='raw')
        >>> df = loader.load_file('benin_cleaned.csv', data_type='cleaned')
        """
        # Get the appropriate directory
        dir_map = {
            'raw': self.raw_dir,
            'cleaned': self.cleaned_dir,
            'processed': self.processed_dir,
            'external': self.external_dir
        }
        
        if data_type not in dir_map:
            raise ValueError(
                f"Invalid data_type '{data_type}'. "
                f"Must be one of: {list(dir_map.keys())}"
            )
        
        filepath = dir_map[data_type] / filename
        self._validate_file_exists(filepath)
        
        # Load the CSV file
        try:
            df = pd.read_csv(filepath, **kwargs)
        except Exception as e:
            raise IOError(f"Error reading file {filepath}: {str(e)}")
        
        # Apply transformations
        if parse_dates:
            df = self._parse_datetime(df)
        
        if convert_numeric:
            df = self._convert_numeric(df)
        
        return df
    
    def load_country_data(
        self, 
        country: str, 
        data_type: str = 'raw',
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data for a specific country using standard naming conventions.
        
        Parameters
        ----------
        country : str
            Country name: 'benin', 'sierraleone', or 'togo'
        data_type : str, default 'raw'
            Type of data: 'raw' or 'cleaned'
        **kwargs : dict
            Additional arguments passed to load_file()
            
        Returns
        -------
        pd.DataFrame
            Loaded country data
            
        Examples
        --------
        >>> loader = DataLoader()
        >>> benin_raw = loader.load_country_data('benin', data_type='raw')
        >>> togo_cleaned = loader.load_country_data('togo', data_type='cleaned')
        """
        country = country.lower()
        
        # Map country names to file patterns
        filename_map = {
            'benin': {
                'raw': 'benin-malanville.csv',
                'cleaned': 'benin_cleaned.csv'
            },
            'sierraleone': {
                'raw': 'sierraleone-bumbuna.csv',
                'cleaned': 'sierraleone_cleaned.csv'
            },
            'togo': {
                'raw': 'togo-dapaong_qc.csv',
                'cleaned': 'togo_cleaned.csv'
            }
        }
        
        if country not in filename_map:
            raise ValueError(
                f"Unknown country '{country}'. "
                f"Must be one of: {list(filename_map.keys())}"
            )
        
        if data_type not in filename_map[country]:
            raise ValueError(
                f"Data type '{data_type}' not available for {country}. "
                f"Available types: {list(filename_map[country].keys())}"
            )
        
        filename = filename_map[country][data_type]
        return self.load_file(filename, data_type=data_type, **kwargs)
    
    def load_all_countries(
        self, 
        data_type: str = 'raw',
        add_country_column: bool = True,
        **kwargs
    ) -> Dict[str, pd.DataFrame]:
        """
        Load data for all available countries.
        
        Parameters
        ----------
        data_type : str, default 'raw'
            Type of data to load: 'raw' or 'cleaned'
        add_country_column : bool, default True
            Whether to add a 'Country' column to each DataFrame
        **kwargs : dict
            Additional arguments passed to load_country_data()
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary with country names as keys and DataFrames as values
            
        Examples
        --------
        >>> loader = DataLoader()
        >>> all_data = loader.load_all_countries(data_type='cleaned')
        >>> benin_df = all_data['benin']
        >>> togo_df = all_data['togo']
        """
        countries = ['benin', 'sierraleone', 'togo']
        data_dict = {}
        
        for country in countries:
            try:
                df = self.load_country_data(country, data_type=data_type, **kwargs)
                
                if add_country_column:
                    df['Country'] = country.capitalize()
                
                data_dict[country] = df
                
            except FileNotFoundError as e:
                warnings.warn(f"Could not load {country} data: {str(e)}")
                continue
        
        return data_dict
    
    def load_combined_data(
        self, 
        data_type: str = 'raw',
        **kwargs
    ) -> pd.DataFrame:
        """
        Load and combine data from all countries into a single DataFrame.
        
        Parameters
        ----------
        data_type : str, default 'raw'
            Type of data to load: 'raw' or 'cleaned'
        **kwargs : dict
            Additional arguments passed to load_all_countries()
            
        Returns
        -------
        pd.DataFrame
            Combined DataFrame with data from all countries
            
        Examples
        --------
        >>> loader = DataLoader()
        >>> combined = loader.load_combined_data(data_type='cleaned')
        >>> combined.groupby('Country')['GHI'].mean()
        """
        data_dict = self.load_all_countries(
            data_type=data_type,
            add_country_column=True,
            **kwargs
        )
        
        if not data_dict:
            raise ValueError("No data files could be loaded")
        
        # Combine all DataFrames
        combined_df = pd.concat(data_dict.values(), ignore_index=True)
        
        return combined_df


# Convenience functions for quick loading
def load_country(
    country: str, 
    data_type: str = 'raw',
    data_dir: Optional[Union[str, Path]] = None
) -> pd.DataFrame:
    """
    Convenience function to quickly load data for a specific country.
    
    Parameters
    ----------
    country : str
        Country name: 'benin', 'sierraleone', or 'togo'
    data_type : str, default 'raw'
        Type of data: 'raw' or 'cleaned'
    data_dir : str or Path, optional
        Custom data directory path
        
    Returns
    -------
    pd.DataFrame
        Loaded country data
        
    Examples
    --------
    >>> from utils.data_loader import load_country
    >>> benin_df = load_country('benin', data_type='cleaned')
    """
    loader = DataLoader(data_dir=data_dir)
    return loader.load_country_data(country, data_type=data_type)


def load_all(
    data_type: str = 'raw',
    data_dir: Optional[Union[str, Path]] = None
) -> Dict[str, pd.DataFrame]:
    """
    Convenience function to quickly load all country data.
    
    Parameters
    ----------
    data_type : str, default 'raw'
        Type of data: 'raw' or 'cleaned'
    data_dir : str or Path, optional
        Custom data directory path
        
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary with country names as keys and DataFrames as values
        
    Examples
    --------
    >>> from utils.data_loader import load_all
    >>> all_data = load_all(data_type='cleaned')
    >>> benin_df = all_data['benin']
    """
    loader = DataLoader(data_dir=data_dir)
    return loader.load_all_countries(data_type=data_type)
