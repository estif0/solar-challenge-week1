"""
Generate Pre-Computed Statistics for Dashboard

This script processes cleaned data and generates statistics that will be
used by the Streamlit dashboard. This solves the problem of the data/ folder
being gitignored - we save computed statistics as JSON files.

Run this script whenever your data changes:
    python src/scripts/generate_dashboard_data.py
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from utils.data_loader import DataLoader
from analysis.solar_metrics import SolarMetrics, compare_solar_potential
from analysis.statistical_tests import StatisticalAnalyzer


def generate_statistics():
    """Generate and save all dashboard statistics."""
    
    print("🔄 Loading cleaned data...")
    loader = DataLoader()
    
    try:
        # Load all countries' cleaned data
        countries_data = loader.load_all_countries(data_type='cleaned')
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure cleaned data exists in src/data/cleaned/")
        return
    
    print(f"✅ Loaded data for {len(countries_data)} countries")
    
    # Initialize statistics dictionary
    stats = {
        'countries': {},
        'comparison': {},
        'metadata': {
            'generation_date': pd.Timestamp.now().isoformat(),
            'countries_included': list(countries_data.keys())
        }
    }
    
    # Process each country
    for country, df in countries_data.items():
        print(f"\n📊 Processing {country.capitalize()}...")
        
        # Basic statistics
        country_stats = {
            'record_count': len(df),
            'date_range': {
                'start': df['Timestamp'].min().isoformat(),
                'end': df['Timestamp'].max().isoformat()
            },
            'solar_irradiance': {},
            'meteorological': {},
            'temporal_patterns': {}
        }
        
        # Solar irradiance statistics
        for col in ['GHI', 'DNI', 'DHI']:
            if col in df.columns:
                country_stats['solar_irradiance'][col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'q25': float(df[col].quantile(0.25)),
                    'q75': float(df[col].quantile(0.75))
                }
        
        # Meteorological variables
        for col in ['Tamb', 'RH', 'WS', 'BP']:
            if col in df.columns:
                country_stats['meteorological'][col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                }
        
        # Use SolarMetrics for advanced analysis
        metrics = SolarMetrics(df)
        assessment = metrics.assess_solar_potential()
        
        country_stats['solar_assessment'] = assessment
        
        # Monthly patterns
        monthly = metrics.calculate_monthly_patterns(['GHI', 'DNI', 'DHI'])
        country_stats['temporal_patterns']['monthly'] = {
            col: {
                'mean': monthly[(col, 'mean')].to_dict(),
                'max': monthly[(col, 'max')].to_dict()
            }
            for col in ['GHI', 'DNI', 'DHI'] if (col, 'mean') in monthly.columns
        }
        
        # Hourly patterns
        hourly = metrics.calculate_hourly_patterns(['GHI', 'DNI', 'DHI'])
        country_stats['temporal_patterns']['hourly'] = {
            col: {
                'mean': hourly[(col, 'mean')].to_dict(),
                'max': hourly[(col, 'max')].to_dict()
            }
            for col in ['GHI', 'DNI', 'DHI'] if (col, 'mean') in hourly.columns
        }
        
        # Correlation matrix
        corr_vars = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
        available_vars = [v for v in corr_vars if v in df.columns]
        if len(available_vars) > 1:
            corr_matrix = df[available_vars].corr()
            country_stats['correlations'] = corr_matrix.to_dict()
        
        stats['countries'][country] = country_stats
    
    # Cross-country comparison using existing function
    print("\n🔄 Generating cross-country comparison...")
    comparison = compare_solar_potential(countries_data)
    stats['comparison']['solar_potential'] = comparison.to_dict()
    
    # Statistical tests for key metrics
    print("🔄 Running statistical tests...")
    statistical_tests = StatisticalAnalyzer()
    
    for metric in ['GHI', 'DNI', 'DHI']:
        if all(metric in df.columns for df in countries_data.values()):
            # Prepare data for ANOVA
            groups = [df[metric].dropna().values for df in countries_data.values()]
            labels = list(countries_data.keys())
            
            # ANOVA test
            anova_result = statistical_tests.anova_oneway(
                *groups, # type: ignore
                group_names=labels
            )
            
            if metric not in stats['comparison']:
                stats['comparison'][metric] = {}
            
            stats['comparison'][metric]['anova'] = {
                'f_statistic': float(anova_result['f_statistic']),
                'p_value': float(anova_result['p_value']),
                'significant': bool(anova_result['significant_difference']),
                'interpretation': anova_result['interpretation']
            }
    
    # Save to JSON file
    output_path = Path(__file__).parent.parent / 'data' / 'processed' / 'dashboard_statistics.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Saving statistics to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"✅ Dashboard statistics generated successfully!")
    print(f"📁 File size: {output_path.stat().st_size / 1024:.2f} KB")
    print(f"\n🎉 Ready for dashboard deployment!")


if __name__ == '__main__':
    generate_statistics()
