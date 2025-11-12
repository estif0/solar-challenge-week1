"""
Analysis package for statistical tests and solar-specific calculations.

This package provides:
- Statistical tests (statistical_tests)
- Solar metrics calculations (solar_metrics)
"""

from .statistical_tests import (
    StatisticalAnalyzer,
    compare_groups,
    quick_correlation_test,
    summary_statistics
)
from .solar_metrics import (
    SolarMetrics,
    compare_solar_potential,
    calculate_dni_from_ghi_dhi,
    calculate_cleaning_impact,
    calculate_rh_impact_on_irradiance
)

__all__ = [
    'StatisticalAnalyzer',
    'compare_groups',
    'quick_correlation_test',
    'summary_statistics',
    'SolarMetrics',
    'compare_solar_potential',
    'calculate_dni_from_ghi_dhi',
    'calculate_cleaning_impact',
    'calculate_rh_impact_on_irradiance',
]
