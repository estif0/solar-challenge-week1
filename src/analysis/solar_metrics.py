"""
Solar Radiation Metrics and Analysis

This module provides domain-specific calculations and analysis for solar radiation data,
including:
- Solar irradiance component analysis (GHI, DNI, DHI)
- Clearness index calculations
- Solar energy potential assessment
- Temperature-based metrics
- Wind speed analysis
- Humidity impact analysis
- Time-based aggregations and patterns

All functions are designed to work with standard solar radiation datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple, Union, List
import warnings


class SolarMetrics:
    """
    Calculate solar radiation metrics and perform domain-specific analysis.
    
    This class provides methods for analyzing solar irradiance components,
    calculating derived metrics, and assessing solar energy potential.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing solar radiation data
    """
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with solar radiation DataFrame."""
        self.df = df.copy()
        self._validate_columns()
    
    def _validate_columns(self):
        """Validate that required columns exist."""
        required = ['Timestamp', 'GHI', 'DNI', 'DHI']
        missing = [col for col in required if col not in self.df.columns]
        if missing:
            warnings.warn(f"Missing columns: {missing}. Some methods may not work.")
    
    def calculate_clearness_index(
        self,
        solar_constant: float = 1367.0
    ) -> pd.Series:
        """
        Calculate clearness index (Kt = GHI / Extraterrestrial radiation).
        
        This is a simplified calculation using GHI and solar constant.
        For precise calculations, consider latitude, day of year, and solar zenith angle.
        
        Parameters
        ----------
        solar_constant : float, default 1367.0
            Solar constant in W/m²
            
        Returns
        -------
        pd.Series
            Clearness index values
            
        Examples
        --------
        >>> metrics = SolarMetrics(df)
        >>> kt = metrics.calculate_clearness_index()
        >>> print(f"Mean clearness index: {kt.mean():.3f}")
        """
        # Simplified clearness index
        # In practice, you'd calculate extraterrestrial radiation based on location and time
        kt = self.df['GHI'] / solar_constant
        kt = kt.clip(0, 1)  # Clearness index should be between 0 and 1
        return kt
    
    def calculate_diffuse_fraction(self) -> pd.Series:
        """
        Calculate diffuse fraction (Kd = DHI / GHI).
        
        Returns
        -------
        pd.Series
            Diffuse fraction values
            
        Examples
        --------
        >>> metrics = SolarMetrics(df)
        >>> kd = metrics.calculate_diffuse_fraction()
        >>> print(f"Mean diffuse fraction: {kd.mean():.3f}")
        """
        kd = self.df['DHI'] / self.df['GHI']
        kd = kd.replace([np.inf, -np.inf], np.nan)
        kd = kd.clip(0, 1)
        return kd
    
    def identify_daylight_hours(
        self,
        ghi_threshold: float = 10.0
    ) -> pd.Series:
        """
        Identify daylight hours based on GHI threshold.
        
        Parameters
        ----------
        ghi_threshold : float, default 10.0
            GHI threshold in W/m² to consider as daylight
            
        Returns
        -------
        pd.Series
            Boolean series indicating daylight hours
            
        Examples
        --------
        >>> metrics = SolarMetrics(df)
        >>> is_day = metrics.identify_daylight_hours()
        >>> print(f"Daylight hours: {is_day.sum()} out of {len(is_day)}")
        """
        return self.df['GHI'] > ghi_threshold
    
    def calculate_daily_energy(
        self,
        time_column: str = 'Timestamp',
        irradiance_column: str = 'GHI'
    ) -> pd.Series:
        """
        Calculate daily energy (kWh/m²) from irradiance data.
        
        Assumes data is in W/m² at regular intervals.
        
        Parameters
        ----------
        time_column : str, default 'Timestamp'
            Name of timestamp column
        irradiance_column : str, default 'GHI'
            Name of irradiance column to integrate
            
        Returns
        -------
        pd.Series
            Daily energy in kWh/m²
            
        Examples
        --------
        >>> metrics = SolarMetrics(df)
        >>> daily_energy = metrics.calculate_daily_energy()
        >>> print(f"Mean daily energy: {daily_energy.mean():.2f} kWh/m²")
        """
        df_copy = self.df.copy()
        df_copy['Date'] = pd.to_datetime(df_copy[time_column]).dt.date
        
        # Calculate time interval in hours
        if len(df_copy) > 1:
            time_diff = pd.to_datetime(df_copy[time_column]).diff()
            interval_hours = time_diff.dt.total_seconds().median() / 3600.0
        else:
            interval_hours = 1/60  # Assume 1-minute intervals
        
        # Sum irradiance for each day and convert to kWh/m²
        daily_energy = df_copy.groupby('Date')[irradiance_column].sum() * interval_hours / 1000.0
        
        return daily_energy
    
    def analyze_temperature_impact(
        self,
        temp_column: str = 'Tamb',
        irradiance_column: str = 'GHI',
        bins: int = 10
    ) -> pd.DataFrame:
        """
        Analyze the relationship between temperature and solar irradiance.
        
        Parameters
        ----------
        temp_column : str, default 'Tamb'
            Temperature column name
        irradiance_column : str, default 'GHI'
            Irradiance column name
        bins : int, default 10
            Number of temperature bins
            
        Returns
        -------
        pd.DataFrame
            Temperature bins with mean irradiance and counts
            
        Examples
        --------
        >>> metrics = SolarMetrics(df)
        >>> temp_analysis = metrics.analyze_temperature_impact()
        >>> print(temp_analysis)
        """
        df_copy = self.df[[temp_column, irradiance_column]].dropna()
        
        # Create temperature bins
        df_copy['temp_bin'] = pd.cut(df_copy[temp_column], bins=bins)
        
        # Aggregate by bin
        result = df_copy.groupby('temp_bin', observed=True).agg({
            irradiance_column: ['mean', 'std', 'count'],
            temp_column: 'mean'
        }).round(2)
        
        result.columns = ['mean_irradiance', 'std_irradiance', 'count', 'mean_temp']
        
        return result
    
    def calculate_solar_panel_efficiency(
        self,
        panel_temp_column: str = 'TModA',
        reference_temp: float = 25.0,
        temp_coefficient: float = -0.004
    ) -> pd.Series:
        """
        Estimate solar panel efficiency based on temperature.
        
        Uses temperature coefficient to adjust efficiency from reference conditions.
        
        Parameters
        ----------
        panel_temp_column : str, default 'TModA'
            Panel temperature column name
        reference_temp : float, default 25.0
            Reference temperature in °C
        temp_coefficient : float, default -0.004
            Temperature coefficient (typically -0.3% to -0.5% per °C)
            
        Returns
        -------
        pd.Series
            Relative efficiency factor (1.0 = reference conditions)
            
        Examples
        --------
        >>> metrics = SolarMetrics(df)
        >>> efficiency = metrics.calculate_solar_panel_efficiency()
        >>> print(f"Mean efficiency factor: {efficiency.mean():.3f}")
        """
        temp_diff = self.df[panel_temp_column] - reference_temp
        efficiency_factor = 1.0 + (temp_coefficient * temp_diff)
        return efficiency_factor.clip(0.5, 1.2)  # Reasonable bounds
    
    def analyze_wind_speed_impact(
        self,
        wind_column: str = 'WS',
        temp_column: str = 'TModA',
        bins: int = 5
    ) -> pd.DataFrame:
        """
        Analyze wind speed impact on panel temperature.
        
        Parameters
        ----------
        wind_column : str, default 'WS'
            Wind speed column name
        temp_column : str, default 'TModA'
            Panel temperature column name
        bins : int, default 5
            Number of wind speed bins
            
        Returns
        -------
        pd.DataFrame
            Wind speed bins with temperature statistics
        """
        df_copy = self.df[[wind_column, temp_column]].dropna()
        
        # Create wind speed bins
        df_copy['wind_bin'] = pd.cut(df_copy[wind_column], bins=bins)
        
        # Aggregate by bin
        result = df_copy.groupby('wind_bin', observed=True).agg({
            temp_column: ['mean', 'std', 'count'],
            wind_column: 'mean'
        }).round(2)
        
        result.columns = ['mean_temp', 'std_temp', 'count', 'mean_wind']
        
        return result
    
    def calculate_hourly_patterns(
        self,
        columns: Optional[List[str]] = None,
        time_column: str = 'Timestamp'
    ) -> pd.DataFrame:
        """
        Calculate hourly patterns for specified columns.
        
        Parameters
        ----------
        columns : List[str], optional
            Columns to analyze. If None, uses GHI, DNI, DHI
        time_column : str, default 'Timestamp'
            Timestamp column name
            
        Returns
        -------
        pd.DataFrame
            Hourly statistics
        """
        if columns is None:
            columns = ['GHI', 'DNI', 'DHI']
        
        df_copy = self.df.copy()
        df_copy['Hour'] = pd.to_datetime(df_copy[time_column]).dt.hour
        
        hourly = df_copy.groupby('Hour')[columns].agg(['mean', 'std', 'max'])
        
        return hourly.round(2)
    
    def calculate_monthly_patterns(
        self,
        columns: Optional[List[str]] = None,
        time_column: str = 'Timestamp'
    ) -> pd.DataFrame:
        """
        Calculate monthly patterns for specified columns.
        
        Parameters
        ----------
        columns : List[str], optional
            Columns to analyze. If None, uses GHI, DNI, DHI
        time_column : str, default 'Timestamp'
            Timestamp column name
            
        Returns
        -------
        pd.DataFrame
            Monthly statistics
        """
        if columns is None:
            columns = ['GHI', 'DNI', 'DHI']
        
        df_copy = self.df.copy()
        df_copy['Month'] = pd.to_datetime(df_copy[time_column]).dt.month
        
        monthly = df_copy.groupby('Month')[columns].agg(['mean', 'std', 'max'])
        
        return monthly.round(2)
    
    def assess_solar_potential(self) -> Dict[str, any]:
        """
        Comprehensive solar potential assessment.
        
        Returns
        -------
        Dict
            Dictionary with various solar potential metrics
            
        Examples
        --------
        >>> metrics = SolarMetrics(df)
        >>> assessment = metrics.assess_solar_potential()
        >>> print(f"Annual GHI: {assessment['annual_ghi_kwh_m2']:.2f} kWh/m²")
        """
        # Identify daylight hours
        is_daylight = self.identify_daylight_hours()
        daylight_data = self.df[is_daylight]
        
        # Calculate daily energy
        daily_energy = self.calculate_daily_energy()
        
        # Calculate clearness index
        kt = self.calculate_clearness_index()
        
        assessment = {
            'mean_ghi': float(self.df['GHI'].mean()),
            'max_ghi': float(self.df['GHI'].max()),
            'mean_dni': float(self.df['DNI'].mean()),
            'mean_dhi': float(self.df['DHI'].mean()),
            'mean_clearness_index': float(kt.mean()),
            'daylight_hours_percent': float((is_daylight.sum() / len(self.df)) * 100),
            'mean_daily_energy_kwh_m2': float(daily_energy.mean()),
            'annual_ghi_kwh_m2': float(daily_energy.sum() * 365 / len(daily_energy)),
            'peak_sun_hours': float(daily_energy.mean()),  # Approximation
        }
        
        # Add temperature data if available
        if 'Tamb' in self.df.columns:
            assessment['mean_ambient_temp'] = float(self.df['Tamb'].mean())
            assessment['max_ambient_temp'] = float(self.df['Tamb'].max())
            assessment['min_ambient_temp'] = float(self.df['Tamb'].min())
        
        return assessment


# Convenience functions

def calculate_dni_from_ghi_dhi(
    ghi: Union[pd.Series, np.ndarray],
    dhi: Union[pd.Series, np.ndarray],
    zenith_angle: Optional[Union[pd.Series, np.ndarray]] = None
) -> Union[pd.Series, np.ndarray]:
    """
    Calculate DNI from GHI and DHI.
    
    DNI = (GHI - DHI) / cos(zenith_angle)
    
    If zenith angle not provided, uses simplified calculation: DNI ≈ GHI - DHI
    
    Parameters
    ----------
    ghi : pd.Series or np.ndarray
        Global Horizontal Irradiance
    dhi : pd.Series or np.ndarray
        Diffuse Horizontal Irradiance
    zenith_angle : pd.Series or np.ndarray, optional
        Solar zenith angle in radians
        
    Returns
    -------
    pd.Series or np.ndarray
        Calculated DNI values
        
    Examples
    --------
    >>> dni = calculate_dni_from_ghi_dhi(df['GHI'], df['DHI'])
    """
    if zenith_angle is not None:
        dni = (ghi - dhi) / np.cos(zenith_angle)
    else:
        # Simplified approximation
        dni = ghi - dhi
    
    # Clean negative values
    if isinstance(dni, pd.Series):
        dni = dni.clip(lower=0)
    else:
        dni = np.maximum(dni, 0)
    
    return dni


def compare_solar_potential(
    data_dict: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Compare solar potential across multiple datasets (e.g., locations).
    
    Parameters
    ----------
    data_dict : Dict[str, pd.DataFrame]
        Dictionary with location names as keys and DataFrames as values
        
    Returns
    -------
    pd.DataFrame
        Comparison table with solar metrics for each location
        
    Examples
    --------
    >>> data = {'Benin': benin_df, 'Togo': togo_df, 'Sierra Leone': sierra_df}
    >>> comparison = compare_solar_potential(data)
    >>> print(comparison)
    """
    results = {}
    
    for name, df in data_dict.items():
        metrics = SolarMetrics(df)
        assessment = metrics.assess_solar_potential()
        results[name] = assessment
    
    comparison_df = pd.DataFrame(results).T
    comparison_df = comparison_df.round(2)
    
    return comparison_df


def calculate_cleaning_impact(
    df: pd.DataFrame,
    cleaning_column: str = 'Cleaning',
    irradiance_column: str = 'ModA',
    window_days: int = 7
) -> Dict[str, float]:
    """
    Analyze the impact of cleaning on module performance.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with cleaning events and module readings
    cleaning_column : str, default 'Cleaning'
        Binary column indicating cleaning events (1 = cleaned)
    irradiance_column : str, default 'ModA'
        Module irradiance measurement column
    window_days : int, default 7
        Days before/after cleaning to analyze
        
    Returns
    -------
    Dict
        Statistics on cleaning impact
        
    Examples
    --------
    >>> impact = calculate_cleaning_impact(df)
    >>> print(f"Improvement: {impact['percent_improvement']:.1f}%")
    """
    # Find cleaning events
    cleaning_events = df[df[cleaning_column] == 1].index
    
    if len(cleaning_events) == 0:
        return {'error': 'No cleaning events found'}
    
    before_values = []
    after_values = []
    
    for event_idx in cleaning_events:
        # Get window around event
        event_loc = df.index.get_loc(event_idx)
        
        # Before window
        before_start = max(0, event_loc - window_days * 1440)  # Assuming minute data
        before_data = df.iloc[before_start:event_loc][irradiance_column].mean()
        
        # After window  
        after_end = min(len(df), event_loc + window_days * 1440)
        after_data = df.iloc[event_loc:after_end][irradiance_column].mean()
        
        if not np.isnan(before_data) and not np.isnan(after_data):
            before_values.append(before_data)
            after_values.append(after_data)
    
    if len(before_values) == 0:
        return {'error': 'Insufficient data around cleaning events'}
    
    mean_before = np.mean(before_values)
    mean_after = np.mean(after_values)
    improvement = ((mean_after - mean_before) / mean_before) * 100
    
    return {
        'cleaning_events': len(cleaning_events),
        'mean_before_cleaning': float(mean_before),
        'mean_after_cleaning': float(mean_after),
        'percent_improvement': float(improvement),
        'events_analyzed': len(before_values)
    }


def calculate_rh_impact_on_irradiance(
    df: pd.DataFrame,
    rh_column: str = 'RH',
    irradiance_column: str = 'GHI',
    bins: int = 10
) -> pd.DataFrame:
    """
    Analyze relationship between relative humidity and solar irradiance.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with RH and irradiance data
    rh_column : str, default 'RH'
        Relative humidity column name
    irradiance_column : str, default 'GHI'
        Irradiance column name
    bins : int, default 10
        Number of RH bins
        
    Returns
    -------
    pd.DataFrame
        RH bins with irradiance statistics
    """
    df_clean = df[[rh_column, irradiance_column]].dropna()
    
    # Create RH bins
    df_clean['rh_bin'] = pd.cut(df_clean[rh_column], bins=bins)
    
    # Aggregate
    result = df_clean.groupby('rh_bin', observed=True).agg({
        irradiance_column: ['mean', 'std', 'count'],
        rh_column: 'mean'
    }).round(2)
    
    result.columns = ['mean_irradiance', 'std_irradiance', 'count', 'mean_rh']
    
    return result
