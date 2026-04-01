import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import ResumeParser, SkillExtractor, GapAnalyzer, LearningPathGenerator
import data
import tempfile
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI-Based Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Dark Theme Core */
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2c, #0d0f17);
        color: #ffffff;
    }
    
    /* Ensure all text is visible */
    .stMarkdown, p, li, h1, h2, h3, span {
        color: #ffffff !important;
    }
    
    /* Premium Metric Style */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Button enhancements */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        border: none;
        border-radius: 12px;
        color: white !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
    }

    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
    }

</style>
""", unsafe_allow_html=True)

def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🎯 AI Skill Analyzer")
        st.info("Upload your resume and select a target role to analyze your skill gaps.")
        
        uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'txt'])
        
        role_options = {role_id: info['name'] for role_id, info in data.JOB_ROLES.items()}
        selected_role_id = st.selectbox("Target Job Role", options=list(role_options.keys()), format_func=lambda x: role_options[x])
        
        analyze_btn = st.button("🚀 Run Analysis")

    # --- MAIN CONTENT ---
    st.title("Skill Gap Analysis Dashboard")
    
    if analyze_btn and uploaded_file:
        with st.spinner("Analyzing your resume..."):
            # Save uploaded file temporarily to process it
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                # 1. Extraction
                text = ResumeParser.extract_text(tmp_path)
                extractor = SkillExtractor(data.SKILLS_TAXONOMY)
                user_skills = extractor.extract_skills(text)
                
                # 2. Gap Analysis
                results = GapAnalyzer.analyze(user_skills, selected_role_id)
                
                # 3. Learning Path
                learning_path = LearningPathGenerator.generate(results)
                
                # Clean up temp file
                os.remove(tmp_path)

                # --- DASHBOARD UI ---
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    st.metric("Readiness Score", f"{results['readiness_score']}%", delta=f"{results['readiness_score']-50}% vs. Avg")
                
                with col2:
                    st.metric("Skills Matched", f"{len(results['matched_skills'])}", f"of {len(data.JOB_ROLES[selected_role_id]['skills'])}")
                
                with col3:
                    st.metric("Total Gap Points", f"{results['total_gap_points']}", delta_color="inverse")

                # --- VISUALIZATIONS ---
                st.markdown("---")
                v_col1, v_col2 = st.columns([1, 1])
                
                with v_col1:
                    # Radar Chart
                    st.subheader("Skill Matrix Comparison")
                    df_radar = pd.DataFrame(results['skill_radar_data'])
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=df_radar['Required'],
                        theta=df_radar['Skill'],
                        fill='toself',
                        name='Required'
                    ))
                    fig.add_trace(go.Scatterpolar(
                        r=df_radar['Actual'],
                        theta=df_radar['Skill'],
                        fill='toself',
                        name='Your Skills'
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 4])),
                        showlegend=True,
                        height=450,
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with v_col2:
                    st.subheader("Skill Breakdown")
                    # Matched vs Missing pie chart
                    labels = ['Matched', 'Missing']
                    values = [len(results['matched_skills']), len(results['missing_skills'])]
                    fig_pie = px.pie(names=labels, values=values, color_discrete_sequence=['#2ecc71', '#e74c3c'], hole=0.5)
                    fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_pie, use_container_width=True)

                # --- DETAILED ANALYSIS ---
                st.subheader("Detailed Gap Analysis")
                tab1, tab2 = st.tabs(["Matched Skills", "Missing Skills"])
                
                with tab1:
                    for skill in results['matched_skills']:
                        st.markdown(f"✅ **{skill['skill']}**: Level {skill['level']} (Required: {skill['req']})")
                
                with tab2:
                    for skill in results['missing_skills']:
                        priority_color = "red" if skill['priority'] == "High" else "orange"
                        st.markdown(f"❌ **{skill['skill']}**: Level 0 (Required: {skill['req']}) - Priority: :{priority_color}[{skill['priority']}]")

                # --- LEARNING PATH ---
                st.markdown("---")
                st.subheader("Personalized Learning Roadmap")
                
                for phase in learning_path:
                    with st.expander(f"📌 {phase['phase']} - {phase['duration']}", expanded=True):
                        st.write(f"**Focus:** {phase['focus']}")
                        st.write(f"**Skills to Learn:** {', '.join(phase['skills'])}")
                        
                        if phase['resources']:
                            st.write("**Recommended Resources:**")
                            for res in phase['resources']:
                                st.markdown(f"- [{res['name']}]({res['url']}) ({res['type']})")
                        else:
                            st.write("No specific resources currently in database. Check general documentation.")

            except Exception as e:
                st.error(f"Error processing analysis: {str(e)}")

    elif not analyze_btn:
        # Welcome Screen
        st.markdown("""
        <div class="card">
            <h2>Welcome to the AI Skill Analyzer! 🚀</h2>
            <p>This tool helps you identify the gap between your current skills and the requirements of top tech roles.</p>
            <h3>How to use:</h3>
            <ol>
                <li>Upload your <b>Resume</b> (PDF, DOCX, or TXT).</li>
                <li>Select your <b>Target Job Role</b> from the sidebar.</li>
                <li>Click <b>Run Analysis</b> to see your results and learning roadmap.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("Don't have a resume handy? Try downloading the sample_resume.txt from the repository root!")

if __name__ == "__main__":
    main()
