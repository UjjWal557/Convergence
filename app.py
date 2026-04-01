import re
import os
import nltk
from nltk.tokenize import word_tokenize
import pdfplumber
import docx
import json
import pandas as pd
from google import genai
from google.genai import types
from typing import Dict, List, Tuple
import data

# Ensure NLTK data is available
# NLTK punkt is assumed to be ready

class ResumeParser:
    """Parses resumes in various formats (PDF, DOCX, TXT)."""
    @staticmethod
    def extract_text(file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return ResumeParser._parse_pdf(file_path)
        elif ext == '.docx':
            return ResumeParser._parse_docx(file_path)
        elif ext == '.txt':
            return ResumeParser._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _parse_pdf(path: str) -> str:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def _parse_docx(path: str) -> str:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])

    @staticmethod
    def _parse_txt(path: str) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

class GeminiExtractor:
    """Uses Google Gemini to extract precise candidate details."""
    def __init__(self, api_key: str):
        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            print(f"Gemini Init Error: {e}")
            self.client = None

    def extract_details(self, resume_text: str) -> Dict[str, str]:
        if not self.client:
            return {"name": "N/A", "email": "N/A", "phone": "N/A"}

        prompt = f"""Extract the following details from the resume text:
1. Full Name of the candidate
2. Email Address
3. Phone Number

Return ONLY a JSON object with keys: "name", "email", "phone".
If a detail is missing, use "N/A".

Resume Text:
{resume_text[:4000]}"""
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
            return {"name": "N/A", "email": "N/A", "phone": "N/A"}
        except Exception as e:
            print(f"Gemini Extraction Error: {e}")
            return {"name": "N/A", "email": "N/A", "phone": "N/A"}

class ContactExtractor:
    """High-level extractor combining Regex and AI for contact details."""
    @staticmethod
    def extract_info(text: str, api_key: str = None) -> Dict[str, str]:
        # If API key is available, prioritize Gemini for 100% accuracy
        if api_key:
            gemini = GeminiExtractor(api_key)
            return gemini.extract_details(text)

        # Fallback to simple regex if no API key
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'(\+?\d[\d -]{8,}\d)'
        
        email_match = re.search(email_pattern, text)
        phone_match = re.search(phone_pattern, text)
        
        return {
            "name": "N/A",
            "email": email_match.group(0) if email_match else "N/A",
            "phone": phone_match.group(0) if phone_match else "N/A"
        }

class SkillExtractor:
    """Extracts and evaluates skills from resume text."""
    def __init__(self, taxonomy: Dict):
        self.taxonomy = taxonomy

    def extract_skills(self, text: str) -> Dict[str, int]:
        """Simple keyword-based extraction with frequency mapping to proficiency."""
        text = text.lower()
        tokens = word_tokenize(text)
        found_skills = {}

        # Look for skills from taxonomy
        for skill_id, info in self.taxonomy.items():
            count = 0
            # Check for name and aliases
            patterns = [info['name'].lower()] + info['aliases']
            for pattern in patterns:
                # Use regex for word boundaries
                matches = re.findall(rf'\b{re.escape(pattern)}\b', text)
                count += len(matches)
            
            if count > 0:
                # Map count to proficiency (1-4)
                if count >= 10: level = 4
                elif count >= 5: level = 3
                elif count >= 2: level = 2
                else: level = 1
                found_skills[skill_id] = level
        
        return found_skills

class GapAnalyzer:
    """Compares extracted skills against job requirements."""
    @staticmethod
    def analyze(user_skills: Dict[str, int], target_role_id: str, roles_taxonomy: Dict = None) -> Dict:
        taxonomy = roles_taxonomy if roles_taxonomy else data.JOB_ROLES
        if target_role_id not in taxonomy:
            return {"error": "Role not found"}

        role_info = taxonomy[target_role_id]
        required_skills = role_info['skills']
        
        analysis = {
            "role_name": role_info['name'],
            "matched_skills": [],
            "missing_skills": [],
            "skill_radar_data": [],
            "readiness_score": 0,
            "total_gap_points": 0
        }

        total_possible_score = sum(required_skills.values())
        current_score = 0

        for skill_id, req_level in required_skills.items():
            user_level = user_skills.get(skill_id, 0)
            skill_name = data.SKILLS_TAXONOMY.get(skill_id, {}).get('name', skill_id)

            # Radar chart data: skill, required, actual
            analysis["skill_radar_data"].append({
                "Skill": skill_name,
                "Required": req_level,
                "Actual": user_level
            })

            if user_level >= req_level:
                analysis["matched_skills"].append({
                    "skill": skill_name, 
                    "level": user_level, 
                    "req": req_level
                })
                current_score += req_level 
            elif user_level > 0:
                # Partial match
                analysis["matched_skills"].append({
                    "skill": skill_name, 
                    "level": user_level, 
                    "req": req_level,
                    "gap": req_level - user_level
                })
                current_score += user_level
                analysis["total_gap_points"] += (req_level - user_level)
            else:
                analysis["missing_skills"].append({
                    "skill": skill_name, 
                    "req": req_level,
                    "priority": "High" if req_level >= 3 else "Normal"
                })
                analysis["total_gap_points"] += req_level

        # Calculate readiness percentage
        analysis["readiness_score"] = round((current_score / total_possible_score) * 100) if total_possible_score > 0 else 0
        
        return analysis

class LearningPathGenerator:
    """Generates a roadmap for bridging skill gaps."""
    @staticmethod
    def generate(analysis: Dict) -> List[Dict]:
        path = []
        
        # Prioritize missing skills and major gaps
        critical_skills = [s for s in analysis["missing_skills"] if s["priority"] == "High"]
        if critical_skills:
            path.append({
                "phase": "Phase 1: Foundation (Critical Gaps)",
                "duration": f"{len(critical_skills) * 2} - {len(critical_skills) * 4} weeks",
                "focus": "Addressing skills essential for the role.",
                "skills": [s["skill"] for s in critical_skills],
                "resources": LearningPathGenerator._get_resources(critical_skills)
            })

        moderate_skills = [s for s in analysis["missing_skills"] if s["priority"] == "Normal"]
        if moderate_skills:
            path.append({
                "phase": "Phase 2: Core Competencies",
                "duration": f"{len(moderate_skills) * 1} - {len(moderate_skills) * 2} weeks",
                "focus": "Expanding your toolkit with secondary requirements.",
                "skills": [s["skill"] for s in moderate_skills],
                "resources": LearningPathGenerator._get_resources(moderate_skills)
            })

        growth_skills = [s for s in analysis["matched_skills"] if s.get("gap", 0) > 0]
        if growth_skills:
            path.append({
                "phase": "Phase 3: Advanced Optimization",
                "duration": "Ongoing",
                "focus": "Deepening knowledge in systems you already know.",
                "skills": [s["skill"] for s in growth_skills],
                "resources": LearningPathGenerator._get_resources(growth_skills)
            })

        return path

    @staticmethod
    def _get_resources(skill_list: List[Dict]) -> List[Dict]:
        all_resources = []
        for s in skill_list:
            skill_id = None
            for key, info in data.SKILLS_TAXONOMY.items():
                if info['name'] == s['skill']:
                    skill_id = key
                    break
            
            if skill_id and skill_id in data.LEARNING_RESOURCES:
                all_resources.extend(data.LEARNING_RESOURCES[skill_id])
        return all_resources[:5]
