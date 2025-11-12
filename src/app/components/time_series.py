"""
Time Series Component

Displays temporal patterns (monthly and hourly).
"""

import streamlit as st
from typing import Dict, Any
from ..utils.chart_builder import create_monthly_pattern_chart, create_hourly_pattern_chart
from ..config import COUNTRIES


def render_time_series(country_stats: Dict[str, Any], country_key: str):
    """
    Render time series analysis section.
    
    Parameters
    ----------
    country_stats : Dict
        Country-specific statistics
    country_key : str
        Country identifier
    """
    st.header(f"📈 Time Patterns: {COUNTRIES[country_key]['name']}")
    
    # Monthly patterns
    st.subheader("📅 Monthly Patterns")
    st.markdown("Average solar irradiance by month throughout the year.")
    
    # Tabs for different metrics
    metric_tabs = st.tabs(['GHI', 'DNI', 'DHI'])
    
    for metric, tab in zip(['GHI', 'DNI', 'DHI'], metric_tabs):
        with tab:
            fig = create_monthly_pattern_chart(country_stats, metric)
            if fig.data:
                st.plotly_chart(fig, width='stretch')
            else:
                st.warning(f"No monthly data available for {metric}")
    
    st.markdown("---")
    
    # Hourly patterns
    st.subheader("🕐 Daily Pattern (Hourly Averages)")
    st.markdown("Average solar irradiance by hour of the day.")
    
    fig = create_hourly_pattern_chart(country_stats, ['GHI', 'DNI', 'DHI'])
    if fig.data:
        st.plotly_chart(fig, width='stretch')
        
        # Insights
        with st.expander("💡 Pattern Insights"):
            st.markdown("""
            **Key Observations:**
            - Solar irradiance peaks around midday (11 AM - 2 PM)
            - DNI typically shows sharper peaks than GHI
            - DHI remains relatively constant during daylight hours
            - Early morning and late afternoon show lower irradiance values
            """)
    else:
        st.warning("No hourly data available")
