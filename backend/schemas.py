from pydantic import BaseModel
from typing import Optional, List

class CollegeBase(BaseModel):
    name: str
    district: str
    description: Optional[str] = ""
    courses: List[str] = []

class CourseBase(BaseModel):
    name: str
    duration: str
    eligibility: str
    fees: Optional[str] = ""
    college_name: str

class BSCCBase(BaseModel):
    course_name: str
    college_name: str
    district: str
    eligibility: str
    duration: str

class PartnerBase(BaseModel):
    name: str
    mobile: str
    district: str

class FeedbackBase(BaseModel):
    name: str
    district: str
    rating: int
    message: str
    approved: bool = False

class ContentBase(BaseModel):
    google_form_link: str
    google_drive_link: str