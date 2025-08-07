class ThesisFrameworkTool {
    constructor() {
        this.currentStep = 0;
        this.formData = {
            researchArea: '',
            tentativeTitle: '',
            problemStatement: '',
            objectives: [''],
            methodology: '',
            timeframe: '',
            resources: '',
            keyQuestions: ['']
        };
        
        this.steps = [
            { icon: 'target', title: "Define Research Focus", key: "focus" },
            { icon: 'lightbulb', title: "Problem & Objectives", key: "problem" },
            { icon: 'file-text', title: "Methodology & Timeline", key: "method" },
            { icon: 'check-circle', title: "Framework Summary", key: "summary" }
        ];
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.renderStep();
        this.updateProgress();
    }
    
    bindEvents() {
        document.getElementById('prevBtn').addEventListener('click', () => {
            this.setCurrentStep(Math.max(0, this.currentStep - 1));
        });
        
        document.getElementById('nextBtn').addEventListener('click', () => {
            if (this.currentStep < this.steps.length - 1) {
                this.setCurrentStep(Math.min(this.steps.length - 1, this.currentStep + 1));
            }
        });
    }
    
    setCurrentStep(step) {
        this.currentStep = step;
        this.renderStep();
        this.updateProgress();
        this.updateNavigation();
    }
    
    updateFormData(key, value) {
        this.formData[key] = value;
    }
    
    addArrayItem(key) {
        this.formData[key] = [...this.formData[key], ''];
        this.renderStep();
    }
    
    updateArrayItem(key, index, value) {
        this.formData[key] = this.formData[key].map((item, i) => i === index ? value : item);
    }
    
    updateProgress() {
        const stepElements = document.querySelectorAll('.step-inactive, .step-active, .step-completed');
        stepElements.forEach((element, index) => {
            element.classList.remove('step-active', 'step-completed', 'step-inactive');
            if (index === this.currentStep) {
                element.classList.add('step-active');
            } else if (index < this.currentStep) {
                element.classList.add('step-completed');
            } else {
                element.classList.add('step-inactive');
            }
        });
        
        // Update step titles
        const stepTitles = document.querySelectorAll('.text-blue-600, .text-green-600, .text-gray-400');
        stepTitles.forEach((title, index) => {
            title.classList.remove('text-blue-600', 'text-green-600', 'text-gray-400');
            if (index === this.currentStep) {
                title.classList.add('text-blue-600');
            } else if (index < this.currentStep) {
                title.classList.add('text-green-600');
            } else {
                title.classList.add('text-gray-400');
            }
        });
        
        // Update progress lines
        const progressLines = document.querySelectorAll('.w-8.h-px.mx-4');
        progressLines.forEach((line, index) => {
            if (index < this.currentStep) {
                line.classList.remove('bg-gray-300');
                line.classList.add('bg-green-500');
            } else {
                line.classList.remove('bg-green-500');
                line.classList.add('bg-gray-300');
            }
        });
    }
    
    updateNavigation() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.disabled = this.currentStep === 0;
        
        if (this.currentStep < this.steps.length - 1) {
            nextBtn.textContent = 'Next Step';
            nextBtn.onclick = () => this.setCurrentStep(this.currentStep + 1);
        } else {
            nextBtn.textContent = 'Generate Framework';
            nextBtn.onclick = () => this.generateFramework();
        }
    }
    
    renderStep() {
        const content = document.getElementById('content');
        content.innerHTML = '';
        content.classList.add('fade-in');
        
        switch(this.currentStep) {
            case 0:
                this.renderStep0();
                break;
            case 1:
                this.renderStep1();
                break;
            case 2:
                this.renderStep2();
                break;
            case 3:
                this.renderStep3();
                break;
        }
        
        // Re-initialize icons
        lucide.createIcons();
    }
    
    renderStep0() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="space-y-6">
                <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <div class="flex items-center gap-2 mb-2">
                        <i data-lucide="target" class="w-5 h-5 text-blue-600"></i>
                        <h3 class="font-semibold text-blue-900">Define Your Research Focus</h3>
                    </div>
                    <p class="text-blue-700 text-sm">Let's start by clarifying your research domain and initial thesis concept.</p>
                </div>
                
                <div>
                    <label class="block text-sm font-medium mb-2">Research Area/Field</label>
                    <input
                        type="text"
                        placeholder="e.g., Machine Learning, Environmental Science, Educational Psychology..."
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value="${this.formData.researchArea}"
                        onchange="thesisFramework.updateFormData('researchArea', this.value)"
                    />
                </div>
                
                <div>
                    <label class="block text-sm font-medium mb-2">Tentative Thesis Title</label>
                    <input
                        type="text"
                        placeholder="Don't worry, this can change! Just your current best idea..."
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value="${this.formData.tentativeTitle}"
                        onchange="thesisFramework.updateFormData('tentativeTitle', this.value)"
                    />
                    <p class="text-xs text-gray-500 mt-1">💡 Tip: Keep it focused but descriptive. You can refine this as your research evolves.</p>
                </div>
            </div>
        `;
    }
    
    renderStep1() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="space-y-6">
                <div class="bg-green-50 p-4 rounded-lg border border-green-200">
                    <div class="flex items-center gap-2 mb-2">
                        <i data-lucide="lightbulb" class="w-5 h-5 text-green-600"></i>
                        <h3 class="font-semibold text-green-900">Problem Statement & Objectives</h3>
                    </div>
                    <p class="text-green-700 text-sm">What problem are you solving and what do you hope to achieve?</p>
                </div>
                
                <div>
                    <label class="block text-sm font-medium mb-2">Problem Statement</label>
                    <textarea
                        rows="4"
                        placeholder="Describe the problem or gap in knowledge your thesis will address..."
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        onchange="thesisFramework.updateFormData('problemStatement', this.value)"
                    >${this.formData.problemStatement}</textarea>
                </div>
                
                <div>
                    <label class="block text-sm font-medium mb-2">Research Objectives</label>
                    <div id="objectives-container">
                        ${this.formData.objectives.map((obj, index) => `
                            <div class="mb-2">
                                <input
                                    type="text"
                                    placeholder="Objective ${index + 1}: What specifically do you want to achieve?"
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    value="${obj}"
                                    onchange="thesisFramework.updateArrayItem('objectives', ${index}, this.value)"
                                />
                            </div>
                        `).join('')}
                    </div>
                    <button
                        onclick="thesisFramework.addArrayItem('objectives')"
                        class="text-blue-600 text-sm hover:text-blue-800 font-medium"
                    >
                        + Add another objective
                    </button>
                </div>

                <div>
                    <label class="block text-sm font-medium mb-2">Key Research Questions</label>
                    <div id="questions-container">
                        ${this.formData.keyQuestions.map((question, index) => `
                            <div class="mb-2">
                                <input
                                    type="text"
                                    placeholder="Research Question ${index + 1}: What key question will guide your research?"
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    value="${question}"
                                    onchange="thesisFramework.updateArrayItem('keyQuestions', ${index}, this.value)"
                                />
                            </div>
                        `).join('')}
                    </div>
                    <button
                        onclick="thesisFramework.addArrayItem('keyQuestions')"
                        class="text-blue-600 text-sm hover:text-blue-800 font-medium"
                    >
                        + Add another question
                    </button>
                </div>
            </div>
        `;
    }
    
    renderStep2() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="space-y-6">
                <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
                    <div class="flex items-center gap-2 mb-2">
                        <i data-lucide="file-text" class="w-5 h-5 text-purple-600"></i>
                        <h3 class="font-semibold text-purple-900">Methodology & Planning</h3>
                    </div>
                    <p class="text-purple-700 text-sm">How will you conduct your research and manage your timeline?</p>
                </div>
                
                <div>
                    <label class="block text-sm font-medium mb-2">Research Methodology</label>
                    <textarea
                        rows="4"
                        placeholder="Describe your planned research approach (qualitative, quantitative, mixed methods, etc.)"
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        onchange="thesisFramework.updateFormData('methodology', this.value)"
                    >${this.formData.methodology}</textarea>
                </div>
                
                <div>
                    <label class="block text-sm font-medium mb-2">Expected Timeframe</label>
                    <input
                        type="text"
                        placeholder="e.g., 18 months, 2 years, 3 semesters..."
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        value="${this.formData.timeframe}"
                        onchange="thesisFramework.updateFormData('timeframe', this.value)"
                    />
                </div>
                
                <div>
                    <label class="block text-sm font-medium mb-2">Required Resources</label>
                    <textarea
                        rows="3"
                        placeholder="What resources do you need? (access to databases, software, equipment, participants, etc.)"
                        class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        onchange="thesisFramework.updateFormData('resources', this.value)"
                    >${this.formData.resources}</textarea>
                </div>
            </div>
        `;
    }
    
    renderStep3() {
        const content = document.getElementById('content');
        content.innerHTML = `
            <div class="space-y-6">
                <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-200">
                    <div class="flex items-center gap-2 mb-2">
                        <i data-lucide="check-circle" class="w-5 h-5 text-indigo-600"></i>
                        <h3 class="font-semibold text-indigo-900">Your Thesis Framework</h3>
                    </div>
                    <p class="text-indigo-700 text-sm">Review your framework and get ready to integrate with your thesis project!</p>
                </div>
                
                <div class="bg-white border border-gray-200 rounded-lg p-4">
                    <div class="mb-4">
                        <h4 class="font-semibold text-gray-800">Research Focus</h4>
                        <p class="text-gray-600">${this.formData.researchArea || "Not specified"}</p>
                    </div>
                    
                    <div class="mb-4">
                        <h4 class="font-semibold text-gray-800">Working Title</h4>
                        <p class="text-gray-600">${this.formData.tentativeTitle || "Not specified"}</p>
                    </div>
                    
                    <div class="mb-4">
                        <h4 class="font-semibold text-gray-800">Objectives (${this.formData.objectives.filter(obj => obj.trim()).length})</h4>
                        <ul class="text-gray-600 text-sm">
                            ${this.formData.objectives.filter(obj => obj.trim()).map((obj, i) => `
                                <li class="mb-1">• ${obj}</li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
                
                <div class="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border">
                    <div class="flex items-center gap-2 mb-3">
                        <i data-lucide="zap" class="w-5 h-5 text-purple-600"></i>
                        <h3 class="font-semibold text-purple-900">Ready for Thesis Integration!</h3>
                    </div>
                    <p class="text-purple-700 text-sm mb-4">
                        Your framework is ready! Click below to download a comprehensive guide that includes specific workflows for your thesis project.
                    </p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                        <div class="bg-white p-3 rounded border">
                            <div class="flex items-center gap-1 mb-1">
                                <i data-lucide="users" class="w-3 h-3 text-blue-500"></i>
                                <span class="font-medium">Data Analysis</span>
                            </div>
                            <p class="text-gray-600">Statistical analysis, preprocessing, visualization</p>
                        </div>
                        <div class="bg-white p-3 rounded border">
                            <div class="flex items-center gap-1 mb-1">
                                <i data-lucide="file-text" class="w-3 h-3 text-green-500"></i>
                                <span class="font-medium">Documentation</span>
                            </div>
                            <p class="text-gray-600">Literature review, methodology, framework</p>
                        </div>
                        <div class="bg-white p-3 rounded border">
                            <div class="flex items-center gap-1 mb-1">
                                <i data-lucide="calendar" class="w-3 h-3 text-orange-500"></i>
                                <span class="font-medium">Project Management</span>
                            </div>
                            <p class="text-gray-600">Timeline tracking, progress monitoring</p>
                        </div>
                    </div>
                </div>
                
                <button
                    onclick="thesisFramework.generateFramework()"
                    class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center justify-center gap-2"
                >
                    <i data-lucide="download" class="w-4 h-4"></i>
                    Download Complete Framework & Integration Guide
                </button>
            </div>
        `;
    }
    
    generateFramework() {
        const framework = `# THESIS WRITING FRAMEWORK

## Research Overview
**Field/Area**: ${this.formData.researchArea}
**Tentative Title**: ${this.formData.tentativeTitle}

## Problem Statement
${this.formData.problemStatement}

## Research Objectives
${this.formData.objectives.filter(obj => obj.trim()).map((obj, i) => `${i + 1}. ${obj}`).join('\n')}

## Key Research Questions
${this.formData.keyQuestions.filter(q => q.trim()).map((q, i) => `${i + 1}. ${q}`).join('\n')}

## Methodology Approach
${this.formData.methodology}

## Timeline & Resources
**Timeframe**: ${this.formData.timeframe}
**Required Resources**: ${this.formData.resources}

## Integration with Thesis Project Framework:

### 1. Data Analysis Pipeline
- Use the Python scripts in \`code/data-analysis/\` for statistical analysis
- Leverage \`preprocess.py\` for data cleaning and preparation
- Utilize \`main_analysis.py\` for correlation, regression, and hypothesis testing

### 2. Visualization Tools
- Generate publication-ready plots with \`code/visualization/create_plots.py\`
- Create interactive visualizations for presentations
- Export figures in multiple formats (PNG, PDF, SVG)

### 3. Documentation Structure
- Update \`docs/framework.md\` with your research framework
- Use \`docs/literature-review/literature_review_template.md\` for literature review
- Document methodology in \`docs/methodology/methodology_template.md\`

### 4. Project Management
- Track progress using the project structure
- Use \`data/\` directory for your datasets
- Maintain version control with the provided \`.gitignore\`

## Recommended Workflow:
1. **Data Collection**: Store raw data in \`data/raw/\`
2. **Preprocessing**: Use \`code/data-analysis/preprocess.py\` for data cleaning
3. **Analysis**: Run statistical tests with \`code/data-analysis/main_analysis.py\`
4. **Visualization**: Create plots with \`code/visualization/create_plots.py\`
5. **Documentation**: Update framework and methodology documents
6. **Results**: Store outputs in \`results/\` directory

## Next Steps:
1. Install Python dependencies: \`pip install -r requirements.txt\`
2. Test the framework with sample data
3. Customize scripts for your specific research needs
4. Begin data collection and analysis
5. Update documentation as your research evolves

---
*Generated by Thesis Framework Assistant*
*Integrated with Python Data Analysis Framework*`;

        const blob = new Blob([framework], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'thesis-framework.md';
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Initialize the framework tool
let thesisFramework;
document.addEventListener('DOMContentLoaded', function() {
    thesisFramework = new ThesisFrameworkTool();
});
