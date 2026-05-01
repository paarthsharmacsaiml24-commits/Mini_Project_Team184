import streamlit as st
from utils import extract_text_from_pdf, preprocess, get_similarity, extract_skills, missing_skills

st.title("AI Resume–Job Matching System")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if uploaded_file and job_desc:
    resume_text = extract_text_from_pdf(uploaded_file)

    clean_resume = preprocess(resume_text)
    clean_job = preprocess(job_desc)

    score = get_similarity(clean_resume, clean_job)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)
    gaps = missing_skills(resume_skills, job_skills)

    match_skills = len(set(resume_skills) & set(job_skills))

    # ✅ ADD THIS LINE
    total_skills = len(job_skills) if job_skills else 1

    if job_skills:
        st.write(f"Candidate matches {match_skills} out of {total_skills} required skills.")
    else:
        st.write("No job skills provided for comparison.")

    skill_match_percent = (match_skills / total_skills) * 100

    st.metric("📊 Match Score", f"{score}%")
    st.metric("🧠 Skill Match", f"{round(skill_match_percent)}%")
    if resume_skills:
        for skill in resume_skills:
            st.success(skill)
    else:
        st.write("No resume skills found")
    st.write("### 💼 Job Skills")
    if job_skills:
        for skill in job_skills:
            st.info(skill)
    else:
        st.write("No job skills detected")

    if gaps:
        for skill in gaps:
            st.error(skill)
    else:
        st.success("No missing skills 🎉")
    if score > 75:
        st.success("🎯 Recommended Candidate")
    elif score > 50:
        st.warning("🤔 Consider with Improvements")
    else:
        st.error("❌ Not Suitable")
if not job_skills:
    st.warning("⚠️ No skills detected in job description")
st.write("### 🧠 Analysis")
st.write(f"Candidate matches {match_skills} out of {total_skills} required skills.")