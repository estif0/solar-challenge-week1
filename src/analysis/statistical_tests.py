"""
Statistical Testing Utilities

This module provides statistical analysis functions for solar radiation data,
including:
- Normality tests
- Correlation analysis with significance testing
- T-tests and ANOVA for group comparisons
- Chi-square tests
- Non-parametric alternatives

All functions return structured results with test statistics and p-values.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union
import warnings


class StatisticalAnalyzer:
    """
    Performs statistical tests and analysis on solar radiation data.
    
    This class provides methods for hypothesis testing, correlation analysis,
    and comparative statistics across groups.
    
    Parameters
    ----------
    significance_level : float, default 0.05
        Significance level (alpha) for hypothesis tests
    """
    
    def __init__(self, significance_level: float = 0.05):
        """Initialize analyzer with significance level."""
        self.alpha = significance_level
    
    def test_normality(
        self,
        data: Union[pd.Series, np.ndarray],
        method: str = 'shapiro'
    ) -> Dict[str, any]:
        """
        Test if data follows a normal distribution.
        
        Parameters
        ----------
        data : pd.Series or np.ndarray
            Data to test
        method : str, default 'shapiro'
            Test method: 'shapiro', 'kstest', or 'anderson'
            
        Returns
        -------
        Dict
            Dictionary with test results including statistic, p-value, and conclusion
            
        Examples
        --------
        >>> analyzer = StatisticalAnalyzer()
        >>> result = analyzer.test_normality(df['GHI'])
        >>> print(result['is_normal'])
        """
        if isinstance(data, pd.Series):
            data = data.dropna().values
        else:
            data = data[~np.isnan(data)]
        
        if len(data) < 3:
            return {
                'method': method,
                'error': 'Insufficient data for normality test (n < 3)'
            }
        
        result = {'method': method}
        
        try:
            if method == 'shapiro':
                # Shapiro-Wilk test
                if len(data) > 5000:
                    # Sample for large datasets
                    data = np.random.choice(data, 5000, replace=False)
                    result['note'] = 'Used sample of 5000 points for efficiency'
                
                statistic, p_value = stats.shapiro(data)
                result['statistic'] = float(statistic)
                result['p_value'] = float(p_value)
                result['is_normal'] = p_value > self.alpha
                result['interpretation'] = (
                    f"Data {'appears' if result['is_normal'] else 'does not appear'} "
                    f"to be normally distributed (p={p_value:.4f})"
                )
            
            elif method == 'kstest':
                # Kolmogorov-Smirnov test
                statistic, p_value = stats.kstest(data, 'norm')
                result['statistic'] = float(statistic)
                result['p_value'] = float(p_value)
                result['is_normal'] = p_value > self.alpha
                result['interpretation'] = (
                    f"Data {'appears' if result['is_normal'] else 'does not appear'} "
                    f"to be normally distributed (p={p_value:.4f})"
                )
            
            elif method == 'anderson':
                # Anderson-Darling test
                anderson_result = stats.anderson(data)
                result['statistic'] = float(anderson_result.statistic)
                result['critical_values'] = anderson_result.critical_values.tolist()
                result['significance_levels'] = anderson_result.significance_level.tolist()
                # Check at our alpha level (usually 5%)
                idx = 2  # 5% level
                result['is_normal'] = anderson_result.statistic < anderson_result.critical_values[idx]
                result['interpretation'] = (
                    f"Data {'appears' if result['is_normal'] else 'does not appear'} "
                    f"to be normally distributed at {anderson_result.significance_level[idx]}% level"
                )
            else:
                result['error'] = f"Unknown method '{method}'"
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def correlation_analysis(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'pearson'
    ) -> Dict[str, pd.DataFrame]:
        """
        Perform correlation analysis with significance testing.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data
        columns : List[str], optional
            Columns to include. If None, uses all numeric columns
        method : str, default 'pearson'
            Correlation method: 'pearson', 'spearman', or 'kendall'
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionary with 'correlation' matrix and 'p_values' matrix
            
        Examples
        --------
        >>> analyzer = StatisticalAnalyzer()
        >>> result = analyzer.correlation_analysis(df, columns=['GHI', 'DNI', 'DHI'])
        >>> print(result['correlation'])
        >>> print(result['p_values'])
        """
        if columns is None:
            data = df.select_dtypes(include=[np.number])
        else:
            data = df[columns]
        
        n_vars = len(data.columns)
        corr_matrix = np.zeros((n_vars, n_vars))
        p_matrix = np.zeros((n_vars, n_vars))
        
        for i, col1 in enumerate(data.columns):
            for j, col2 in enumerate(data.columns):
                if i == j:
                    corr_matrix[i, j] = 1.0
                    p_matrix[i, j] = 0.0
                elif i > j:
                    # Already computed
                    corr_matrix[i, j] = corr_matrix[j, i]
                    p_matrix[i, j] = p_matrix[j, i]
                else:
                    # Remove NaN values
                    mask = ~(data[col1].isna() | data[col2].isna())
                    x = data.loc[mask, col1].values
                    y = data.loc[mask, col2].values
                    
                    if len(x) < 3:
                        corr_matrix[i, j] = np.nan
                        p_matrix[i, j] = np.nan
                        continue
                    
                    if method == 'pearson':
                        corr, p_val = stats.pearsonr(x, y)
                    elif method == 'spearman':
                        corr, p_val = stats.spearmanr(x, y)
                    elif method == 'kendall':
                        corr, p_val = stats.kendalltau(x, y)
                    else:
                        raise ValueError(f"Unknown method '{method}'")
                    
                    corr_matrix[i, j] = corr
                    p_matrix[i, j] = p_val
        
        corr_df = pd.DataFrame(corr_matrix, index=data.columns, columns=data.columns)
        p_df = pd.DataFrame(p_matrix, index=data.columns, columns=data.columns)
        
        return {
            'correlation': corr_df,
            'p_values': p_df,
            'method': method,
            'significant_at_alpha': (p_df < self.alpha).sum().sum() // 2  # Divide by 2 for symmetry
        }
    
    def ttest_independent(
        self,
        group1: Union[pd.Series, np.ndarray],
        group2: Union[pd.Series, np.ndarray],
        equal_var: bool = True
    ) -> Dict[str, any]:
        """
        Perform independent samples t-test.
        
        Parameters
        ----------
        group1 : pd.Series or np.ndarray
            First group data
        group2 : pd.Series or np.ndarray
            Second group data
        equal_var : bool, default True
            Whether to assume equal variances (Welch's t-test if False)
            
        Returns
        -------
        Dict
            Test results with statistic, p-value, and interpretation
            
        Examples
        --------
        >>> analyzer = StatisticalAnalyzer()
        >>> result = analyzer.ttest_independent(benin_ghi, togo_ghi)
        >>> print(result['significant_difference'])
        """
        if isinstance(group1, pd.Series):
            group1 = group1.dropna().values
        if isinstance(group2, pd.Series):
            group2 = group2.dropna().values
        
        statistic, p_value = stats.ttest_ind(group1, group2, equal_var=equal_var)
        
        result = {
            'test': "Welch's t-test" if not equal_var else "Student's t-test",
            'statistic': float(statistic),
            'p_value': float(p_value),
            'significant_difference': p_value < self.alpha,
            'group1_mean': float(np.mean(group1)),
            'group2_mean': float(np.mean(group2)),
            'group1_std': float(np.std(group1, ddof=1)),
            'group2_std': float(np.std(group2, ddof=1)),
            'interpretation': (
                f"{'Significant' if p_value < self.alpha else 'No significant'} "
                f"difference between groups (p={p_value:.4f})"
            )
        }
        
        return result
    
    def anova_oneway(
        self,
        *groups: Union[pd.Series, np.ndarray],
        group_names: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Perform one-way ANOVA test.
        
        Parameters
        ----------
        *groups : pd.Series or np.ndarray
            Multiple groups to compare
        group_names : List[str], optional
            Names for the groups
            
        Returns
        -------
        Dict
            Test results with F-statistic, p-value, and group statistics
            
        Examples
        --------
        >>> analyzer = StatisticalAnalyzer()
        >>> result = analyzer.anova_oneway(
        ...     benin_ghi, togo_ghi, sierra_ghi,
        ...     group_names=['Benin', 'Togo', 'Sierra Leone']
        ... )
        >>> print(result['significant_difference'])
        """
        # Clean data
        cleaned_groups = []
        for group in groups:
            if isinstance(group, pd.Series):
                cleaned_groups.append(group.dropna().values)
            else:
                cleaned_groups.append(group[~np.isnan(group)])
        
        # Perform ANOVA
        statistic, p_value = stats.f_oneway(*cleaned_groups)
        
        result = {
            'test': 'One-way ANOVA',
            'f_statistic': float(statistic),
            'p_value': float(p_value),
            'significant_difference': p_value < self.alpha,
            'num_groups': len(groups),
            'interpretation': (
                f"{'Significant' if p_value < self.alpha else 'No significant'} "
                f"difference among groups (p={p_value:.4f})"
            )
        }
        
        # Add group statistics
        if group_names is None:
            group_names = [f"Group {i+1}" for i in range(len(groups))]
        
        group_stats = {}
        for name, group in zip(group_names, cleaned_groups):
            group_stats[name] = {
                'mean': float(np.mean(group)),
                'std': float(np.std(group, ddof=1)),
                'n': len(group)
            }
        
        result['group_statistics'] = group_stats
        
        return result
    
    def kruskal_wallis(
        self,
        *groups: Union[pd.Series, np.ndarray],
        group_names: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Perform Kruskal-Wallis H-test (non-parametric alternative to ANOVA).
        
        Parameters
        ----------
        *groups : pd.Series or np.ndarray
            Multiple groups to compare
        group_names : List[str], optional
            Names for the groups
            
        Returns
        -------
        Dict
            Test results with H-statistic and p-value
            
        Examples
        --------
        >>> analyzer = StatisticalAnalyzer()
        >>> result = analyzer.kruskal_wallis(benin_ghi, togo_ghi, sierra_ghi)
        """
        # Clean data
        cleaned_groups = []
        for group in groups:
            if isinstance(group, pd.Series):
                cleaned_groups.append(group.dropna().values)
            else:
                cleaned_groups.append(group[~np.isnan(group)])
        
        # Perform test
        statistic, p_value = stats.kruskal(*cleaned_groups)
        
        result = {
            'test': 'Kruskal-Wallis H-test',
            'h_statistic': float(statistic),
            'p_value': float(p_value),
            'significant_difference': p_value < self.alpha,
            'num_groups': len(groups),
            'interpretation': (
                f"{'Significant' if p_value < self.alpha else 'No significant'} "
                f"difference among groups (p={p_value:.4f})"
            )
        }
        
        # Add group statistics
        if group_names is None:
            group_names = [f"Group {i+1}" for i in range(len(groups))]
        
        group_stats = {}
        for name, group in zip(group_names, cleaned_groups):
            group_stats[name] = {
                'median': float(np.median(group)),
                'mean': float(np.mean(group)),
                'n': len(group)
            }
        
        result['group_statistics'] = group_stats
        
        return result
    
    def mann_whitney_u(
        self,
        group1: Union[pd.Series, np.ndarray],
        group2: Union[pd.Series, np.ndarray],
        alternative: str = 'two-sided'
    ) -> Dict[str, any]:
        """
        Perform Mann-Whitney U test (non-parametric alternative to t-test).
        
        Parameters
        ----------
        group1 : pd.Series or np.ndarray
            First group data
        group2 : pd.Series or np.ndarray
            Second group data
        alternative : str, default 'two-sided'
            Alternative hypothesis: 'two-sided', 'less', or 'greater'
            
        Returns
        -------
        Dict
            Test results with U-statistic and p-value
        """
        if isinstance(group1, pd.Series):
            group1 = group1.dropna().values
        if isinstance(group2, pd.Series):
            group2 = group2.dropna().values
        
        statistic, p_value = stats.mannwhitneyu(group1, group2, alternative=alternative)
        
        result = {
            'test': 'Mann-Whitney U test',
            'u_statistic': float(statistic),
            'p_value': float(p_value),
            'alternative': alternative,
            'significant_difference': p_value < self.alpha,
            'group1_median': float(np.median(group1)),
            'group2_median': float(np.median(group2)),
            'interpretation': (
                f"{'Significant' if p_value < self.alpha else 'No significant'} "
                f"difference between groups (p={p_value:.4f})"
            )
        }
        
        return result


# Convenience functions

def compare_groups(
    data_dict: Dict[str, Union[pd.Series, np.ndarray]],
    parametric: bool = True,
    significance_level: float = 0.05
) -> Dict[str, any]:
    """
    Compare multiple groups using appropriate test.
    
    Parameters
    ----------
    data_dict : Dict[str, pd.Series or np.ndarray]
        Dictionary with group names as keys and data as values
    parametric : bool, default True
        Whether to use parametric (ANOVA) or non-parametric (Kruskal-Wallis) test
    significance_level : float, default 0.05
        Significance level for testing
        
    Returns
    -------
    Dict
        Test results
        
    Examples
    --------
    >>> data = {'Benin': benin_ghi, 'Togo': togo_ghi, 'Sierra Leone': sierra_ghi}
    >>> result = compare_groups(data, parametric=True)
    >>> print(result['interpretation'])
    """
    analyzer = StatisticalAnalyzer(significance_level=significance_level)
    
    group_names = list(data_dict.keys())
    groups = list(data_dict.values())
    
    if parametric:
        return analyzer.anova_oneway(*groups, group_names=group_names)
    else:
        return analyzer.kruskal_wallis(*groups, group_names=group_names)


def quick_correlation_test(
    x: Union[pd.Series, np.ndarray],
    y: Union[pd.Series, np.ndarray],
    method: str = 'pearson'
) -> Dict[str, any]:
    """
    Quick correlation test between two variables.
    
    Parameters
    ----------
    x : pd.Series or np.ndarray
        First variable
    y : pd.Series or np.ndarray
        Second variable
    method : str, default 'pearson'
        Correlation method: 'pearson', 'spearman', or 'kendall'
        
    Returns
    -------
    Dict
        Correlation coefficient and p-value
        
    Examples
    --------
    >>> result = quick_correlation_test(df['GHI'], df['Tamb'])
    >>> print(f"Correlation: {result['correlation']:.3f}, p-value: {result['p_value']:.4f}")
    """
    if isinstance(x, pd.Series):
        x = x.values
    if isinstance(y, pd.Series):
        y = y.values
    
    # Remove NaN pairs
    mask = ~(np.isnan(x) | np.isnan(y))
    x = x[mask]
    y = y[mask]
    
    if method == 'pearson':
        corr, p_val = stats.pearsonr(x, y)
    elif method == 'spearman':
        corr, p_val = stats.spearmanr(x, y)
    elif method == 'kendall':
        corr, p_val = stats.kendalltau(x, y)
    else:
        raise ValueError(f"Unknown method '{method}'")
    
    return {
        'method': method,
        'correlation': float(corr),
        'p_value': float(p_val),
        'significant': p_val < 0.05,
        'interpretation': (
            f"{method.capitalize()} correlation: {corr:.3f} "
            f"({'significant' if p_val < 0.05 else 'not significant'}, p={p_val:.4f})"
        )
    }


def summary_statistics(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    group_by: Optional[str] = None
) -> pd.DataFrame:
    """
    Generate comprehensive summary statistics.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to analyze
    columns : List[str], optional
        Columns to include. If None, uses all numeric columns
    group_by : str, optional
        Column to group by
        
    Returns
    -------
    pd.DataFrame
        Summary statistics table
        
    Examples
    --------
    >>> stats_df = summary_statistics(df, columns=['GHI', 'DNI', 'DHI'])
    >>> print(stats_df)
    """
    if columns is None:
        data = df.select_dtypes(include=[np.number])
    else:
        data = df[columns]
    
    if group_by:
        summary = data.groupby(df[group_by]).agg([
            'count', 'mean', 'std', 'min', 
            ('25%', lambda x: x.quantile(0.25)),
            ('50%', lambda x: x.quantile(0.50)),
            ('75%', lambda x: x.quantile(0.75)),
            'max'
        ])
    else:
        summary = data.agg([
            'count', 'mean', 'std', 'min',
            lambda x: x.quantile(0.25),
            lambda x: x.quantile(0.50),
            lambda x: x.quantile(0.75),
            'max'
        ])
        summary.index = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    
    return summary
