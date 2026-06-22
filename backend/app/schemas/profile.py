from pydantic import BaseModel
class ProfileCreate(BaseModel):
    full_name: str
    college: str
    branch: str
    graduation_year: int
    cgpa: str
    github_url: str
    linkedin_url: str
class ProfileUpdate(ProfileCreate):
    pass

class ProfileResponse(ProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True