"""
Solar Radiation Analysis Dashboard

Main Streamlit application that analyzes solar radiation data from
three West African locations: Benin, Sierra Leone, and Togo.

This dashboard uses pre-computed statistics (not raw data) to ensure
it works even when the data/ folder is gitignored.

Run with: streamlit run src/app/main.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import PAGE_TITLE, PAGE_ICON, LAYOUT
from app.utils.data_loader import load_statistics, get_country_stats, get_metadata
from app.components.sidebar import render_sidebar
from app.components.overview import render_overview
from app.components.time_series import render_time_series
from app.components.correlations import render_correlations
from app.components.comparisons import render_comparisons


# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Load statistics
    try:
        stats = load_statistics()
    except FileNotFoundError as e:
        st.error(f"""
        ### ⚠️ Statistics File Not Found
        
        {str(e)}
        
        **To fix this:**
        1. Make sure you have cleaned data in `src/data/cleaned/`
        2. Run the data generation script:
        ```bash
        python src/scripts/generate_dashboard_data.py
        ```
        """)
        st.stop()
    
    # Get metadata
    metadata = get_metadata(stats)
    available_countries = metadata.get('countries_included', [])
    
    if not available_countries:
        st.error("No country data available in statistics file.")
        st.stop()
    
    # Render sidebar and get selected country
    selected_country = render_sidebar(available_countries)
    
    # Get country-specific statistics
    country_stats = get_country_stats(stats, selected_country)
    
    # Main content area
    st.title(f"{PAGE_ICON} Solar Radiation Analysis Dashboard")
    st.markdown(f"*Data generated on: {metadata.get('generation_date', 'Unknown')[:10]}*")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "📈 Time Patterns",
        "🔗 Correlations",
        "🌍 Comparisons"
    ])
    
    with tab1:
        render_overview(country_stats, selected_country)
    
    with tab2:
        render_time_series(country_stats, selected_country)
    
    with tab3:
        render_correlations(country_stats, selected_country)
    
    with tab4:
        render_comparisons(stats)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>Built with Streamlit • Data from Solar Radiation Measurement Dataset</p>
        <p>🌞 Analyzing solar potential across West Africa</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
