# Thesis Framework Web Interface

A modern web interface for the thesis framework that provides an interactive way to create and manage your research framework, with integration to the Python data analysis tools.

## Features

### 🎯 Interactive Framework Builder
- Step-by-step framework creation process
- Real-time form validation and guidance
- Progress tracking with visual indicators
- Export framework as Markdown file

### 📊 Data Analysis Integration
- Connect to your existing Python analysis scripts
- Preview sample data analysis results
- Preprocessing pipeline integration
- Statistical analysis visualization

### 🎨 Modern UI/UX
- Clean, responsive design with Tailwind CSS
- Lucide icons for intuitive navigation
- Smooth animations and transitions
- Mobile-friendly interface

## Quick Start

### Option 1: Simple HTML Interface
1. Open `index.html` in your web browser
2. Start building your thesis framework
3. Download your completed framework

### Option 2: Full Web Server (Recommended)
1. Install Flask if not already installed:
   ```bash
   pip install flask
   ```

2. Start the web server:
   ```bash
   cd code/web-interface
   python server.py
   ```

3. Open your browser and go to: `http://localhost:5000`

## Framework Steps

### Step 1: Define Research Focus
- **Research Area/Field**: Specify your academic discipline
- **Tentative Title**: Your working thesis title
- Get guidance on crafting effective research questions

### Step 2: Problem & Objectives
- **Problem Statement**: Define the research gap
- **Research Objectives**: List specific goals
- **Key Research Questions**: Formulate guiding questions
- Add multiple objectives and questions as needed

### Step 3: Methodology & Timeline
- **Research Methodology**: Choose your approach
- **Expected Timeframe**: Set realistic deadlines
- **Required Resources**: Identify needed tools and access

### Step 4: Framework Summary
- Review your complete framework
- Download as Markdown file
- Get integration guidance for your thesis project

## API Endpoints

The web server provides several API endpoints for advanced functionality:

### Framework Management
- `POST /api/save-framework` - Save framework to server
- `GET /api/frameworks` - List all saved frameworks
- `GET /api/framework/<id>` - Get specific framework

### Data Analysis
- `GET /api/analyze-sample-data` - Analyze sample dataset
- `POST /api/preprocess-data` - Preprocess data with custom config
- `GET /api/health` - Server health check

## Integration with Thesis Project

The web interface is designed to work seamlessly with your existing thesis framework:

### Data Analysis Pipeline
- Connects to `code/data-analysis/main_analysis.py`
- Integrates with `code/data-analysis/preprocess.py`
- Uses `code/tools/data_utils.py` for utilities

### Documentation Structure
- Generates framework compatible with `docs/framework.md`
- Aligns with literature review templates
- Supports methodology documentation

### Project Management
- Saves frameworks in organized structure
- Integrates with version control
- Maintains consistency with project standards

## Customization

### Styling
- Modify `index.html` for layout changes
- Update CSS classes for styling
- Customize Tailwind classes for design

### Functionality
- Edit `js/thesis-framework.js` for behavior changes
- Modify `server.py` for backend customization
- Add new API endpoints as needed

### Data Integration
- Connect to your own datasets
- Customize analysis parameters
- Add domain-specific preprocessing

## File Structure

```
code/web-interface/
├── index.html              # Main interface
├── js/
│   └── thesis-framework.js # Frontend logic
├── server.py               # Flask backend
├── README.md              # This file
└── frameworks/            # Generated frameworks (created on use)
```

## Browser Compatibility

- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Mobile browsers**: Responsive design

## Troubleshooting

### Common Issues

1. **Icons not showing**
   - Check internet connection (Lucide icons loaded from CDN)
   - Refresh the page

2. **Server won't start**
   - Ensure Flask is installed: `pip install flask`
   - Check port 5000 is available
   - Verify Python path includes required modules

3. **Analysis tools not working**
   - Ensure sample data exists in `data/sample_data.csv`
   - Check all Python dependencies are installed
   - Verify import paths in `server.py`

### Getting Help

1. Check the browser console for JavaScript errors
2. Review server logs for Python errors
3. Verify all dependencies are installed
4. Test with the sample data first

## Advanced Usage

### Custom Data Analysis
1. Replace sample data with your own dataset
2. Modify analysis parameters in `server.py`
3. Add custom preprocessing steps
4. Integrate with your specific research needs

### Framework Templates
1. Create template frameworks for different research types
2. Customize the form fields for your discipline
3. Add domain-specific guidance and tips

### Multi-user Support
1. Add user authentication to `server.py`
2. Implement user-specific framework storage
3. Add collaboration features

## Contributing

To contribute to the web interface:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This web interface is part of the thesis framework project and follows the same licensing terms.
