from fastapi import FastAPI, Request, Form, UploadFile, File, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
import os
import shutil
import tempfile
import json
import pandas as pd
import io

import data
import app
import database

# Initialize database tables as soon as the module is imported
print("[DB] Initializing MySQL database...")
database.init_db()

app_root = FastAPI(debug=True)

# Global config for Gemini
GEMINI_API_KEY = "AIzaSyB1tgFTSQP9D2I0hSV2pBeBWlx4mz_-l8o"

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
# Register tojson filter in Jinja2 environment
templates.env.filters['tojson'] = json.dumps
app_root.mount("/static", StaticFiles(directory="static"), name="static")


def parse_db_json(field_data):
    """Safely parse JSON from DB results.
    MySQL connector v9 returns JSON columns as native Python dicts.
    Older connectors or SQLite return them as strings.
    """
    if field_data is None:
        return {}
    if isinstance(field_data, (dict, list)):
        return field_data  # Already a Python object (MySQL connector v9)
    if isinstance(field_data, str):
        try:
            return json.loads(field_data)
        except Exception:
            return {}
    return {}

def serialize_row(row: dict) -> dict:
    """Convert a MySQL row dict into a Jinja2-safe flat dict.
    Ensures all values are Python primitives (str, int, float, bool, None).
    Converts datetimes to strings and nested dicts to JSON strings.
    """
    safe = {}
    for k, v in row.items():
        if isinstance(v, (dict, list)):
            safe[k] = json.dumps(v)  # Serialize nested to string for template safety
        elif hasattr(v, 'isoformat'):  # datetime / date
            safe[k] = str(v)
        else:
            safe[k] = v
    return safe

def get_combined_roles():
    """Merges built-in job roles with custom ones from DB."""
    all_roles = data.JOB_ROLES.copy()
    custom_roles = database.get_custom_roles()
    all_roles.update(custom_roles)
    return all_roles

@app_root.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    reports = database.get_reports()
    total_resumes = len(reports)
    avg_match = round(sum([r['readiness_score'] for r in reports]) / total_resumes if total_resumes > 0 else 0)
    # Calculate shortlisted count (score >= 30%)
    shortlisted_count = len([r for r in reports if r['readiness_score'] >= 30])
    all_roles = get_combined_roles()
    
    # Enrich reports with display names (Real Name or Filename)
    enriched_reports = []
    for r in reports[:5]:
        analysis = parse_db_json(r['analysis_json'])
        display_name = analysis.get('name', r['filename'])
        if display_name == 'N/A' or not display_name: display_name = r['filename']
        
        enriched_reports.append({
            **serialize_row(r),
            "display_name": display_name
        })
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "active_page": "dashboard",
        "total_resumes": total_resumes,
        "avg_match": avg_match,
        "shortlisted": shortlisted_count,
        "recent_reports": enriched_reports,
        "all_roles": all_roles
    })

@app_root.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    all_roles = get_combined_roles()
    return templates.TemplateResponse("upload.html", {
        "request": request, 
        "active_page": "upload",
        "roles": all_roles,
        "all_roles": all_roles
    })

@app_root.post("/analyze")
async def analyze_resume(request: Request, role_id: str = Form(...), file: UploadFile = File(...)):
    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Run core logic from app.py
        text = app.ResumeParser.extract_text(tmp_path)
        extractor = app.SkillExtractor(data.SKILLS_TAXONOMY)
        user_skills = extractor.extract_skills(text)
        
        # Extract contact info using Gemini
        contact_info = app.ContactExtractor.extract_info(text, api_key=GEMINI_API_KEY)
        
        # We need to make sure GapAnalyzer uses the combined roles
        roles = get_combined_roles()
        if role_id not in roles:
            return {"error": "Role not found"}
            
        role_info = roles[role_id]
        analysis = app.GapAnalyzer.analyze(user_skills, role_id, roles_taxonomy=roles)
        
        # Add metadata and AI extracted details
        analysis['filename'] = file.filename
        analysis['role_id'] = role_id
        analysis['name'] = contact_info.get('name', 'N/A')
        analysis['email'] = contact_info.get('email', 'N/A')
        analysis['phone'] = contact_info.get('phone', 'N/A')
        analysis['role_name'] = role_info['name']
        analysis['learning_path'] = app.LearningPathGenerator.generate(analysis)
        
        # Save to DB
        report_id = database.save_report(file.filename, role_id, analysis['readiness_score'], analysis)
        
        return RedirectResponse(url=f"/report/{report_id}", status_code=303)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app_root.get("/report/{report_id}", response_class=HTMLResponse)
async def view_report(request: Request, report_id: int):
    row = database.get_report(report_id)
    if not row:
        return RedirectResponse(url="/")
        
    report_data = parse_db_json(row['analysis_json'])
    all_roles = get_combined_roles()
    
    return templates.TemplateResponse("report.html", {
        "request": request,
        "active_page": "reports",
        "report": report_data,
        "report_id": report_id,
        "all_roles": all_roles
    })

@app_root.get("/reports", response_class=HTMLResponse)
async def list_reports(request: Request):
    reports = database.get_reports()
    total_resumes = len(reports)
    avg_match = round(sum([r['readiness_score'] for r in reports]) / total_resumes if total_resumes > 0 else 0)
    shortlisted_count = len([r for r in reports if r['readiness_score'] >= 30])
    
    enriched_reports = []
    for r in reports:
        analysis = parse_db_json(r['analysis_json'])
        display_name = analysis.get('name', r['filename'])
        if display_name == 'N/A' or not display_name: display_name = r['filename']
        enriched_reports.append({**serialize_row(r), "display_name": display_name})

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "active_page": "reports",
        "total_resumes": total_resumes,
        "avg_match": avg_match,
        "shortlisted": shortlisted_count,
        "recent_reports": enriched_reports
    })

@app_root.get("/gap-analysis/{report_id}", response_class=HTMLResponse)
async def view_gap_analysis(request: Request, report_id: int):
    row = database.get_report(report_id)
    if not row:
        return RedirectResponse(url="/")
        
    report_data = parse_db_json(row['analysis_json'])
    if 'role_id' not in report_data:
        report_data['role_id'] = row['role_id']
        
    all_reports = database.get_reports()
    all_roles = get_combined_roles()
    
    return templates.TemplateResponse("gap_analysis.html", {
        "request": request,
        "active_page": "gap_analysis",
        "report": report_data,
        "report_id": report_id,
        "all_reports": [{"id": r['id'], "filename": r['filename'], "role_id": r['role_id']} for r in all_reports],
        "all_roles": all_roles
    })

@app_root.get("/gap-analysis", response_class=HTMLResponse)
async def recent_gap(request: Request):
    reports = database.get_reports()
    if reports:
        return RedirectResponse(url=f"/gap-analysis/{reports[0]['id']}")
    return RedirectResponse(url="/upload")

@app_root.get("/job-manager", response_class=HTMLResponse)
async def job_manager(request: Request):
    all_roles = get_combined_roles()
    return templates.TemplateResponse("job_manager.html", {
        "request": request,
        "active_page": "job_manager",
        "taxonomy": data.SKILLS_TAXONOMY,
        "all_roles": all_roles
    })

@app_root.post("/add-role")
async def add_role(request: Request):
    form_data = await request.form()
    role_name = form_data.get("name")
    role_desc = form_data.get("description")
    role_id = role_name.lower().replace(" ", "_")
    
    skills = {}
    for key, value in form_data.items():
        if key.startswith("skill_") and int(value) > 0:
            skills[key.replace("skill_", "")] = int(value)
            
    database.save_custom_role(role_id, role_name, role_desc, skills)
    return RedirectResponse(url="/job-manager", status_code=303)

@app_root.get("/download-shortlisted")
async def download_shortlisted():
    reports = database.get_reports()
    shortlisted_data = []
    combined_roles = get_combined_roles()
    
    for r in reports:
        if r['readiness_score'] >= 30:
            analysis = parse_db_json(r['analysis_json'])
            role_name = combined_roles.get(r['role_id'], {}).get('name', r['role_id'])
            
            # Use Extracted Name if available
            real_name = analysis.get('name', r['filename'])
            if real_name == 'N/A' or not real_name: real_name = r['filename']
            
            shortlisted_data.append({
                "Candidate Name": real_name,
                "Job Role": role_name,
                "Match Score": f"{r['readiness_score']}%",
                "Email": analysis.get('email', 'N/A'),
                "Phone": analysis.get('phone', 'N/A')
            })
    
    if not shortlisted_data:
        shortlisted_data = [{"Candidate Name": "No candidates meet threshold", "Job Role": "", "Match Score": "", "Email": "", "Phone": ""}]

    df = pd.DataFrame(shortlisted_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Shortlisted Candidates')
    
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=shortlisted_candidates.xlsx"}
    )

if __name__ == "__main__":
    import uvicorn
    # Local development run defaults to 8000
    print("Starting server on http://localhost:8000")
    uvicorn.run(app_root, host="0.0.0.0", port=8000)
