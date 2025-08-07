#!/usr/bin/env python3
"""
Thesis Framework Web Interface Server
Provides a web interface for the thesis framework with backend integration
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import pandas as pd
import sys
import os

# Add the parent directory to the path to import our analysis modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data-analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

try:
    from main_analysis import ThesisDataAnalyzer
    from preprocess import DataPreprocessor
    from data_utils import DataUtils
except ImportError:
    print("Warning: Could not import analysis modules. Some features may not be available.")

app = Flask(__name__)

# Configure the template and static folders
app.template_folder = '.'
app.static_folder = '.'

class ThesisFrameworkServer:
    def __init__(self):
        self.frameworks = {}
        self.data_analyzer = None
        self.preprocessor = None
        
    def initialize_analysis_tools(self):
        """Initialize the data analysis tools if available"""
        try:
            # Try to load sample data for demonstration
            sample_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'sample_data.csv')
            if os.path.exists(sample_data_path):
                self.data_analyzer = ThesisDataAnalyzer(sample_data_path)
                self.preprocessor = DataPreprocessor(sample_data_path)
                return True
        except Exception as e:
            print(f"Could not initialize analysis tools: {e}")
            return False

# Initialize the server
server = ThesisFrameworkServer()

@app.route('/')
def index():
    """Serve the main thesis framework interface"""
    return send_from_directory('.', 'index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory('js', filename)

@app.route('/api/save-framework', methods=['POST'])
def save_framework():
    """Save a thesis framework to the server"""
    try:
        data = request.json
        framework_id = f"framework_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save framework data
        server.frameworks[framework_id] = {
            'data': data,
            'created_at': datetime.now().isoformat(),
            'title': data.get('tentativeTitle', 'Untitled Framework')
        }
        
        # Create framework file
        framework_content = generate_framework_content(data)
        framework_path = os.path.join('frameworks', f'{framework_id}.md')
        
        # Ensure frameworks directory exists
        os.makedirs('frameworks', exist_ok=True)
        
        with open(framework_path, 'w', encoding='utf-8') as f:
            f.write(framework_content)
        
        return jsonify({
            'success': True,
            'framework_id': framework_id,
            'message': 'Framework saved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/frameworks')
def list_frameworks():
    """List all saved frameworks"""
    frameworks = []
    for framework_id, framework_data in server.frameworks.items():
        frameworks.append({
            'id': framework_id,
            'title': framework_data['title'],
            'created_at': framework_data['created_at']
        })
    
    return jsonify(frameworks)

@app.route('/api/framework/<framework_id>')
def get_framework(framework_id):
    """Get a specific framework"""
    if framework_id in server.frameworks:
        return jsonify(server.frameworks[framework_id])
    else:
        return jsonify({'error': 'Framework not found'}), 404

@app.route('/api/analyze-sample-data')
def analyze_sample_data():
    """Analyze the sample data and return insights"""
    try:
        if not server.data_analyzer:
            server.initialize_analysis_tools()
        
        if not server.data_analyzer:
            return jsonify({
                'success': False,
                'error': 'Data analysis tools not available'
            })
        
        # Perform basic analysis
        analysis_results = {
            'summary_stats': server.data_analyzer.get_summary_statistics(),
            'correlations': server.data_analyzer.correlation_analysis(),
            'missing_values': server.data_analyzer.explore_missing_values(),
            'data_shape': server.data_analyzer.data.shape,
            'columns': list(server.data_analyzer.data.columns)
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/preprocess-data', methods=['POST'])
def preprocess_data():
    """Preprocess data based on user specifications"""
    try:
        data = request.json
        preprocessing_config = data.get('config', {})
        
        if not server.preprocessor:
            server.initialize_analysis_tools()
        
        if not server.preprocessor:
            return jsonify({
                'success': False,
                'error': 'Preprocessing tools not available'
            })
        
        # Apply preprocessing based on configuration
        results = {}
        
        # Handle missing values
        if preprocessing_config.get('handle_missing'):
            method = preprocessing_config.get('missing_method', 'auto')
            server.preprocessor.handle_missing_values(method=method)
            results['missing_values_handled'] = True
        
        # Handle outliers
        if preprocessing_config.get('handle_outliers'):
            method = preprocessing_config.get('outlier_method', 'iqr')
            server.preprocessor.handle_outliers(method=method)
            results['outliers_handled'] = True
        
        # Encode categorical variables
        if preprocessing_config.get('encode_categorical'):
            method = preprocessing_config.get('encoding_method', 'label')
            server.preprocessor.encode_categorical_variables(method=method)
            results['categorical_encoded'] = True
        
        # Scale numerical features
        if preprocessing_config.get('scale_features'):
            method = preprocessing_config.get('scaling_method', 'standard')
            server.preprocessor.scale_numerical_features(method=method)
            results['features_scaled'] = True
        
        return jsonify({
            'success': True,
            'results': results,
            'data_shape': server.preprocessor.data.shape
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_framework_content(data):
    """Generate framework content from form data"""
    content = f"""# THESIS WRITING FRAMEWORK

## Research Overview
**Field/Area**: {data.get('researchArea', 'Not specified')}
**Tentative Title**: {data.get('tentativeTitle', 'Not specified')}

## Problem Statement
{data.get('problemStatement', 'Not specified')}

## Research Objectives
{chr(10).join([f"{i+1}. {obj}" for i, obj in enumerate(data.get('objectives', [])) if obj.strip()])}

## Key Research Questions
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(data.get('keyQuestions', [])) if q.strip()])}

## Methodology Approach
{data.get('methodology', 'Not specified')}

## Timeline & Resources
**Timeframe**: {data.get('timeframe', 'Not specified')}
**Required Resources**: {data.get('resources', 'Not specified')}

## Integration with Thesis Project Framework:

### 1. Data Analysis Pipeline
- Use the Python scripts in `code/data-analysis/` for statistical analysis
- Leverage `preprocess.py` for data cleaning and preparation
- Utilize `main_analysis.py` for correlation, regression, and hypothesis testing

### 2. Visualization Tools
- Generate publication-ready plots with `code/visualization/create_plots.py`
- Create interactive visualizations for presentations
- Export figures in multiple formats (PNG, PDF, SVG)

### 3. Documentation Structure
- Update `docs/framework.md` with your research framework
- Use `docs/literature-review/literature_review_template.md` for literature review
- Document methodology in `docs/methodology/methodology_template.md`

### 4. Project Management
- Track progress using the project structure
- Use `data/` directory for your datasets
- Maintain version control with the provided `.gitignore`

## Recommended Workflow:
1. **Data Collection**: Store raw data in `data/raw/`
2. **Preprocessing**: Use `code/data-analysis/preprocess.py` for data cleaning
3. **Analysis**: Run statistical tests with `code/data-analysis/main_analysis.py`
4. **Visualization**: Create plots with `code/visualization/create_plots.py`
5. **Documentation**: Update framework and methodology documents
6. **Results**: Store outputs in `results/` directory

## Next Steps:
1. Install Python dependencies: `pip install -r requirements.txt`
2. Test the framework with sample data
3. Customize scripts for your specific research needs
4. Begin data collection and analysis
5. Update documentation as your research evolves

---
*Generated by Thesis Framework Assistant*
*Integrated with Python Data Analysis Framework*
*Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return content

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'analysis_tools_available': server.data_analyzer is not None
    })

if __name__ == '__main__':
    print("Starting Thesis Framework Web Interface...")
    print("Access the interface at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    # Initialize analysis tools
    server.initialize_analysis_tools()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
