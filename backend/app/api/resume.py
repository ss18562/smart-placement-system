from app.services.resume_parser import extract_text_from_pdf
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.core.dependencies import get_current_user
from app.services.ats import analyze_resume
from app.services.resume_analyzer import (
    extract_skills,
    extract_links,
    calculate_completeness,
    extract_projects,
    extract_email,
    extract_phone
)
from app.schemas.jd import JDRequest
from app.services.jd_matcher import match_resume_to_jd
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads"


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

        return existing_resume

    new_resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume
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

    result = analyze_resume(text)

    return result    
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
        "links": extract_links(text),
        "completeness_score": calculate_completeness(text)
    }
   
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

    result = match_resume_to_jd(
        resume_text,
        jd_data.job_description
    )

    return result 