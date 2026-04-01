# 🎯 AI-Based Skill Gap Analyzer

## Overview
The AI-Based Skill Gap Analyzer is a production-ready application designed to help job seekers and professionals identify the "gap" between their current skillset (extracted from their resume) and the requirements of their target job roles. It provides a comprehensive analysis, visual skill matrix comparisons, and a personalized learning roadmap to bridge those gaps.

## Key Features
- **Multi-Format Resume Parsing**: Supports PDF, DOCX, and TXT files.
- **Skill Extraction Engine**: Detects 100+ technical skills using NLP-based keyword matching and alias handling.
- **Job Role Matching**: Compares user skills against 8 predefined tech roles (Data Scientist, Full-Stack Engineer, ML Engineer, etc.).
- **Interactive Visualizations**: Includes Skill Radar Charts and readiness scores via Plotly.
- **Personalized Learning Path**: Generates a phased roadmap with curated resources (courses, books, projects).

## Quick Start (5 Minutes)

### 1. Prerequisites
- Python 3.8 or higher installed on your system.

### 2. Installation
Clone this repository or download the project files. 
Navigate to the project directory and run:

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK tokenizer data
python -c "import nltk; nltk.download('punkt')"
```

### 3. Run the Application
Start the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

### 4. Open in Browser
Visit `http://localhost:8501` to access the dashboard.

## Supported Job Roles
1. **Data Scientist**
2. **Full-Stack Engineer**
3. **Machine Learning Engineer**
4. **DevOps Engineer**
5. **Frontend Developer**
6. **Backend Developer**
7. **Data Analyst**
8. **Cloud Architect**

## Technology Stack
- **Frontend**: Streamlit, Plotly, Pandas
- **Backend**: Python, pdfplumber, python-docx, NLTK
- **Deployment**: Ready for Streamlit Cloud or Docker-based hosting.

## Project Structure
- `streamlit_app.py`: The interactive UI and visualization layer.
- `app.py`: Core logic for parsing, extraction, and gap analysis.
- `data.py`: Centralized taxonomy of skills, roles, and resources.
- `requirements.txt`: List of required Python packages.
- `sample_resume.txt`: A demo resume for initial testing.

---
*Built with ❤️ for rapid deployment and professional-grade skill analysis.*
