# 📋 SKILL GAP ANALYZER - IMPLEMENTATION GUIDE

## 🧠 CORE LOGIC EXPLANATION

### 1. Resume Parser (`app.py`)
- The `ResumeParser` class uses `pdfplumber` for text extraction from PDF files, providing better handling for layouts and column formats compared to standard libries like `pypdf2`.
- `python-docx` is used for Word (DOCX) files, while standard Python I/O handles ASCII or UTF-8 encoded text files.

### 2. Skill Extraction Engine (`app.py`)
- The `SkillExtractor` class tokenizes the resume text using `nltk.word_tokenize`.
- It performs normalized keyword matching across the `SKILLS_TAXONOMY` from `data.py`.
- **Note**: A frequency-to-proficiency mapping is used for skill levels (e.g., 10+ occurrences = Expert Level 4).

### 3. Gap Analyzer (`app.py`)
- The `GapAnalyzer` performs a direct comparison between the user's extracted skills and the requirements of the selected `JOB_ROLE`.
- It calculates a `readiness_score` based on the ratio of current skill levels vs. total required levels.
- **Priority Scoring**: Skills that are required at Level 3 or 4 but are missing are flagged as "High" priority gaps.

## 🎨 INTERFACE DESIGN (`streamlit_app.py`)
- The Streamlit interface is designed for simplicity and speed.
- It uses `px.pie` and `go.Scatterpolar` from Plotly for interactive data visualization.
- **Custom CSS**: Minimal CSS additions are used to enhance cards and skill highlight colors.

## 🛠️ EXTENDING THE SYSTEM

### To Add New Skills:
1.  Open `data.py`.
2.  Add a new entry to the `SKILLS_TAXONOMY` dictionary.
3.  Include relevant aliases (e.g., "K8s" for "Kubernetes").

### To Add New Job Roles:
1.  Open `data.py`.
2.  Add a new role to the `JOB_ROLES` dictionary.
3.  Define the required skill levels (1-4) for this role.

### To Improve Natural Language Processing (NLP):
- Replace the keyword matching logic in `app.py` with an NLP model like `spaCy` or `HuggingFace Transformers` for more advanced Named Entity Recognition (NER).
- This will allow the system to detect skills from broader contexts rather than just keyword frequency.

## 🚀 DEPLOYMENT OPTIONS

- **Streamlit Cloud**: Connect your GitHub repository to [Streamlit Community Cloud](https://streamlit.io/cloud) for a one-click deployment.
- **Docker**: Build a simple Docker image using the provided `requirements.txt` and an `EXPOSE 8501` command in your Dockerfile.
- **FastAPI/React**: Use the core logic from `app.py` as a REST API backend with a custom React/Vue frontend for high-performance enterprise applications.
