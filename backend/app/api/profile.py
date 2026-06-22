from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.profile import StudentProfile
from app.models.user import User

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse
)

from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/profile", response_model=ProfileResponse)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == current_user.id
    ).first()

    if existing_profile:
        return existing_profile

    new_profile = StudentProfile(
        user_id=current_user.id,
        full_name=profile.full_name,
        college=profile.college,
        branch=profile.branch,
        graduation_year=profile.graduation_year,
        cgpa=profile.cgpa,
        github_url=profile.github_url,
        linkedin_url=profile.linkedin_url
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get("/profile", response_model=ProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@router.put("/profile", response_model=ProfileResponse)
def update_profile(
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == current_user.id
    ).first()

    if not existing_profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    existing_profile.full_name = profile.full_name
    existing_profile.college = profile.college
    existing_profile.branch = profile.branch
    existing_profile.graduation_year = profile.graduation_year
    existing_profile.cgpa = profile.cgpa
    existing_profile.github_url = profile.github_url
    existing_profile.linkedin_url = profile.linkedin_url

    db.commit()
    db.refresh(existing_profile)

    return existing_profile