"""
Sidebar Component

Handles country selection and navigation.
"""

import streamlit as st
from typing import List
from ..config import COUNTRIES


def render_sidebar(available_countries: List[str]) -> str:
    """
    Render the sidebar with country selection.
    
    Parameters
    ----------
    available_countries : List[str]
        List of available country keys
        
    Returns
    -------
    str
        Selected country key
    """
    with st.sidebar:
        st.title("☀️ Solar Dashboard")
        
        st.markdown("---")
        
        # Country selection
        st.subheader("📍 Select Country")
        
        # Create radio options with flags and names
        country_options = {
            f"{COUNTRIES[c]['flag']} {COUNTRIES[c]['name']}": c 
            for c in available_countries
        }
        
        selected_display = st.radio(
            "Choose a country to analyze:",
            options=list(country_options.keys()),
            label_visibility="collapsed"
        )
        
        selected_country = country_options[selected_display]
        
        st.markdown("---")
        
        # Country info
        st.subheader("ℹ️ Location Info")
        country_info = COUNTRIES[selected_country]
        st.write(f"**Country:** {country_info['name']}")
        st.write(f"**Location:** {country_info['location']}")
        
        st.markdown("---")
        
        # Navigation
        st.subheader("📊 Dashboard Sections")
        st.markdown("""
        - **Overview**: Key statistics
        - **Time Patterns**: Monthly & hourly trends
        - **Correlations**: Variable relationships
        - **Comparisons**: Cross-country analysis
        """)
        
        st.markdown("---")
        
        # About
        with st.expander("ℹ️ About"):
            st.markdown("""
            This dashboard analyzes solar radiation data from three West African locations.
            
            **Data Source:**  
            Solar Radiation Measurement Data
            
            **Metrics:**
            - GHI: Global Horizontal Irradiance
            - DNI: Direct Normal Irradiance
            - DHI: Diffuse Horizontal Irradiance
            """)
        
    return selected_country
