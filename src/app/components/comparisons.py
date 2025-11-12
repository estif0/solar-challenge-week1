"""
Comparisons Component

Displays cross-country comparisons and statistical tests.
"""

import streamlit as st
from typing import Dict, Any
from ..utils.chart_builder import create_metric_comparison_chart, create_box_plot_comparison
from ..config import COUNTRIES


def render_comparisons(stats: Dict[str, Any]):
    """
    Render cross-country comparison section.
    
    Parameters
    ----------
    stats : Dict
        Complete statistics dictionary
    """
    st.header("🌍 Cross-Country Comparison")
    
    st.markdown("""
    Compare solar radiation characteristics across all three locations.
    """)
    
    # Mean comparison
    st.subheader("📊 Average Solar Irradiance Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = create_metric_comparison_chart(stats, 'GHI', 'mean')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = create_metric_comparison_chart(stats, 'DNI', 'mean')
        st.plotly_chart(fig, width='stretch')
    
    with col3:
        fig = create_metric_comparison_chart(stats, 'DHI', 'mean')
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # Distribution comparison
    st.subheader("📦 Distribution Comparison")
    
    metric_select = st.selectbox(
        "Select metric to compare:",
        options=['GHI', 'DNI', 'DHI'],
        format_func=lambda x: {
            'GHI': 'Global Horizontal Irradiance',
            'DNI': 'Direct Normal Irradiance',
            'DHI': 'Diffuse Horizontal Irradiance'
        }[x]
    )
    
    fig = create_box_plot_comparison(stats, metric_select)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # Statistical tests
    st.subheader("📈 Statistical Significance Tests")
    
    st.markdown("""
    ANOVA (Analysis of Variance) tests whether the mean values differ significantly 
    across countries. A **p-value < 0.05** indicates statistically significant differences.
    """)
    
    comparison_data = stats.get('comparison', {})
    
    # Display ANOVA results
    for metric in ['GHI', 'DNI', 'DHI']:
        if metric in comparison_data and 'anova' in comparison_data[metric]:
            anova = comparison_data[metric]['anova']
            
            with st.expander(f"🔬 ANOVA Results for {metric}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "F-Statistic",
                        f"{anova['f_statistic']:.4f}",
                        help="Ratio of variance between groups to variance within groups"
                    )
                
                with col2:
                    st.metric(
                        "P-Value",
                        f"{anova['p_value']:.6f}",
                        help="Probability that differences are due to chance"
                    )
                
                with col3:
                    is_significant = anova['significant']
                    st.metric(
                        "Significant?",
                        "Yes ✓" if is_significant else "No ✗",
                        help="Are the differences statistically significant? (α = 0.05)"
                    )
                
                # Interpretation
                st.markdown("**Interpretation:**")
                st.info(anova['interpretation'])
    
    st.markdown("---")
    
    # Summary comparison table
    st.subheader("📋 Summary Comparison Table")
    
    if 'solar_potential' in comparison_data:
        import pandas as pd
        
        # Convert to DataFrame - countries as rows, metrics as columns
        potential_df = pd.DataFrame(comparison_data['solar_potential'])
        
        # Select key metrics to display
        key_metrics = ['mean_ghi', 'mean_dni', 'mean_dhi', 
                      'annual_ghi_kwh_m2', 'mean_daily_energy_kwh_m2',
                      'peak_sun_hours', 'mean_clearness_index']
        
        available_metrics = [m for m in key_metrics if m in potential_df.columns]
        
        if available_metrics:
            display_df = potential_df[available_metrics].round(2)
            
            # Rename columns (metrics) for better display
            display_df.columns = [
                metric.replace('_', ' ').title() 
                for metric in display_df.columns
            ]
            
            # Rename index (countries) for better display
            display_df.index = [
                COUNTRIES.get(country.lower(), {}).get('name', country)
                for country in display_df.index
            ]
            
            st.dataframe(display_df, width='stretch')
            
            # Ranking
            st.markdown("#### 🏆 Rankings")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Best for GHI:**")
                best_ghi_country = potential_df['mean_ghi'].idxmax()
                country_info = COUNTRIES.get(best_ghi_country.lower(), {})
                st.success(f"{country_info.get('flag', '')} {country_info.get('name', best_ghi_country)}")
            
            with col2:
                st.markdown("**Best for DNI:**")
                best_dni_country = potential_df['mean_dni'].idxmax()
                country_info = COUNTRIES.get(best_dni_country.lower(), {})
                st.success(f"{country_info.get('flag', '')} {country_info.get('name', best_dni_country)}")
            
            with col3:
                st.markdown("**Best Annual Energy:**")
                best_annual_country = potential_df['annual_ghi_kwh_m2'].idxmax()
                country_info = COUNTRIES.get(best_annual_country.lower(), {})
                st.success(f"{country_info.get('flag', '')} {country_info.get('name', best_annual_country)}")
        else:
            st.warning("No solar potential metrics available")
    else:
        st.warning("Solar potential comparison data not available")
