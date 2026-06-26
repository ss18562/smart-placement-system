from sqlalchemy.orm import Session

from app.services.parsers.pdf_parser import extract_text_from_pdf

from app.services.parsers.resume_analyzer import (
    extract_email,
    extract_phone,
    extract_skills,
    extract_projects,
    calculate_completeness
)

from app.services.parsers.education_parser import (
    extract_education
)

from app.services.engines.ats_engine import analyze_resume

from app.models.resume_analysis import ResumeAnalysis


def process_resume(resume, db: Session):
    """
    Complete Resume Processing Pipeline

    Steps:
    1. Extract text from PDF
    2. Extract resume information
    3. Calculate ATS score
    4. Save analysis into database
    """

    # -------------------------
    # Extract Resume Text
    # -------------------------

    text = extract_text_from_pdf(
        resume.file_path
    )

    # -------------------------
    # Personal Details
    # -------------------------

    email = extract_email(text)
    phone = extract_phone(text)

    # -------------------------
    # Resume Sections
    # -------------------------

    skills = extract_skills(text)

    projects = extract_projects(text)

    education = extract_education(text)

    completeness = calculate_completeness(text)

    # -------------------------
    # ATS Analysis
    # -------------------------

    ats_result = analyze_resume(text)

    ats_score = ats_result["ats_score"]

    # -------------------------
    # Check Existing Analysis
    # -------------------------

    analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.resume_id == resume.id
    ).first()

    if analysis:

        analysis.email = email
        analysis.phone = phone

        analysis.skills = ",".join(skills)

        analysis.projects = ",".join(projects)

        analysis.education = ",".join(education)

        analysis.experience = ""

        analysis.certifications = ""

        analysis.achievements = ""

        analysis.ats_score = ats_score

        db.commit()
        db.refresh(analysis)

        return analysis

    # -------------------------
    # Create New Analysis
    # -------------------------

    analysis = ResumeAnalysis(

        resume_id=resume.id,

        email=email,

        phone=phone,

        skills=",".join(skills),

        projects=",".join(projects),

        education=",".join(education),

        experience="",

        certifications="",

        achievements="",

        ats_score=ats_score

    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    return analysis