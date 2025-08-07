#!/usr/bin/env python3
"""
Data Preprocessing Script for Thesis Research

This script handles common data preprocessing tasks including:
- Data cleaning
- Missing value handling
- Feature scaling
- Data transformation
- Outlier detection and treatment
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    """
    Class for handling data preprocessing tasks
    """
    
    def __init__(self, data=None):
        """
        Initialize the preprocessor
        
        Args:
            data (pd.DataFrame): Input data
        """
        self.data = data
        self.original_data = None
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        
    def load_data(self, file_path):
        """
        Load data from file
        
        Args:
            file_path (str): Path to data file
        """
        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                self.data = pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                self.data = pd.read_json(file_path)
            else:
                raise ValueError("Unsupported file format")
            
            self.original_data = self.data.copy()
            print(f"Data loaded: {self.data.shape}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def explore_missing_values(self):
        """
        Analyze missing values in the dataset
        """
        if self.data is None:
            print("No data loaded")
            return
        
        print("\n=== MISSING VALUES ANALYSIS ===")
        
        # Calculate missing values
        missing_data = self.data.isnull().sum()
        missing_percent = (missing_data / len(self.data)) * 100
        
        # Create missing values summary
        missing_summary = pd.DataFrame({
            'Missing_Count': missing_data,
            'Missing_Percent': missing_percent
        }).sort_values('Missing_Percent', ascending=False)
        
        print("Missing values summary:")
        print(missing_summary[missing_summary['Missing_Count'] > 0])
        
        # Visualize missing values
        plt.figure(figsize=(12, 6))
        
        # Heatmap of missing values
        plt.subplot(1, 2, 1)
        sns.heatmap(self.data.isnull(), yticklabels=False, cbar=True, cmap='viridis')
        plt.title('Missing Values Heatmap')
        
        # Bar plot of missing percentages
        plt.subplot(1, 2, 2)
        missing_percent.plot(kind='bar')
        plt.title('Missing Values Percentage')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('missing_values_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return missing_summary
    
    def handle_missing_values(self, strategy='auto', columns=None):
        """
        Handle missing values using various strategies
        
        Args:
            strategy (str): 'auto', 'mean', 'median', 'mode', 'drop', 'knn'
            columns (list): Specific columns to process
        """
        if self.data is None:
            print("No data loaded")
            return
        
        print(f"\n=== HANDLING MISSING VALUES (Strategy: {strategy}) ===")
        
        if columns is None:
            columns = self.data.columns
        
        for col in columns:
            if self.data[col].isnull().sum() > 0:
                print(f"Processing column: {col}")
                
                if strategy == 'auto':
                    # Choose strategy based on data type
                    if self.data[col].dtype in ['object', 'category']:
                        # For categorical data, use mode
                        mode_value = self.data[col].mode()[0]
                        self.data[col].fillna(mode_value, inplace=True)
                        print(f"  - Filled with mode: {mode_value}")
                    else:
                        # For numeric data, use median
                        median_value = self.data[col].median()
                        self.data[col].fillna(median_value, inplace=True)
                        print(f"  - Filled with median: {median_value}")
                
                elif strategy == 'mean':
                    mean_value = self.data[col].mean()
                    self.data[col].fillna(mean_value, inplace=True)
                    print(f"  - Filled with mean: {mean_value}")
                
                elif strategy == 'median':
                    median_value = self.data[col].median()
                    self.data[col].fillna(median_value, inplace=True)
                    print(f"  - Filled with median: {median_value}")
                
                elif strategy == 'mode':
                    mode_value = self.data[col].mode()[0]
                    self.data[col].fillna(mode_value, inplace=True)
                    print(f"  - Filled with mode: {mode_value}")
                
                elif strategy == 'drop':
                    self.data.dropna(subset=[col], inplace=True)
                    print(f"  - Dropped rows with missing values")
                
                elif strategy == 'knn':
                    # Use KNN imputation for numeric columns
                    if self.data[col].dtype in ['int64', 'float64']:
                        imputer = KNNImputer(n_neighbors=5)
                        self.data[col] = imputer.fit_transform(self.data[[col]])
                        print(f"  - Used KNN imputation")
        
        print(f"Final shape after missing value handling: {self.data.shape}")
    
    def detect_outliers(self, method='iqr', columns=None):
        """
        Detect outliers using various methods
        
        Args:
            method (str): 'iqr', 'zscore', 'isolation_forest'
            columns (list): Columns to check for outliers
        """
        if self.data is None:
            print("No data loaded")
            return
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns
        
        print(f"\n=== OUTLIER DETECTION (Method: {method}) ===")
        
        outlier_info = {}
        
        for col in columns:
            if col in self.data.columns:
                print(f"\nAnalyzing column: {col}")
                
                if method == 'iqr':
                    Q1 = self.data[col].quantile(0.25)
                    Q3 = self.data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers = self.data[(self.data[col] < lower_bound) | 
                                       (self.data[col] > upper_bound)]
                    
                    outlier_count = len(outliers)
                    outlier_percent = (outlier_count / len(self.data)) * 100
                    
                    print(f"  - Outliers: {outlier_count} ({outlier_percent:.2f}%)")
                    print(f"  - Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
                    
                    outlier_info[col] = {
                        'method': 'iqr',
                        'outlier_count': outlier_count,
                        'outlier_percent': outlier_percent,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound
                    }
                
                elif method == 'zscore':
                    from scipy import stats
                    z_scores = np.abs(stats.zscore(self.data[col]))
                    outliers = self.data[z_scores > 3]
                    
                    outlier_count = len(outliers)
                    outlier_percent = (outlier_count / len(self.data)) * 100
                    
                    print(f"  - Outliers: {outlier_count} ({outlier_percent:.2f}%)")
                    
                    outlier_info[col] = {
                        'method': 'zscore',
                        'outlier_count': outlier_count,
                        'outlier_percent': outlier_percent
                    }
        
        return outlier_info
    
    def handle_outliers(self, method='cap', columns=None):
        """
        Handle outliers using various methods
        
        Args:
            method (str): 'cap', 'remove', 'transform'
            columns (list): Columns to process
        """
        if self.data is None:
            print("No data loaded")
            return
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns
        
        print(f"\n=== HANDLING OUTLIERS (Method: {method}) ===")
        
        for col in columns:
            if col in self.data.columns:
                print(f"Processing column: {col}")
                
                if method == 'cap':
                    # Cap outliers at 1st and 99th percentiles
                    lower_bound = self.data[col].quantile(0.01)
                    upper_bound = self.data[col].quantile(0.99)
                    
                    self.data[col] = self.data[col].clip(lower=lower_bound, upper=upper_bound)
                    print(f"  - Capped at [{lower_bound:.2f}, {upper_bound:.2f}]")
                
                elif method == 'remove':
                    # Remove outliers using IQR method
                    Q1 = self.data[col].quantile(0.25)
                    Q3 = self.data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    before_count = len(self.data)
                    self.data = self.data[(self.data[col] >= lower_bound) & 
                                        (self.data[col] <= upper_bound)]
                    after_count = len(self.data)
                    
                    print(f"  - Removed {before_count - after_count} outliers")
                
                elif method == 'transform':
                    # Log transformation for positive skewed data
                    if self.data[col].min() > 0:
                        self.data[col] = np.log1p(self.data[col])
                        print(f"  - Applied log transformation")
        
        print(f"Final shape after outlier handling: {self.data.shape}")
    
    def encode_categorical_variables(self, method='label', columns=None):
        """
        Encode categorical variables
        
        Args:
            method (str): 'label', 'onehot', 'target'
            columns (list): Categorical columns to encode
        """
        if self.data is None:
            print("No data loaded")
            return
        
        if columns is None:
            columns = self.data.select_dtypes(include=['object', 'category']).columns
        
        print(f"\n=== ENCODING CATEGORICAL VARIABLES (Method: {method}) ===")
        
        for col in columns:
            if col in self.data.columns:
                print(f"Processing column: {col}")
                
                if method == 'label':
                    # Label encoding
                    le = LabelEncoder()
                    self.data[col] = le.fit_transform(self.data[col])
                    self.encoders[col] = le
                    print(f"  - Applied label encoding")
                
                elif method == 'onehot':
                    # One-hot encoding
                    dummies = pd.get_dummies(self.data[col], prefix=col)
                    self.data = pd.concat([self.data, dummies], axis=1)
                    self.data.drop(col, axis=1, inplace=True)
                    print(f"  - Applied one-hot encoding")
    
    def scale_features(self, method='standard', columns=None):
        """
        Scale numerical features
        
        Args:
            method (str): 'standard', 'minmax', 'robust'
            columns (list): Numerical columns to scale
        """
        if self.data is None:
            print("No data loaded")
            return
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns
        
        print(f"\n=== SCALING FEATURES (Method: {method}) ===")
        
        for col in columns:
            if col in self.data.columns:
                print(f"Processing column: {col}")
                
                if method == 'standard':
                    # Standard scaling
                    scaler = StandardScaler()
                    self.data[col] = scaler.fit_transform(self.data[[col]])
                    self.scalers[col] = scaler
                    print(f"  - Applied standard scaling")
                
                elif method == 'minmax':
                    # Min-max scaling
                    scaler = MinMaxScaler()
                    self.data[col] = scaler.fit_transform(self.data[[col]])
                    self.scalers[col] = scaler
                    print(f"  - Applied min-max scaling")
    
    def create_features(self):
        """
        Create new features from existing ones
        """
        if self.data is None:
            print("No data loaded")
            return
        
        print("\n=== CREATING NEW FEATURES ===")
        
        # Example feature creation (modify based on your data)
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            # Create interaction features
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    self.data[f'{col1}_x_{col2}'] = self.data[col1] * self.data[col2]
                    print(f"  - Created interaction: {col1}_x_{col2}")
        
        # Create polynomial features for important variables
        # (modify based on your specific needs)
        
        print(f"Final shape after feature creation: {self.data.shape}")
    
    def save_processed_data(self, filename='processed_data.csv'):
        """
        Save processed data to file
        
        Args:
            filename (str): Output filename
        """
        if self.data is not None:
            self.data.to_csv(filename, index=False)
            print(f"Processed data saved to {filename}")
        else:
            print("No data to save")
    
    def get_preprocessing_summary(self):
        """
        Get a summary of preprocessing steps
        """
        summary = {
            'original_shape': self.original_data.shape if self.original_data is not None else None,
            'current_shape': self.data.shape if self.data is not None else None,
            'scalers_applied': list(self.scalers.keys()),
            'encoders_applied': list(self.encoders.keys()),
            'imputers_applied': list(self.imputers.keys())
        }
        
        print("\n=== PREPROCESSING SUMMARY ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        return summary

def main():
    """
    Main function to run preprocessing
    """
    print("=== DATA PREPROCESSING SCRIPT ===")
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Example usage (uncomment and modify as needed)
    # preprocessor.load_data('data/raw_data.csv')
    # preprocessor.explore_missing_values()
    # preprocessor.handle_missing_values(strategy='auto')
    # preprocessor.detect_outliers()
    # preprocessor.handle_outliers(method='cap')
    # preprocessor.encode_categorical_variables(method='label')
    # preprocessor.scale_features(method='standard')
    # preprocessor.create_features()
    # preprocessor.save_processed_data()
    # preprocessor.get_preprocessing_summary()
    
    print("\nPreprocessing complete!")

if __name__ == "__main__":
    main()
