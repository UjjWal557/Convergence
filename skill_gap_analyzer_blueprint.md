# 🎯 SKILL GAP ANALYZER - SYSTEM BLUEPRINT

## 🧩 ARCHITECTURE OVERVIEW

### 1. Presentation Layer (Frontend)
- **Framework**: Streamlit.
- **Visuals**: Plotly for radar charts and pie charts.
- **State**: `SessionState` for session-level persistence.
- **Interaction**: File uploader, selectboxes, and interactive expanders.

### 2. Logic Layer (Backend)
- **Parsing**: `pdfplumber`, `python-docx`, and standard I/O for text files.
- **NLP**: `NLTK` for tokenization and word boundary detection.
- **Extraction**: Alias matching engine for skill identification from resumes.
- **Analysis**: Gap analysis algorithm for target role matching.
- **Recommendation**: Dynamic learning path generator based on gap severity.

### 3. Data Layer (Repository)
- **Skill Taxonomy**: 100+ technical skills with categories and aliases.
- **Job Roles**: 8 tech roles with weighted skill requirements.
- **Resources**: 200+ curated links to courses, books, and projects.

## ⚙️ SYSTEM WORKFLOW

1.  **Ingestion**: User uploads a resume (PDF/DOCX/TXT).
2.  **Extraction**: The system cleans the text and tokenizes it using NLTK.
3.  **Identification**: Keywords and aliases are matched against the `data.SKILLS_TAXONOMY`.
4.  **Inference**: Proficiency is inferred based on keyword frequency and context.
5.  **Role Comparison**: The target role requirements are pulled from `data.JOB_ROLES`.
6.  **Scoring**: A "Readiness Score" is calculated using a weighted comparison of user vs. role skills.
7.  **Gap Prioritization**: Missing or low-proficiency skills are prioritized for improvement.
8.  **Roadmap Generation**: A phased learning plan is created, linking to `data.LEARNING_RESOURCES`.

## 📈 SCALABILITY & FUTURE ENHANCEMENTS

- **Database**: Port taxonomy and job roles to PostgreSQL.
- **ML Integration**: Use BERT-based models for advanced Named Entity Recognition (NER).
- **Multi-lingual Support**: Add language-specific tokenizers and skill aliases.
- **Portfolio Tracking**: Integrate with GitHub/LinkedIn APIs to track user skill growth over time.
- **Cloud Deployment**: Containerize with Docker for AWS/GCP deployment.
