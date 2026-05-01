from flask import Flask, render_template, request
from utils import extract_text_from_pdf, preprocess, get_similarity, extract_skills, missing_skills

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        resume_text = extract_text_from_pdf(file)
        clean_resume = preprocess(resume_text)
        clean_job = preprocess(job_desc)

        score = get_similarity(clean_resume, clean_job)

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)
        gaps = missing_skills(resume_skills, job_skills)

        match_skills = len(set(resume_skills) & set(job_skills))
        total_skills = len(job_skills) if job_skills else 1
        skill_match = round((match_skills / total_skills) * 100)

        result = {
            "score": score,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "gaps": gaps,
            "skill_match": skill_match
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))