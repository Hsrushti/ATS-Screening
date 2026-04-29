from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import os
import shutil

from app.services.resume_parser import (
    extract_text,
    extract_email,
    extract_phone,
    extract_name
)

from app.services.matcher import match_resume_to_jd

router = APIRouter()

UPLOAD_FOLDER = "app/uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- Helper Functions ----------

def get_status(score):
    if score >= 80:
        return "High Ranked"
    elif score >= 60:
        return "Recommended"
    elif score >= 40:
        return "Consider"
    else:
        return "Needs Review"


# ---------- Home Route ----------

@router.get("/")
def home():
    return {"message": "Backend Running Successfully"}


# ---------- Resume Parsing ----------

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)

    return {
        "filename": file.filename,
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }


# ---------- Single Resume Match ----------

@router.post("/match-resume")
async def match_resume(file: UploadFile = File(...), jd: str = Form(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text(file_path)

    raw_score = match_resume_to_jd(resume_text, jd)

    # Boost score for display
    fit_score = min(round(raw_score * 3.5), 100)

    return {
        "filename": file.filename,
        "fit_score": fit_score,
        "status": get_status(fit_score)
    }


# ---------- Bulk Resume Ranking ----------

@router.post("/bulk-match")
async def bulk_match(files: List[UploadFile] = File(...), jd: str = Form(...)):
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = extract_text(file_path)

        raw_score = match_resume_to_jd(resume_text, jd)

        results.append({
            "filename": file.filename,
            "raw_score": raw_score
        })

    # Sort by raw score descending
    ranked = sorted(results, key=lambda x: x["raw_score"], reverse=True)

    if not ranked:
        return {"ranked_candidates": []}

    top_score = ranked[0]["raw_score"]

    final_results = []

    for item in ranked:
        if top_score == 0:
            fit_score = 50
        else:
            fit_score = round((item["raw_score"] / top_score) * 100)

        final_results.append({
            "filename": item["filename"],
            "fit_score": fit_score,
            "status": get_status(fit_score)
        })

    return {
        "ranked_candidates": final_results
    }