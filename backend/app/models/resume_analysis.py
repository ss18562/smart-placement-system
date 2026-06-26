from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.db.base import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        unique=True
    )

    email = Column(String)
    phone = Column(String)

    skills = Column(Text)
    projects = Column(Text)

    education = Column(Text)
    experience = Column(Text)

    certifications = Column(Text)
    achievements = Column(Text)

    ats_score = Column(Integer)