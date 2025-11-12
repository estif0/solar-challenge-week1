"""
Visualization Utilities

This module provides reusable plotting functions for solar radiation data analysis.
It includes functions for:
- Time series plots
- Distribution plots (histograms, box plots, violin plots)
- Correlation analysis (heatmaps, pair plots)
- Comparative plots across countries
- Solar-specific visualizations

All functions use consistent styling and return matplotlib figure objects
for flexibility.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List, Optional, Tuple, Dict
import warnings

# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class SolarVisualizer:
    """
    A collection of visualization methods for solar radiation data.
    
    This class provides consistent, reusable plotting functions with
    sensible defaults for solar data analysis.
    
    Parameters
    ----------
    style : str, default 'whitegrid'
        Seaborn style: 'whitegrid', 'darkgrid', 'white', 'dark', 'ticks'
    palette : str, default 'husl'
        Color palette for plots
    """
    
    def __init__(self, style: str = 'whitegrid', palette: str = 'husl'):
        """Initialize visualizer with style preferences."""
        sns.set_style(style)
        self.palette = palette
    
    def plot_time_series(
        self,
        df: pd.DataFrame,
        columns: Union[str, List[str]],
        time_column: str = 'Timestamp',
        title: Optional[str] = None,
        ylabel: Optional[str] = None,
        figsize: Tuple[int, int] = (14, 6),
        alpha: float = 0.7
    ) -> plt.Figure:
        """
        Plot time series data for one or more columns.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data
        columns : str or List[str]
            Column name(s) to plot
        time_column : str, default 'Timestamp'
            Name of the time/datetime column
        title : str, optional
            Plot title
        ylabel : str, optional
            Y-axis label
        figsize : Tuple[int, int], default (14, 6)
            Figure size (width, height)
        alpha : float, default 0.7
            Line transparency
            
        Returns
        -------
        plt.Figure
            The created figure
            
        Examples
        --------
        >>> viz = SolarVisualizer()
        >>> fig = viz.plot_time_series(df, ['GHI', 'DNI', 'DHI'])
        >>> plt.show()
        """
        if isinstance(columns, str):
            columns = [columns]
        
        fig, ax = plt.subplots(figsize=figsize)
        
        for col in columns:
            if col not in df.columns:
                warnings.warn(f"Column '{col}' not found, skipping")
                continue
            ax.plot(df[time_column], df[col], label=col, alpha=alpha)
        
        ax.set_xlabel(time_column)
        ax.set_ylabel(ylabel or 'Value')
        ax.set_title(title or f'Time Series: {", ".join(columns)}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def plot_distribution(
        self,
        df: pd.DataFrame,
        column: str,
        kind: str = 'hist',
        bins: int = 50,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """
        Plot distribution of a single column.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data
        column : str
            Column name to plot
        kind : str, default 'hist'
            Type of plot: 'hist', 'kde', 'box', or 'violin'
        bins : int, default 50
            Number of bins for histogram
        title : str, optional
            Plot title
        figsize : Tuple[int, int], default (10, 6)
            Figure size
            
        Returns
        -------
        plt.Figure
            The created figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        data = df[column].dropna()
        
        if kind == 'hist':
            ax.hist(data, bins=bins, edgecolor='black', alpha=0.7)
            ax.set_ylabel('Frequency')
        elif kind == 'kde':
            data.plot(kind='kde', ax=ax)
            ax.set_ylabel('Density')
        elif kind == 'box':
            ax.boxplot(data, vert=True)
            ax.set_ylabel(column)
        elif kind == 'violin':
            parts = ax.violinplot([data], vert=True, showmeans=True, showmedians=True)
            ax.set_ylabel(column)
        else:
            raise ValueError(f"Unknown kind '{kind}'. Use 'hist', 'kde', 'box', or 'violin'")
        
        ax.set_xlabel(column)
        ax.set_title(title or f'Distribution of {column}')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return fig
    
    def plot_correlation_heatmap(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'pearson',
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 8),
        annot: bool = True,
        cmap: str = 'coolwarm'
    ) -> plt.Figure:
        """
        Plot correlation heatmap for numeric columns.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data
        columns : List[str], optional
            Specific columns to include. If None, uses all numeric columns
        method : str, default 'pearson'
            Correlation method: 'pearson', 'spearman', or 'kendall'
        title : str, optional
            Plot title
        figsize : Tuple[int, int], default (10, 8)
            Figure size
        annot : bool, default True
            Whether to annotate cells with correlation values
        cmap : str, default 'coolwarm'
            Colormap name
            
        Returns
        -------
        plt.Figure
            The created figure
        """
        if columns is None:
            # Use all numeric columns
            data = df.select_dtypes(include=[np.number])
        else:
            data = df[columns]
        
        corr = data.corr(method=method)
        
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(
            corr,
            annot=annot,
            fmt='.2f',
            cmap=cmap,
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        
        ax.set_title(title or f'{method.capitalize()} Correlation Heatmap')
        plt.tight_layout()
        
        return fig
    
    def plot_comparison(
        self,
        data_dict: Dict[str, pd.DataFrame],
        column: str,
        agg_func: str = 'mean',
        kind: str = 'bar',
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """
        Compare a metric across multiple datasets (e.g., countries).
        
        Parameters
        ----------
        data_dict : Dict[str, pd.DataFrame]
            Dictionary with labels as keys and DataFrames as values
        column : str
            Column to compare
        agg_func : str, default 'mean'
            Aggregation function: 'mean', 'median', 'sum', 'std', etc.
        kind : str, default 'bar'
            Plot type: 'bar', 'barh', or 'line'
        title : str, optional
            Plot title
        figsize : Tuple[int, int], default (10, 6)
            Figure size
            
        Returns
        -------
        plt.Figure
            The created figure
        """
        # Calculate aggregated values
        values = {}
        for label, df in data_dict.items():
            if column in df.columns:
                values[label] = df[column].agg(agg_func)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        labels = list(values.keys())
        vals = list(values.values())
        
        if kind == 'bar':
            ax.bar(labels, vals, color=sns.color_palette(self.palette, len(labels)))
        elif kind == 'barh':
            ax.barh(labels, vals, color=sns.color_palette(self.palette, len(labels)))
        else:
            ax.plot(labels, vals, marker='o', linewidth=2, markersize=8)
            ax.grid(True, alpha=0.3)
        
        ax.set_title(title or f'{agg_func.capitalize()} {column} Comparison')
        ax.set_ylabel(column if kind != 'barh' else '')
        ax.set_xlabel('' if kind != 'barh' else column)
        plt.tight_layout()
        
        return fig
    
    def plot_monthly_pattern(
        self,
        df: pd.DataFrame,
        column: str,
        time_column: str = 'Timestamp',
        agg_func: str = 'mean',
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 6)
    ) -> plt.Figure:
        """
        Plot monthly aggregated patterns.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data
        column : str
            Column to analyze
        time_column : str, default 'Timestamp'
            Name of datetime column
        agg_func : str, default 'mean'
            Aggregation function
        title : str, optional
            Plot title
        figsize : Tuple[int, int], default (12, 6)
            Figure size
            
        Returns
        -------
        plt.Figure
            The created figure
        """
        # Extract month and aggregate
        df_copy = df.copy()
        df_copy['Month'] = pd.to_datetime(df_copy[time_column]).dt.month
        monthly_data = df_copy.groupby('Month')[column].agg(agg_func)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        ax.plot(monthly_data.index, monthly_data.values, marker='o', linewidth=2, markersize=8)
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(months)
        ax.set_xlabel('Month')
        ax.set_ylabel(f'{agg_func.capitalize()} {column}')
        ax.set_title(title or f'Monthly Pattern: {column}')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return fig
    
    def plot_daily_pattern(
        self,
        df: pd.DataFrame,
        column: str,
        time_column: str = 'Timestamp',
        agg_func: str = 'mean',
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 6)
    ) -> plt.Figure:
        """
        Plot hourly/daily aggregated patterns.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data
        column : str
            Column to analyze
        time_column : str, default 'Timestamp'
            Name of datetime column
        agg_func : str, default 'mean'
            Aggregation function
        title : str, optional
            Plot title
        figsize : Tuple[int, int], default (12, 6)
            Figure size
            
        Returns
        -------
        plt.Figure
            The created figure
        """
        # Extract hour and aggregate
        df_copy = df.copy()
        df_copy['Hour'] = pd.to_datetime(df_copy[time_column]).dt.hour
        hourly_data = df_copy.groupby('Hour')[column].agg(agg_func)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(hourly_data.index, hourly_data.values, marker='o', linewidth=2, markersize=6)
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel(f'{agg_func.capitalize()} {column}')
        ax.set_title(title or f'Daily Pattern: {column}')
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return fig
    
    def plot_box_comparison(
        self,
        data_dict: Dict[str, pd.DataFrame],
        column: str,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """
        Create box plots comparing a column across multiple datasets.
        
        Parameters
        ----------
        data_dict : Dict[str, pd.DataFrame]
            Dictionary with labels as keys and DataFrames as values
        column : str
            Column to compare
        title : str, optional
            Plot title
        figsize : Tuple[int, int], default (10, 6)
            Figure size
            
        Returns
        -------
        plt.Figure
            The created figure
        """
        # Prepare data for box plot
        data_list = []
        labels = []
        
        for label, df in data_dict.items():
            if column in df.columns:
                data_list.append(df[column].dropna())
                labels.append(label)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        bp = ax.boxplot(data_list, labels=labels, patch_artist=True)
        
        # Color the boxes
        colors = sns.color_palette(self.palette, len(data_list))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel(column)
        ax.set_title(title or f'Box Plot Comparison: {column}')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return fig
    
    def plot_scatter(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        hue_column: Optional[str] = None,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6),
        alpha: float = 0.6
    ) -> plt.Figure:
        """
        Create scatter plot with optional color grouping.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data
        x_column : str
            Column for x-axis
        y_column : str
            Column for y-axis
        hue_column : str, optional
            Column for color grouping
        title : str, optional
            Plot title
        figsize : Tuple[int, int], default (10, 6)
            Figure size
        alpha : float, default 0.6
            Point transparency
            
        Returns
        -------
        plt.Figure
            The created figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if hue_column:
            for category in df[hue_column].unique():
                mask = df[hue_column] == category
                ax.scatter(
                    df.loc[mask, x_column],
                    df.loc[mask, y_column],
                    label=category,
                    alpha=alpha,
                    s=20
                )
            ax.legend()
        else:
            ax.scatter(df[x_column], df[y_column], alpha=alpha, s=20)
        
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(title or f'{y_column} vs {x_column}')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return fig


# Convenience functions

def quick_time_series(
    df: pd.DataFrame,
    columns: Union[str, List[str]],
    time_column: str = 'Timestamp',
    title: Optional[str] = None
) -> plt.Figure:
    """
    Quick time series plot with default settings.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    columns : str or List[str]
        Column(s) to plot
    time_column : str, default 'Timestamp'
        Name of time column
    title : str, optional
        Plot title
        
    Returns
    -------
    plt.Figure
        The created figure
    """
    viz = SolarVisualizer()
    return viz.plot_time_series(df, columns, time_column, title)


def quick_distribution(
    df: pd.DataFrame,
    column: str,
    kind: str = 'hist',
    title: Optional[str] = None
) -> plt.Figure:
    """
    Quick distribution plot with default settings.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    column : str
        Column to plot
    kind : str, default 'hist'
        Plot type: 'hist', 'kde', 'box', or 'violin'
    title : str, optional
        Plot title
        
    Returns
    -------
    plt.Figure
        The created figure
    """
    viz = SolarVisualizer()
    return viz.plot_distribution(df, column, kind, title=title)


def quick_correlation(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: Optional[str] = None
) -> plt.Figure:
    """
    Quick correlation heatmap with default settings.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    columns : List[str], optional
        Columns to include
    title : str, optional
        Plot title
        
    Returns
    -------
    plt.Figure
        The created figure
    """
    viz = SolarVisualizer()
    return viz.plot_correlation_heatmap(df, columns, title=title)
