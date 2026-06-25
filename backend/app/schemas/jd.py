from pydantic import BaseModel

class JDRequest(BaseModel):
    job_description: str