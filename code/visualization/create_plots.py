#!/usr/bin/env python3
"""
Data Visualization Script for Thesis Research

This script creates various types of plots and visualizations commonly used in research:
- Distribution plots
- Correlation heatmaps
- Box plots
- Scatter plots
- Time series plots
- Custom research-specific visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ThesisVisualizer:
    """
    Class for creating research visualizations
    """
    
    def __init__(self, data=None):
        """
        Initialize the visualizer
        
        Args:
            data (pd.DataFrame): Input data
        """
        self.data = data
        self.figures = {}
        
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
            
            print(f"Data loaded for visualization: {self.data.shape}")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def create_distribution_plots(self, columns=None, save_path='distributions.png'):
        """
        Create distribution plots for numerical variables
        
        Args:
            columns (list): Columns to plot
            save_path (str): Path to save the plot
        """
        if self.data is None:
            print("No data loaded")
            return
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns
        
        # Calculate number of subplots
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        elif n_cols == 1:
            axes = axes.reshape(-1, 1)
        
        for i, col in enumerate(columns):
            row = i // n_cols
            col_idx = i % n_cols
            
            # Histogram with KDE
            axes[row, col_idx].hist(self.data[col], bins=30, alpha=0.7, density=True, 
                                   edgecolor='black', color='skyblue')
            
            # Add KDE curve
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(self.data[col].dropna())
            x_range = np.linspace(self.data[col].min(), self.data[col].max(), 100)
            axes[row, col_idx].plot(x_range, kde(x_range), 'r-', linewidth=2)
            
            axes[row, col_idx].set_title(f'Distribution of {col}')
            axes[row, col_idx].set_xlabel(col)
            axes[row, col_idx].set_ylabel('Density')
            axes[row, col_idx].grid(True, alpha=0.3)
        
        # Hide empty subplots
        for i in range(len(columns), n_rows * n_cols):
            row = i // n_cols
            col_idx = i % n_cols
            axes[row, col_idx].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        self.figures['distributions'] = save_path
    
    def create_correlation_heatmap(self, columns=None, save_path='correlation_heatmap.png'):
        """
        Create correlation heatmap
        
        Args:
            columns (list): Columns to include in correlation
            save_path (str): Path to save the plot
        """
        if self.data is None:
            print("No data loaded")
            return
        
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns
        
        corr_matrix = self.data[columns].corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        
        plt.title('Correlation Matrix', fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        self.figures['correlation_heatmap'] = save_path
    
    def create_box_plots(self, x_col, y_col, save_path='box_plots.png'):
        """
        Create box plots for categorical vs numerical variables
        
        Args:
            x_col (str): Categorical column
            y_col (str): Numerical column
            save_path (str): Path to save the plot
        """
        if self.data is None:
            print("No data loaded")
            return
        
        plt.figure(figsize=(12, 6))
        
        # Create box plot
        sns.boxplot(data=self.data, x=x_col, y=y_col)
        plt.title(f'{y_col} by {x_col}', fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        self.figures['box_plots'] = save_path
    
    def create_scatter_plots(self, x_col, y_col, hue_col=None, save_path='scatter_plots.png'):
        """
        Create scatter plots
        
        Args:
            x_col (str): X-axis column
            y_col (str): Y-axis column
            hue_col (str): Color grouping column
            save_path (str): Path to save the plot
        """
        if self.data is None:
            print("No data loaded")
            return
        
        plt.figure(figsize=(10, 8))
        
        if hue_col:
            sns.scatterplot(data=self.data, x=x_col, y=y_col, hue=hue_col, alpha=0.7)
        else:
            sns.scatterplot(data=self.data, x=x_col, y=y_col, alpha=0.7)
        
        plt.title(f'{y_col} vs {x_col}', fontsize=14)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        self.figures['scatter_plots'] = save_path
    
    def create_time_series_plot(self, time_col, value_col, save_path='time_series.png'):
        """
        Create time series plot
        
        Args:
            time_col (str): Time column
            value_col (str): Value column
            save_path (str): Path to save the plot
        """
        if self.data is None:
            print("No data loaded")
            return
        
        # Convert time column to datetime if needed
        if self.data[time_col].dtype == 'object':
            self.data[time_col] = pd.to_datetime(self.data[time_col])
        
        plt.figure(figsize=(15, 6))
        plt.plot(self.data[time_col], self.data[value_col], linewidth=2)
        plt.title(f'{value_col} Over Time', fontsize=14)
        plt.xlabel('Time')
        plt.ylabel(value_col)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        self.figures['time_series'] = save_path
    
    def create_interactive_plot(self, x_col, y_col, title="Interactive Plot"):
        """
        Create interactive plot using Plotly
        
        Args:
            x_col (str): X-axis column
            y_col (str): Y-axis column
            title (str): Plot title
        """
        if self.data is None:
            print("No data loaded")
            return
        
        fig = px.scatter(self.data, x=x_col, y=y_col, title=title)
        fig.show()
    
    def create_research_summary_plot(self, save_path='research_summary.png'):
        """
        Create a comprehensive summary plot for research findings
        
        Args:
            save_path (str): Path to save the plot
        """
        if self.data is None:
            print("No data loaded")
            return
        
        # Create a 2x2 subplot layout
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Data overview
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Summary statistics
            summary_stats = self.data[numeric_cols].describe()
            axes[0, 0].text(0.1, 0.9, 'Summary Statistics', fontsize=14, fontweight='bold')
            axes[0, 0].text(0.1, 0.8, f'Total observations: {len(self.data)}', fontsize=10)
            axes[0, 0].text(0.1, 0.7, f'Numeric variables: {len(numeric_cols)}', fontsize=10)
            axes[0, 0].text(0.1, 0.6, f'Missing values: {self.data.isnull().sum().sum()}', fontsize=10)
            axes[0, 0].set_xlim(0, 1)
            axes[0, 0].set_ylim(0, 1)
            axes[0, 0].axis('off')
        
        # 2. Distribution of first numeric variable
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            axes[0, 1].hist(self.data[col], bins=30, alpha=0.7, edgecolor='black')
            axes[0, 1].set_title(f'Distribution of {col}')
            axes[0, 1].set_xlabel(col)
            axes[0, 1].set_ylabel('Frequency')
        
        # 3. Correlation heatmap (if multiple numeric variables)
        if len(numeric_cols) > 1:
            corr_matrix = self.data[numeric_cols].corr()
            im = axes[1, 0].imshow(corr_matrix, cmap='coolwarm', aspect='auto')
            axes[1, 0].set_title('Correlation Matrix')
            axes[1, 0].set_xticks(range(len(numeric_cols)))
            axes[1, 0].set_yticks(range(len(numeric_cols)))
            axes[1, 0].set_xticklabels(numeric_cols, rotation=45)
            axes[1, 0].set_yticklabels(numeric_cols)
            plt.colorbar(im, ax=axes[1, 0])
        
        # 4. Missing values visualization
        missing_data = self.data.isnull().sum()
        if missing_data.sum() > 0:
            missing_data = missing_data[missing_data > 0]
            axes[1, 1].bar(range(len(missing_data)), missing_data.values)
            axes[1, 1].set_title('Missing Values by Column')
            axes[1, 1].set_xticks(range(len(missing_data)))
            axes[1, 1].set_xticklabels(missing_data.index, rotation=45)
            axes[1, 1].set_ylabel('Missing Count')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        self.figures['research_summary'] = save_path
    
    def create_custom_plot(self, plot_type, **kwargs):
        """
        Create custom plots based on research needs
        
        Args:
            plot_type (str): Type of custom plot
            **kwargs: Additional arguments for the plot
        """
        if self.data is None:
            print("No data loaded")
            return
        
        if plot_type == 'violin':
            # Violin plot
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=self.data, **kwargs)
            plt.title('Violin Plot')
            plt.show()
        
        elif plot_type == 'pair':
            # Pair plot
            numeric_data = self.data.select_dtypes(include=[np.number])
            if len(numeric_data.columns) > 1:
                sns.pairplot(numeric_data)
                plt.show()
        
        elif plot_type == 'joint':
            # Joint plot
            if len(self.data.select_dtypes(include=[np.number]).columns) >= 2:
                cols = self.data.select_dtypes(include=[np.number]).columns[:2]
                sns.jointplot(data=self.data, x=cols[0], y=cols[1])
                plt.show()
    
    def save_all_figures(self, output_dir='figures/'):
        """
        Save all created figures to a directory
        
        Args:
            output_dir (str): Output directory
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Saving figures to {output_dir}")
        for fig_name, fig_path in self.figures.items():
            print(f"  - {fig_name}: {fig_path}")
    
    def generate_report(self, output_file='visualization_report.html'):
        """
        Generate an HTML report with all visualizations
        
        Args:
            output_file (str): Output HTML file
        """
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Thesis Visualization Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                .figure { margin: 20px 0; }
                img { max-width: 100%; height: auto; }
            </style>
        </head>
        <body>
            <h1>Thesis Visualization Report</h1>
        """
        
        for fig_name, fig_path in self.figures.items():
            html_content += f"""
            <div class="figure">
                <h2>{fig_name.replace('_', ' ').title()}</h2>
                <img src="{fig_path}" alt="{fig_name}">
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"Report generated: {output_file}")

def main():
    """
    Main function to run visualization
    """
    print("=== THESIS VISUALIZATION SCRIPT ===")
    
    # Initialize visualizer
    visualizer = ThesisVisualizer()
    
    # Example usage (uncomment and modify as needed)
    # visualizer.load_data('data/processed_data.csv')
    # visualizer.create_distribution_plots()
    # visualizer.create_correlation_heatmap()
    # visualizer.create_research_summary_plot()
    # visualizer.save_all_figures()
    # visualizer.generate_report()
    
    print("\nVisualization complete!")

if __name__ == "__main__":
    main()
