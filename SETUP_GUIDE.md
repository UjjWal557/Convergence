# 🛠️ SETUP AND DEMO GUIDE

## 📋 Prerequisites
- **Python**: Version 3.8 or higher.
- **System**: Windows, Mac, or Linux.
- **RAM**: Minimum 4GB (8GB+ recommended).

## 🚀 Quick Setup (5 Minutes)

### 1. Extract Project Files
Unzip or clone the project folder into a local directory.

### 2. Create Virtual Environment
Open your terminal or command prompt and navigate to the project directory:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Run the following command to install all required libraries:

```bash
pip install -r requirements.txt
```

### 4. Initialize NLTK Data
Download the necessary NLP tokenizer:

```bash
python -c "import nltk; nltk.download('punkt')"
```

## 🎥 Running the Demo (Walkthrough)

### Step 1: Start the Dashboard
Launch the Streamlit application:

```bash
streamlit run streamlit_app.py
```

### Step 2: Upload Resume
Drag and drop the `sample_resume.txt` from the project root into the "Upload Resume" section in the sidebar.

### Step 3: Select Target Role
In the sidebar, choose "Data Scientist" (or any other role from the dropdown).

### Step 4: Run Analysis
Click the **🚀 Run Analysis** button and wait 1-2 seconds.

### Step 5: Explore Results
1.  **Dashboard Visuals**: Check the *Skill Radar Comparison* and the *Matched vs Missing* pie chart.
2.  **Detailed Gaps**: Scroll down to see the color-coded skill breakdown.
3.  **Roadmap**: Expand the *Personalized Learning Roadmap* sections to see the phased plan and curated resources.

## 🛠️ Common Issues & Fixes

- **Error: "ModuleNotFoundError"**: Ensure the `venv` is active and you ran `pip install -r requirements.txt`.
- **Low Accuracy in Skill Detection**: Resume text must be clear. PDF files with image-based text (scanned) are not supported unless OCR is added. Use text-based PDFs or DOCX files for best results.
- **Port already in use**: If `8501` is taken, Streamlit will automatically try `8502`, etc. You can specify a port with `streamlit run streamlit_app.py --server.port 8080`.

## 🎓 Viva Preparation Questions

1.  **How are skills extracted?**
    - The system uses a keyword-based approach with normalization and alias handling (e.g., "Python" and "Py" maps to the same skill ID). It tokenizes the resume text using NLTK to find exact word boundaries.
2.  **How is the readiness score calculated?**
    - It's a weighted sum of the user's proficiency vs. the job's required proficiency. Meeting a core skill requirement contributes more to the score than a secondary skill.
3.  **Can I add more job roles?**
    - Yes, simply update the `JOB_ROLES` dictionary in `data.py` with the new role's ID, name, and skill requirements.
4.  **Is the system scalable?**
    - Currently, it's designed for single-user local or cloud-based analysis. For enterprise scale, a database like PostgreSQL and an asynchronous task queue like Celery would be needed for handling large volumes of resumes.
