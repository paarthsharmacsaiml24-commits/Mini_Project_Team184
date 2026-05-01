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

    st.subheader(f"Match Score: {score}%")

    st.write("Resume Skills:", resume_skills)
    st.write("Job Skills:", job_skills)
    st.write("Missing Skills:", gaps)
if not job_skills:
    st.warning("⚠️ No skills detected in job description")