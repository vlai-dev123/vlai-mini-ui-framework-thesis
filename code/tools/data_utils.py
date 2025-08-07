#!/usr/bin/env python3
"""
Data Utilities for Thesis Research

This script contains utility functions for common data operations:
- Data validation
- Data transformation
- Statistical helpers
- File operations
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from typing import List, Dict, Any, Optional

class DataUtils:
    """
    Utility class for data operations
    """
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> Dict[str, Any]:
        """
        Validate a dataframe for common issues
        
        Args:
            df (pd.DataFrame): Dataframe to validate
            required_columns (List[str]): List of required columns
            
        Returns:
            Dict[str, Any]: Validation results
        """
        validation_results = {
            'is_valid': True,
            'issues': [],
            'warnings': []
        }
        
        # Check if dataframe is empty
        if df.empty:
            validation_results['is_valid'] = False
            validation_results['issues'].append("Dataframe is empty")
        
        # Check for required columns
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                validation_results['is_valid'] = False
                validation_results['issues'].append(f"Missing required columns: {missing_columns}")
        
        # Check for duplicate rows
        if df.duplicated().sum() > 0:
            validation_results['warnings'].append(f"Found {df.duplicated().sum()} duplicate rows")
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        if missing_counts.sum() > 0:
            validation_results['warnings'].append(f"Found {missing_counts.sum()} missing values")
        
        # Check for infinite values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            inf_counts = np.isinf(df[numeric_cols]).sum().sum()
            if inf_counts > 0:
                validation_results['warnings'].append(f"Found {inf_counts} infinite values")
        
        return validation_results
    
    @staticmethod
    def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean column names by removing special characters and standardizing format
        
        Args:
            df (pd.DataFrame): Dataframe with columns to clean
            
        Returns:
            pd.DataFrame: Dataframe with cleaned column names
        """
        df_clean = df.copy()
        
        # Remove special characters and spaces
        df_clean.columns = df_clean.columns.str.replace(r'[^\w\s]', '', regex=True)
        df_clean.columns = df_clean.columns.str.replace(r'\s+', '_', regex=True)
        df_clean.columns = df_clean.columns.str.lower()
        
        return df_clean
    
    @staticmethod
    def detect_data_types(df: pd.DataFrame) -> Dict[str, str]:
        """
        Detect and suggest data types for columns
        
        Args:
            df (pd.DataFrame): Dataframe to analyze
            
        Returns:
            Dict[str, str]: Dictionary mapping columns to suggested data types
        """
        type_suggestions = {}
        
        for col in df.columns:
            # Check if it's a date column
            if col.lower() in ['date', 'time', 'timestamp', 'created', 'updated']:
                type_suggestions[col] = 'datetime'
                continue
            
            # Check if it's categorical
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.1 and df[col].dtype == 'object':
                type_suggestions[col] = 'category'
                continue
            
            # Check if it's numeric
            if df[col].dtype in ['int64', 'float64']:
                type_suggestions[col] = 'numeric'
                continue
            
            # Default to object
            type_suggestions[col] = 'object'
        
        return type_suggestions
    
    @staticmethod
    def create_summary_statistics(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Create comprehensive summary statistics
        
        Args:
            df (pd.DataFrame): Dataframe to analyze
            
        Returns:
            Dict[str, Any]: Summary statistics
        """
        summary = {
            'basic_info': {
                'shape': df.shape,
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'dtypes': df.dtypes.to_dict()
            },
            'missing_values': df.isnull().sum().to_dict(),
            'descriptive_stats': df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {},
            'categorical_info': {}
        }
        
        # Add categorical column information
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            summary['categorical_info'][col] = {
                'unique_count': df[col].nunique(),
                'most_common': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'most_common_count': df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
            }
        
        return summary
    
    @staticmethod
    def split_data_by_condition(df: pd.DataFrame, condition_col: str, 
                              condition_value: Any) -> tuple:
        """
        Split data based on a condition
        
        Args:
            df (pd.DataFrame): Dataframe to split
            condition_col (str): Column to use for splitting
            condition_value (Any): Value to split on
            
        Returns:
            tuple: (matching_data, non_matching_data)
        """
        matching = df[df[condition_col] == condition_value].copy()
        non_matching = df[df[condition_col] != condition_value].copy()
        
        return matching, non_matching
    
    @staticmethod
    def create_sample_data(n_samples: int = 1000, seed: int = 42) -> pd.DataFrame:
        """
        Create sample data for testing and development
        
        Args:
            n_samples (int): Number of samples to create
            seed (int): Random seed
            
        Returns:
            pd.DataFrame: Sample dataset
        """
        np.random.seed(seed)
        
        # Create sample data
        data = {
            'id': range(1, n_samples + 1),
            'age': np.random.normal(35, 10, n_samples).astype(int),
            'income': np.random.lognormal(10, 0.5, n_samples),
            'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples),
            'satisfaction': np.random.randint(1, 11, n_samples),
            'date': pd.date_range('2023-01-01', periods=n_samples, freq='D'),
            'category': np.random.choice(['A', 'B', 'C'], n_samples)
        }
        
        # Add some missing values
        for col in ['age', 'income', 'satisfaction']:
            mask = np.random.random(n_samples) < 0.05  # 5% missing values
            data[col][mask] = np.nan
        
        return pd.DataFrame(data)
    
    @staticmethod
    def export_to_multiple_formats(df: pd.DataFrame, base_filename: str, 
                                 formats: List[str] = ['csv', 'xlsx', 'json']) -> List[str]:
        """
        Export dataframe to multiple formats
        
        Args:
            df (pd.DataFrame): Dataframe to export
            base_filename (str): Base filename without extension
            formats (List[str]): List of formats to export to
            
        Returns:
            List[str]: List of created filenames
        """
        created_files = []
        
        for fmt in formats:
            filename = f"{base_filename}.{fmt}"
            
            try:
                if fmt == 'csv':
                    df.to_csv(filename, index=False)
                elif fmt == 'xlsx':
                    df.to_excel(filename, index=False)
                elif fmt == 'json':
                    df.to_json(filename, orient='records', indent=2)
                elif fmt == 'parquet':
                    df.to_parquet(filename, index=False)
                
                created_files.append(filename)
                print(f"Exported to {filename}")
                
            except Exception as e:
                print(f"Error exporting to {fmt}: {e}")
        
        return created_files
    
    @staticmethod
    def load_multiple_files(file_paths: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Load multiple files into a dictionary
        
        Args:
            file_paths (List[str]): List of file paths to load
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary mapping filenames to dataframes
        """
        dataframes = {}
        
        for file_path in file_paths:
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.json'):
                    df = pd.read_json(file_path)
                elif file_path.endswith('.parquet'):
                    df = pd.read_parquet(file_path)
                else:
                    print(f"Unsupported file format: {file_path}")
                    continue
                
                filename = os.path.basename(file_path)
                dataframes[filename] = df
                print(f"Loaded {filename}: {df.shape}")
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        return dataframes
    
    @staticmethod
    def create_data_dictionary(df: pd.DataFrame, output_file: str = None) -> Dict[str, Any]:
        """
        Create a data dictionary for the dataframe
        
        Args:
            df (pd.DataFrame): Dataframe to document
            output_file (str): Optional file to save the dictionary
            
        Returns:
            Dict[str, Any]: Data dictionary
        """
        data_dict = {
            'dataset_info': {
                'name': 'Dataset',
                'description': 'Dataset description',
                'created_date': datetime.now().isoformat(),
                'shape': df.shape
            },
            'variables': {}
        }
        
        for col in df.columns:
            var_info = {
                'type': str(df[col].dtype),
                'description': f'Description for {col}',
                'missing_count': df[col].isnull().sum(),
                'missing_percentage': (df[col].isnull().sum() / len(df)) * 100
            }
            
            # Add type-specific information
            if df[col].dtype in ['int64', 'float64']:
                var_info.update({
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'mean': df[col].mean(),
                    'std': df[col].std()
                })
            elif df[col].dtype in ['object', 'category']:
                var_info.update({
                    'unique_values': df[col].nunique(),
                    'most_common': df[col].mode().iloc[0] if not df[col].mode().empty else None
                })
            
            data_dict['variables'][col] = var_info
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(data_dict, f, indent=2)
            print(f"Data dictionary saved to {output_file}")
        
        return data_dict
    
    @staticmethod
    def compare_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, 
                          id_column: str = None) -> Dict[str, Any]:
        """
        Compare two dataframes
        
        Args:
            df1 (pd.DataFrame): First dataframe
            df2 (pd.DataFrame): Second dataframe
            id_column (str): Column to use for row comparison
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        comparison = {
            'shape_comparison': {
                'df1_shape': df1.shape,
                'df2_shape': df2.shape
            },
            'column_comparison': {
                'common_columns': list(set(df1.columns) & set(df2.columns)),
                'df1_only': list(set(df1.columns) - set(df2.columns)),
                'df2_only': list(set(df2.columns) - set(df1.columns))
            }
        }
        
        # Compare common columns
        common_cols = comparison['column_comparison']['common_columns']
        if common_cols:
            comparison['column_analysis'] = {}
            for col in common_cols:
                if df1[col].dtype == df2[col].dtype:
                    if df1[col].dtype in ['int64', 'float64']:
                        comparison['column_analysis'][col] = {
                            'df1_mean': df1[col].mean(),
                            'df2_mean': df2[col].mean(),
                            'mean_difference': df1[col].mean() - df2[col].mean()
                        }
                    else:
                        comparison['column_analysis'][col] = {
                            'df1_unique': df1[col].nunique(),
                            'df2_unique': df2[col].nunique(),
                            'common_values': len(set(df1[col]) & set(df2[col]))
                        }
        
        return comparison

def main():
    """
    Main function to demonstrate utility functions
    """
    print("=== DATA UTILITIES DEMONSTRATION ===")
    
    # Create sample data
    sample_df = DataUtils.create_sample_data(100)
    print(f"Created sample data: {sample_df.shape}")
    
    # Validate data
    validation = DataUtils.validate_dataframe(sample_df)
    print(f"Validation results: {validation}")
    
    # Create summary statistics
    summary = DataUtils.create_summary_statistics(sample_df)
    print(f"Summary statistics created for {len(summary['basic_info']['dtypes'])} columns")
    
    # Create data dictionary
    data_dict = DataUtils.create_data_dictionary(sample_df)
    print(f"Data dictionary created with {len(data_dict['variables'])} variables")
    
    print("\nUtilities demonstration complete!")

if __name__ == "__main__":
    main()
