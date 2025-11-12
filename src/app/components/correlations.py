"""
Correlations Component

Displays correlation analysis and relationships.
"""

import streamlit as st
from typing import Dict, Any
from ..utils.chart_builder import create_correlation_heatmap
from ..config import COUNTRIES


def render_correlations(country_stats: Dict[str, Any], country_key: str):
    """
    Render correlation analysis section.
    
    Parameters
    ----------
    country_stats : Dict
        Country-specific statistics
    country_key : str
        Country identifier
    """
    st.header(f"🔗 Variable Correlations: {COUNTRIES[country_key]['name']}")
    
    st.markdown("""
    This heatmap shows the correlation between different variables. 
    - **+1** = perfect positive correlation
    - **0** = no correlation  
    - **-1** = perfect negative correlation
    """)
    
    fig = create_correlation_heatmap(country_stats)
    
    if fig.data:
        st.plotly_chart(fig, width='stretch')
        
        # Interpretation guide
        with st.expander("📖 How to Interpret"):
            st.markdown("""
            **Strong Correlations (|r| > 0.7):**
            - Indicate variables that move together closely
            - Example: GHI and DNI often show strong positive correlation
            
            **Moderate Correlations (0.3 < |r| < 0.7):**
            - Show some relationship but not perfectly linked
            - Example: Temperature and solar irradiance
            
            **Weak Correlations (|r| < 0.3):**
            - Little to no linear relationship
            - Example: Wind speed and humidity might be weakly correlated
            
            **Negative Correlations:**
            - Variables move in opposite directions
            - Example: Humidity typically decreases when solar radiation increases
            """)
        
        # Key insights
        correlations = country_stats.get('correlations', {})
        if correlations:
            st.subheader("🔍 Key Findings")
            
            # Find strongest correlations
            strong_corrs = []
            for var1 in correlations:
                for var2 in correlations[var1]:
                    if var1 < var2:  # Avoid duplicates
                        corr_value = correlations[var1][var2]
                        if abs(corr_value) > 0.5 and abs(corr_value) < 0.999:  # Exclude self-correlation
                            strong_corrs.append((var1, var2, corr_value))
            
            if strong_corrs:
                strong_corrs.sort(key=lambda x: abs(x[2]), reverse=True)
                
                st.markdown("**Strongest Correlations:**")
                for var1, var2, corr in strong_corrs[:5]:
                    direction = "positive" if corr > 0 else "negative"
                    st.write(f"- **{var1}** ↔ **{var2}**: {corr:.3f} ({direction})")
    else:
        st.warning("No correlation data available for this country")
