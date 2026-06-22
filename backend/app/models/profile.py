from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class StudentProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True
    )

    full_name = Column(String)
    college = Column(String)
    branch = Column(String)
    graduation_year = Column(Integer)
    cgpa = Column(String)

    github_url = Column(String)
    linkedin_url = Column(String)