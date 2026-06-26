from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

import os
import shutil

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.models.resume import Resume
from app.models.user import User

from app.schemas.resume import ResumeResponse
from app.schemas.jd import JDRequest

# -----------------------------
# Services
# -----------------------------

from app.services.parsers.pdf_parser import extract_text_from_pdf

from app.services.parsers.resume_analyzer import (
    extract_skills,
    extract_links,
    calculate_completeness,
    extract_projects,
    extract_email,
    extract_phone
)

from app.services.parsers.education_parser import (
    extract_education
)

from app.services.engines.ats_engine import (
    analyze_resume
)

from app.services.engines.jd_match_engine import (
    match_resume_to_jd
)

from app.services.pipeline.resume_pipeline import (
    process_resume
)

router = APIRouter()

UPLOAD_DIR = "uploads"


# =====================================
# Upload Resume
# =====================================

@router.post("/resume/upload", response_model=ResumeResponse)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{current_user.id}_{file.filename}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    existing_resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if existing_resume:

        existing_resume.file_name = file.filename
        existing_resume.file_path = file_path

        db.commit()
        db.refresh(existing_resume)

        process_resume(existing_resume, db)

        return existing_resume

    new_resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    process_resume(new_resume, db)

    return new_resume


# =====================================
# Get Resume
# =====================================

@router.get("/resume", response_model=ResumeResponse)
def get_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    return resume


# =====================================
# Delete Resume
# =====================================

@router.delete("/resume")
def delete_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    db.delete(resume)
    db.commit()

    return {
        "message": "Resume deleted successfully"
    }


# =====================================
# Resume Text
# =====================================

@router.get("/resume/text")
def get_resume_text(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    text = extract_text_from_pdf(
        resume.file_path
    )

    return {
        "resume_text": text
    }


# =====================================
# ATS Score
# =====================================

@router.get("/resume/ats")
def get_ats_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    text = extract_text_from_pdf(
        resume.file_path
    )

    return analyze_resume(text)


# =====================================
# Resume Analysis
# =====================================

@router.get("/resume/analysis")
def analyze_resume_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    text = extract_text_from_pdf(
        resume.file_path
    )

    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "projects": extract_projects(text),
        "education": extract_education(text),
        "links": extract_links(text),
        "completeness_score": calculate_completeness(text)
    }


# =====================================
# Resume vs Job Description
# =====================================

@router.post("/resume/match")
def match_resume(
    jd_data: JDRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    resume_text = extract_text_from_pdf(
        resume.file_path
    )

    return match_resume_to_jd(
        resume_text,
        jd_data.job_description
    )