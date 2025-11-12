"""
Chart Builder for Dashboard

This module creates Plotly charts from the pre-computed statistics.
All charts are interactive and follow a consistent style.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import numpy as np

from ..config import COUNTRIES, SOLAR_METRICS, CHART_HEIGHT, CHART_TEMPLATE, MONTHS


def create_metric_comparison_chart(
    stats: Dict[str, Any],
    metric: str,
    stat_type: str = 'mean'
) -> go.Figure:
    """
    Create a bar chart comparing a metric across countries.
    
    Parameters
    ----------
    stats : Dict
        Statistics dictionary
    metric : str
        Metric to compare (e.g., 'GHI', 'DNI', 'DHI')
    stat_type : str
        Type of statistic ('mean', 'median', 'max', etc.)
        
    Returns
    -------
    go.Figure
        Plotly bar chart
    """
    countries = []
    values = []
    colors = []
    
    for country_key, country_data in stats['countries'].items():
        if metric in country_data.get('solar_irradiance', {}):
            countries.append(COUNTRIES[country_key]['name'])
            values.append(country_data['solar_irradiance'][metric][stat_type])
            colors.append(COUNTRIES[country_key]['color'])
    
    fig = go.Figure(data=[
        go.Bar(
            x=countries,
            y=values,
            marker_color=colors,
            text=[f"{v:.2f}" for v in values],
            textposition='outside'
        )
    ])
    
    metric_info = SOLAR_METRICS.get(metric, {})
    fig.update_layout(
        title=f"{stat_type.capitalize()} {metric_info.get('name', metric)}",
        xaxis_title="Country",
        yaxis_title=f"{metric} ({metric_info.get('unit', 'W/m²')})",
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        showlegend=False
    )
    
    return fig


def create_monthly_pattern_chart(
    country_stats: Dict[str, Any],
    metric: str = 'GHI'
) -> go.Figure:
    """
    Create a line chart showing monthly patterns.
    
    Parameters
    ----------
    country_stats : Dict
        Country-specific statistics
    metric : str
        Metric to display
        
    Returns
    -------
    go.Figure
        Plotly line chart
    """
    monthly_data = country_stats.get('temporal_patterns', {}).get('monthly', {}).get(metric, {})
    
    if not monthly_data:
        return go.Figure()
    
    means = monthly_data.get('mean', {})
    maxs = monthly_data.get('max', {})
    
    # Convert string keys to integers for proper sorting
    months_int = sorted([int(k) for k in means.keys()])
    
    fig = go.Figure()
    
    # Mean line
    fig.add_trace(go.Scatter(
        x=[MONTHS[m-1] for m in months_int],
        y=[means[str(m)] for m in months_int],
        mode='lines+markers',
        name='Mean',
        line=dict(width=3, color=SOLAR_METRICS[metric]['color'])
    ))
    
    # Max line
    fig.add_trace(go.Scatter(
        x=[MONTHS[m-1] for m in months_int],
        y=[maxs[str(m)] for m in months_int],
        mode='lines',
        name='Maximum',
        line=dict(width=2, dash='dash', color=SOLAR_METRICS[metric]['color']),
        opacity=0.6
    ))
    
    metric_info = SOLAR_METRICS.get(metric, {})
    fig.update_layout(
        title=f"Monthly {metric_info.get('name', metric)} Pattern",
        xaxis_title="Month",
        yaxis_title=f"{metric} ({metric_info.get('unit', 'W/m²')})",
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        hovermode='x unified'
    )
    
    return fig


def create_hourly_pattern_chart(
    country_stats: Dict[str, Any],
    metrics: List[str] = ['GHI', 'DNI', 'DHI']
) -> go.Figure:
    """
    Create a line chart showing hourly patterns for multiple metrics.
    
    Parameters
    ----------
    country_stats : Dict
        Country-specific statistics
    metrics : List[str]
        List of metrics to display
        
    Returns
    -------
    go.Figure
        Plotly line chart
    """
    fig = go.Figure()
    
    for metric in metrics:
        hourly_data = country_stats.get('temporal_patterns', {}).get('hourly', {}).get(metric, {})
        
        if not hourly_data:
            continue
        
        means = hourly_data.get('mean', {})
        hours = sorted([int(k) for k in means.keys()])
        
        fig.add_trace(go.Scatter(
            x=hours,
            y=[means[str(h)] for h in hours],
            mode='lines+markers',
            name=metric,
            line=dict(width=3, color=SOLAR_METRICS[metric]['color'])
        ))
    
    fig.update_layout(
        title="Daily Solar Irradiance Pattern (Average by Hour)",
        xaxis_title="Hour of Day",
        yaxis_title="Irradiance (W/m²)",
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE,
        hovermode='x unified'
    )
    
    return fig


def create_correlation_heatmap(
    country_stats: Dict[str, Any]
) -> go.Figure:
    """
    Create a correlation heatmap.
    
    Parameters
    ----------
    country_stats : Dict
        Country-specific statistics
        
    Returns
    -------
    go.Figure
        Plotly heatmap
    """
    correlations = country_stats.get('correlations', {})
    
    if not correlations:
        return go.Figure()
    
    # Get variables
    variables = list(correlations.keys())
    
    # Build correlation matrix
    n = len(variables)
    corr_matrix = np.zeros((n, n))
    
    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            corr_matrix[i, j] = correlations[var1].get(var2, 0)
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=variables,
        y=variables,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Variable Correlation Matrix",
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE
    )
    
    return fig


def create_box_plot_comparison(
    stats: Dict[str, Any],
    metric: str = 'GHI'
) -> go.Figure:
    """
    Create box plots comparing a metric across countries.
    
    Parameters
    ----------
    stats : Dict
        Statistics dictionary
    metric : str
        Metric to compare
        
    Returns
    -------
    go.Figure
        Plotly box plot
    """
    fig = go.Figure()
    
    for country_key, country_data in stats['countries'].items():
        metric_data = country_data.get('solar_irradiance', {}).get(metric, {})
        
        if not metric_data:
            continue
        
        # Create approximate box plot from statistics
        # This is a simplified version - real box plot would need raw data
        fig.add_trace(go.Box(
            name=COUNTRIES[country_key]['name'],
            y=[
                metric_data['min'],
                metric_data['q25'],
                metric_data['median'],
                metric_data['q75'],
                metric_data['max']
            ],
            marker_color=COUNTRIES[country_key]['color']
        ))
    
    metric_info = SOLAR_METRICS.get(metric, {})
    fig.update_layout(
        title=f"{metric_info.get('name', metric)} Distribution by Country",
        yaxis_title=f"{metric} ({metric_info.get('unit', 'W/m²')})",
        height=CHART_HEIGHT,
        template=CHART_TEMPLATE
    )
    
    return fig
