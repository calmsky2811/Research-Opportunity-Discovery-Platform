import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# LOAD DATA
# =========================

faculty_df = pd.read_csv("data/faculty.csv")

faculty_df.columns = faculty_df.iloc[0]
faculty_df = faculty_df[1:].reset_index(drop=True)

papers_df = pd.read_csv("data/papers.csv")

print("Faculty:", faculty_df.shape)
print("Papers:", papers_df.shape)

# =========================
# LOAD MODEL
# =========================

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")

# =========================
# FACULTY EMBEDDINGS
# =========================

faculty_texts = (
    faculty_df["Research_Areas"].fillna("")
    + " "
    + faculty_df["Skills"].fillna("")
)

print("Creating faculty embeddings...")

faculty_embeddings = model.encode(
    faculty_texts.tolist(),
    show_progress_bar=True
)

print("Faculty embeddings shape:", faculty_embeddings.shape)

# =========================
# PAPER EMBEDDINGS
# =========================

paper_texts = (
    papers_df["Title"].fillna("")
    + " "
    + papers_df["Abstract"].fillna("")
)

print("Creating paper embeddings...")

paper_embeddings = model.encode(
    paper_texts.tolist(),
    show_progress_bar=True
)

print("Paper embeddings shape:", paper_embeddings.shape)

# =========================
# RECOMMEND FACULTY
# =========================

def recommend_faculty(query):

    query_embedding = model.encode([query])

    scores = cosine_similarity(
        query_embedding,
        faculty_embeddings
    )[0]

    top_indices = np.argsort(scores)[-5:][::-1]

    results = faculty_df.iloc[top_indices].copy()

    results["Match_Score"] = (
        scores[top_indices] * 100
    ).round(2)

    return results

# =========================
# RECOMMEND PAPERS
# =========================

def recommend_papers(query):

    query_embedding = model.encode([query])

    scores = cosine_similarity(
        query_embedding,
        paper_embeddings
    )[0]

    top_indices = np.argsort(scores)[-5:][::-1]

    results = papers_df.iloc[top_indices].copy()

    results["Match_Score"] = (
        scores[top_indices] * 100
    ).round(2)

    return results

# =========================
# SKILL GAP ANALYSIS
# =========================

def find_skill_gap(student_skills, faculty_skills):

    student_set = {
        skill.strip().lower()
        for skill in student_skills.split(",")
        if skill.strip()
    }

    faculty_set = {
        skill.strip()
        for skill in faculty_skills.split(",")
        if skill.strip()
    }

    missing_skills = []

    for skill in faculty_set:

        if skill.lower() not in student_set:

            missing_skills.append(skill)

    return missing_skills