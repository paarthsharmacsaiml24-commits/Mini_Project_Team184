import pdfplumber
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from skills import SKILLS

import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    words = text.split()
    return " ".join(words)

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def get_similarity(resume, job_desc):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, job_desc])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def extract_skills(text):
    text = text.lower()
    found = []

    for skill, keywords in SKILL_MAP.items():
        for keyword in keywords:
            if keyword in text:
                found.append(skill)
                break

    return list(set(found))

def missing_skills(resume_skills, job_skills):
    return list(set(job_skills) - set(resume_skills))
