#!/usr/bin/env python3
"""
Main Data Analysis Script for Thesis Research

This script serves as the primary entry point for data analysis.
It includes common statistical analyses and can be customized for specific research needs.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ThesisDataAnalyzer:
    """
    Main class for conducting thesis data analysis
    """
    
    def __init__(self, data_path=None):
        """
        Initialize the analyzer with optional data path
        
        Args:
            data_path (str): Path to the data file
        """
        self.data = None
        self.data_path = data_path
        self.results = {}
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, file_path):
        """
        Load data from various file formats
        
        Args:
            file_path (str): Path to the data file
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
            
            print(f"Data loaded successfully: {self.data.shape}")
            print(f"Columns: {list(self.data.columns)}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def explore_data(self):
        """
        Perform exploratory data analysis
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        print("\n=== EXPLORATORY DATA ANALYSIS ===")
        
        # Basic information
        print("\n1. Data Overview:")
        print(f"Shape: {self.data.shape}")
        print(f"Memory usage: {self.data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Data types
        print("\n2. Data Types:")
        print(self.data.dtypes)
        
        # Missing values
        print("\n3. Missing Values:")
        missing_data = self.data.isnull().sum()
        if missing_data.sum() > 0:
            print(missing_data[missing_data > 0])
        else:
            print("No missing values found.")
        
        # Descriptive statistics
        print("\n4. Descriptive Statistics:")
        print(self.data.describe())
        
        # Store results
        self.results['exploratory'] = {
            'shape': self.data.shape,
            'missing_values': missing_data.to_dict(),
            'descriptive_stats': self.data.describe().to_dict()
        }
    
    def correlation_analysis(self, variables=None):
        """
        Perform correlation analysis
        
        Args:
            variables (list): List of variables to analyze. If None, uses all numeric variables.
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        # Select numeric variables
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if variables:
            numeric_data = numeric_data[variables]
        
        print("\n=== CORRELATION ANALYSIS ===")
        
        # Correlation matrix
        corr_matrix = numeric_data.corr()
        
        # Display correlation matrix
        print("\nCorrelation Matrix:")
        print(corr_matrix.round(3))
        
        # Create correlation heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Store results
        self.results['correlation'] = corr_matrix.to_dict()
    
    def statistical_tests(self, group_var, test_var, test_type='t_test'):
        """
        Perform statistical tests
        
        Args:
            group_var (str): Variable used for grouping
            test_var (str): Variable to test
            test_type (str): Type of test ('t_test', 'anova', 'chi_square')
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        print(f"\n=== STATISTICAL TEST: {test_type.upper()} ===")
        
        if test_type == 't_test':
            # Independent t-test
            groups = self.data[group_var].unique()
            if len(groups) == 2:
                group1_data = self.data[self.data[group_var] == groups[0]][test_var]
                group2_data = self.data[self.data[group_var] == groups[1]][test_var]
                
                t_stat, p_value = stats.ttest_ind(group1_data, group2_data)
                
                print(f"T-statistic: {t_stat:.4f}")
                print(f"P-value: {p_value:.4f}")
                print(f"Significant difference: {'Yes' if p_value < 0.05 else 'No'}")
                
                # Store results
                self.results['t_test'] = {
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                }
        
        elif test_type == 'anova':
            # One-way ANOVA
            groups = self.data[group_var].unique()
            group_data = [self.data[self.data[group_var] == group][test_var] 
                         for group in groups]
            
            f_stat, p_value = stats.f_oneway(*group_data)
            
            print(f"F-statistic: {f_stat:.4f}")
            print(f"P-value: {p_value:.4f}")
            print(f"Significant difference: {'Yes' if p_value < 0.05 else 'No'}")
            
            # Store results
            self.results['anova'] = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
    
    def regression_analysis(self, dependent_var, independent_vars):
        """
        Perform regression analysis
        
        Args:
            dependent_var (str): Dependent variable
            independent_vars (list): List of independent variables
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        print("\n=== REGRESSION ANALYSIS ===")
        
        # Prepare data
        X = self.data[independent_vars]
        y = self.data[dependent_var]
        
        # Import statsmodels for regression
        import statsmodels.api as sm
        
        # Add constant for intercept
        X = sm.add_constant(X)
        
        # Fit model
        model = sm.OLS(y, X).fit()
        
        # Print results
        print(model.summary())
        
        # Store results
        self.results['regression'] = {
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'f_statistic': model.fvalue,
            'f_pvalue': model.f_pvalue,
            'coefficients': model.params.to_dict(),
            'p_values': model.pvalues.to_dict()
        }
    
    def create_visualizations(self):
        """
        Create standard visualizations for the data
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        print("\n=== CREATING VISUALIZATIONS ===")
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Distribution plots for numeric variables
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns[:4]
        for i, col in enumerate(numeric_cols):
            if i < 4:
                row, col_idx = i // 2, i % 2
                axes[row, col_idx].hist(self.data[col], bins=20, alpha=0.7, edgecolor='black')
                axes[row, col_idx].set_title(f'Distribution of {col}')
                axes[row, col_idx].set_xlabel(col)
                axes[row, col_idx].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('data_distributions.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Box plots for categorical variables
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            fig, axes = plt.subplots(1, min(3, len(categorical_cols)), figsize=(15, 5))
            if len(categorical_cols) == 1:
                axes = [axes]
            
            for i, cat_col in enumerate(categorical_cols[:3]):
                if i < len(axes):
                    for num_col in numeric_cols[:1]:
                        self.data.boxplot(column=num_col, by=cat_col, ax=axes[i])
                        axes[i].set_title(f'{num_col} by {cat_col}')
                        axes[i].set_xlabel(cat_col)
            
            plt.tight_layout()
            plt.savefig('box_plots.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def save_results(self, filename='analysis_results.json'):
        """
        Save analysis results to JSON file
        
        Args:
            filename (str): Output filename
        """
        import json
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Convert results to JSON-serializable format
        json_results = {}
        for key, value in self.results.items():
            if isinstance(value, dict):
                json_results[key] = {k: convert_numpy(v) for k, v in value.items()}
            else:
                json_results[key] = convert_numpy(value)
        
        with open(filename, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"Results saved to {filename}")

def main():
    """
    Main function to run the analysis
    """
    print("=== THESIS DATA ANALYSIS SCRIPT ===")
    
    # Initialize analyzer
    analyzer = ThesisDataAnalyzer()
    
    # Example usage (uncomment and modify as needed)
    # analyzer.load_data('data/your_data.csv')
    # analyzer.explore_data()
    # analyzer.correlation_analysis()
    # analyzer.create_visualizations()
    # analyzer.save_results()
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
