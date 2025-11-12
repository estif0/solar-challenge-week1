"""
Overview Component

Displays key statistics and summary cards.
"""

import streamlit as st
from typing import Dict, Any
from ..config import COUNTRIES, SOLAR_METRICS


def render_overview(country_stats: Dict[str, Any], country_key: str):
    """
    Render overview section with key statistics.
    
    Parameters
    ----------
    country_stats : Dict
        Country-specific statistics
    country_key : str
        Country identifier
    """
    st.header(f"📊 Overview: {COUNTRIES[country_key]['name']}")
    
    # Data info
    st.subheader("📅 Data Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Records",
            f"{country_stats['record_count']:,}"
        )
    
    date_range = country_stats.get('date_range', {})
    with col2:
        st.metric(
            "Start Date",
            date_range.get('start', 'N/A')[:10]
        )
    
    with col3:
        st.metric(
            "End Date",
            date_range.get('end', 'N/A')[:10]
        )
    
    st.markdown("---")
    
    # Solar irradiance metrics
    st.subheader("☀️ Solar Irradiance Statistics")
    
    solar_data = country_stats.get('solar_irradiance', {})
    
    # Create tabs for different metrics
    tabs = st.tabs(['GHI', 'DNI', 'DHI'])
    
    for i, (metric_key, tab) in enumerate(zip(['GHI', 'DNI', 'DHI'], tabs)):
        with tab:
            if metric_key in solar_data:
                metric_stats = solar_data[metric_key]
                metric_info = SOLAR_METRICS[metric_key]
                
                # Display metric description
                st.info(f"**{metric_info['name']}**: {metric_info['description']}")
                
                # Display statistics in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Mean",
                        f"{metric_stats['mean']:.2f}",
                        help=f"Average {metric_key}"
                    )
                
                with col2:
                    st.metric(
                        "Median",
                        f"{metric_stats['median']:.2f}",
                        help=f"Middle value of {metric_key}"
                    )
                
                with col3:
                    st.metric(
                        "Maximum",
                        f"{metric_stats['max']:.2f}",
                        help=f"Peak {metric_key} value"
                    )
                
                with col4:
                    st.metric(
                        "Std Dev",
                        f"{metric_stats['std']:.2f}",
                        help=f"Variability in {metric_key}"
                    )
                
                # Additional statistics in expander
                with st.expander("📈 More Statistics"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Minimum:** {metric_stats['min']:.2f} {metric_info['unit']}")
                        st.write(f"**25th Percentile:** {metric_stats['q25']:.2f} {metric_info['unit']}")
                    
                    with col2:
                        st.write(f"**75th Percentile:** {metric_stats['q75']:.2f} {metric_info['unit']}")
                        st.write(f"**Range:** {metric_stats['max'] - metric_stats['min']:.2f} {metric_info['unit']}")
                    
                    with col3:
                        iqr = metric_stats['q75'] - metric_stats['q25']
                        st.write(f"**IQR:** {iqr:.2f} {metric_info['unit']}")
                        cv = (metric_stats['std'] / metric_stats['mean']) * 100
                        st.write(f"**Coeff. of Variation:** {cv:.2f}%")
    
    st.markdown("---")
    
    # Solar assessment
    st.subheader("⚡ Solar Energy Potential Assessment")
    
    assessment = country_stats.get('solar_assessment', {})
    
    if assessment:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Annual GHI",
                f"{assessment.get('annual_ghi_kwh_m2', 0):.0f} kWh/m²",
                help="Estimated annual Global Horizontal Irradiance"
            )
        
        with col2:
            st.metric(
                "Mean Daily Energy",
                f"{assessment.get('mean_daily_energy_kwh_m2', 0):.2f} kWh/m²",
                help="Average daily solar energy"
            )
        
        with col3:
            st.metric(
                "Daylight Hours",
                f"{assessment.get('daylight_hours_percent', 0):.1f}%",
                help="Percentage of time with significant solar radiation"
            )
        
        # Meteorological conditions
        if 'mean_ambient_temp' in assessment:
            st.markdown("#### 🌡️ Environmental Conditions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Mean Temperature",
                    f"{assessment.get('mean_ambient_temp', 0):.1f}°C"
                )
            
            with col2:
                st.metric(
                    "Max Temperature",
                    f"{assessment.get('max_ambient_temp', 0):.1f}°C"
                )
            
            with col3:
                st.metric(
                    "Min Temperature",
                    f"{assessment.get('min_ambient_temp', 0):.1f}°C"
                )
