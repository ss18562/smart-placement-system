from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str

    class Config:
        from_attributes = True