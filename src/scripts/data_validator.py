"""
Data Validator Script

This module validates the structural integrity and format consistency of data files.
It checks:
- File format (.csv)
- Column names and order
- Data types for each column
- File encoding
- Basic file structure (headers, delimiters)

Does NOT perform data quality analysis (missing values, outliers, etc.)
"""

import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys


class DataValidator:
    """
    Validates structural consistency of solar radiation data files.
    
    This validator ensures all data files conform to the expected schema
    without analyzing data quality or statistical properties.
    """
    
    # Expected schema for solar radiation datasets
    EXPECTED_SCHEMA = {
        'columns': [
            'Timestamp', 'GHI', 'DNI', 'DHI', 'ModA', 'ModB', 
            'Tamb', 'RH', 'WS', 'WSgust', 'WSstdev', 'WD', 'WDstdev',
            'BP', 'Cleaning', 'Precipitation', 'TModA', 'TModB', 'Comments'
        ],
        'dtypes': {
            'Timestamp': 'datetime',
            'GHI': 'numeric',
            'DNI': 'numeric',
            'DHI': 'numeric',
            'ModA': 'numeric',
            'ModB': 'numeric',
            'Tamb': 'numeric',
            'RH': 'numeric',
            'WS': 'numeric',
            'WSgust': 'numeric',
            'WSstdev': 'numeric',
            'WD': 'numeric',
            'WDstdev': 'numeric',
            'BP': 'numeric',
            'Cleaning': 'numeric',
            'Precipitation': 'numeric',
            'TModA': 'numeric',
            'TModB': 'numeric',
            'Comments': 'string'
        }
    }
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the DataValidator.
        
        Parameters
        ----------
        data_dir : str, optional
            Path to the data directory. If None, uses default path.
        """
        if data_dir is None:
            # Default to src/data directory
            script_dir = Path(__file__).parent.parent
            self.data_dir = script_dir / 'data'
        else:
            self.data_dir = Path(data_dir)
    
    def validate_file_format(self, filepath: Path) -> Tuple[bool, str]:
        """
        Check if file is a valid CSV file.
        
        Parameters
        ----------
        filepath : Path
            Path to the file to validate
            
        Returns
        -------
        Tuple[bool, str]
            (is_valid, message)
        """
        if not filepath.exists():
            return False, f"File does not exist: {filepath}"
        
        if filepath.suffix.lower() != '.csv':
            return False, f"File is not a CSV file: {filepath.suffix}"
        
        # Try to read first few lines to ensure it's a valid CSV
        try:
            pd.read_csv(filepath, nrows=5)
            return True, "Valid CSV format"
        except Exception as e:
            return False, f"Cannot read as CSV: {str(e)}"
    
    def validate_columns(self, filepath: Path) -> Tuple[bool, str]:
        """
        Check if file has the expected columns in the correct order.
        
        Parameters
        ----------
        filepath : Path
            Path to the file to validate
            
        Returns
        -------
        Tuple[bool, str]
            (is_valid, message)
        """
        try:
            df = pd.read_csv(filepath, nrows=0)  # Read only headers
            actual_columns = df.columns.tolist()
            expected_columns = self.EXPECTED_SCHEMA['columns']
            
            if actual_columns != expected_columns:
                missing = set(expected_columns) - set(actual_columns)
                extra = set(actual_columns) - set(expected_columns)
                
                msg = "Column mismatch:\n"
                if missing:
                    msg += f"  Missing columns: {missing}\n"
                if extra:
                    msg += f"  Extra columns: {extra}\n"
                if set(actual_columns) == set(expected_columns):
                    msg += f"  Columns are present but in wrong order\n"
                    msg += f"  Expected: {expected_columns}\n"
                    msg += f"  Got: {actual_columns}"
                
                return False, msg
            
            return True, "All columns present and in correct order"
        
        except Exception as e:
            return False, f"Error reading columns: {str(e)}"
    
    def validate_data_types(self, filepath: Path) -> Tuple[bool, str]:
        """
        Check if columns have compatible data types.
        
        Parameters
        ----------
        filepath : Path
            Path to the file to validate
            
        Returns
        -------
        Tuple[bool, str]
            (is_valid, message)
        """
        try:
            # Read small sample to check types
            df = pd.read_csv(filepath, nrows=100)
            
            issues = []
            
            for col, expected_type in self.EXPECTED_SCHEMA['dtypes'].items():
                if col not in df.columns:
                    continue
                
                if expected_type == 'datetime':
                    # Try to parse as datetime
                    try:
                        pd.to_datetime(df[col])
                    except Exception:
                        issues.append(f"{col}: Cannot parse as datetime")
                
                elif expected_type == 'numeric':
                    # Try to convert to numeric
                    try:
                        pd.to_numeric(df[col], errors='coerce')
                    except Exception:
                        issues.append(f"{col}: Cannot convert to numeric")
                
                elif expected_type == 'string':
                    # String columns are always compatible
                    pass
            
            if issues:
                return False, "Data type issues:\n  " + "\n  ".join(issues)
            
            return True, "All columns have compatible data types"
        
        except Exception as e:
            return False, f"Error checking data types: {str(e)}"
    
    def validate_file(self, filepath: Path) -> Dict[str, any]:
        """
        Run all validations on a single file.
        
        Parameters
        ----------
        filepath : Path
            Path to the file to validate
            
        Returns
        -------
        Dict
            Validation results with status and messages
        """
        result = {
            'filename': filepath.name,
            'path': str(filepath),
            'valid': True,
            'checks': {}
        }
        
        # Check file format
        is_valid, msg = self.validate_file_format(filepath)
        result['checks']['file_format'] = {'valid': is_valid, 'message': msg}
        if not is_valid:
            result['valid'] = False
            return result  # Stop if file format is invalid
        
        # Check columns
        is_valid, msg = self.validate_columns(filepath)
        result['checks']['columns'] = {'valid': is_valid, 'message': msg}
        if not is_valid:
            result['valid'] = False
        
        # Check data types
        is_valid, msg = self.validate_data_types(filepath)
        result['checks']['data_types'] = {'valid': is_valid, 'message': msg}
        if not is_valid:
            result['valid'] = False
        
        return result
    
    def validate_directory(self, subdir: str = 'raw') -> Dict[str, List]:
        """
        Validate all CSV files in a specific subdirectory.
        
        Parameters
        ----------
        subdir : str
            Subdirectory name ('raw', 'cleaned', 'processed', 'external')
            
        Returns
        -------
        Dict
            Summary of validation results
        """
        dir_path = self.data_dir / subdir
        
        if not dir_path.exists():
            return {
                'directory': str(dir_path),
                'error': 'Directory does not exist',
                'files_checked': 0,
                'files_valid': 0,
                'results': []
            }
        
        csv_files = list(dir_path.glob('*.csv'))
        results = []
        
        for filepath in csv_files:
            result = self.validate_file(filepath)
            results.append(result)
        
        valid_count = sum(1 for r in results if r['valid'])
        
        return {
            'directory': str(dir_path),
            'files_checked': len(results),
            'files_valid': valid_count,
            'all_valid': valid_count == len(results),
            'results': results
        }
    
    def print_validation_report(self, summary: Dict):
        """
        Print a formatted validation report.
        
        Parameters
        ----------
        summary : Dict
            Validation summary from validate_directory()
        """
        print(f"\n{'='*70}")
        print(f"DATA VALIDATION REPORT")
        print(f"{'='*70}")
        print(f"Directory: {summary['directory']}")
        print(f"Files checked: {summary['files_checked']}")
        print(f"Files valid: {summary['files_valid']}")
        print(f"Status: {'✓ ALL VALID' if summary.get('all_valid') else '✗ ISSUES FOUND'}")
        print(f"{'='*70}\n")
        
        for result in summary.get('results', []):
            status = "✓" if result['valid'] else "✗"
            print(f"{status} {result['filename']}")
            
            for check_name, check_result in result['checks'].items():
                check_status = "✓" if check_result['valid'] else "✗"
                print(f"  {check_status} {check_name}: {check_result['message']}")
            
            print()


def main():
    """
    Main function to run validation from command line.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate data file structure and format'
    )
    parser.add_argument(
        '--dir',
        type=str,
        default='raw',
        choices=['raw', 'cleaned', 'processed', 'external'],
        help='Data subdirectory to validate (default: raw)'
    )
    parser.add_argument(
        '--data-path',
        type=str,
        default=None,
        help='Path to data directory (default: src/data)'
    )
    
    args = parser.parse_args()
    
    validator = DataValidator(data_dir=args.data_path)
    summary = validator.validate_directory(subdir=args.dir)
    validator.print_validation_report(summary)
    
    # Exit with error code if validation failed
    if not summary.get('all_valid', False):
        sys.exit(1)


if __name__ == '__main__':
    main()
