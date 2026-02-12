from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class Experience(BaseModel):
    job_title: str = Field(...)
    company: str = Field(...)
    start_date: str = Field(...) 
    end_date: Optional[str] = Field(None)
    description: Optional[str] = Field(None)

class Education(BaseModel):
    degree: str = Field(...)
    institution: str = Field(...)
    start_date: str = Field(...)
    end_date: Optional[str] = Field(None)
    domain: str = Field(...)

class Skill(BaseModel):
    technical_skills: List[str] = Field(...)
    soft_skills: List[str] = Field(...)


class Language(BaseModel):
    name: str = Field(...)
    level: str = Field(...)

class CVModel(BaseModel):
    user_id:Optional[str]=None
    template_id:int =1
    first_name: str = Field(...)
    last_name: str = Field(...)
    job_title: str = Field(...)
    address: str = Field(...) 
    code_postal: str = Field(...)
    city: str = Field(...)
    phone_number: str = Field(...)
    email: EmailStr = Field(...)
    site: Optional[str] = Field(None)
    hobbies: Optional[str] = ""
  
    experiences: List[Experience]
    educations: List[Education]
    skill: Skill
    languages: List[Language]
    summary: str = Field(...)