from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Subject(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    subject_code: str
    subject_name: str
    semester: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ExamSession(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    subject_code: str
    exam_date: str
    exam_time: str
    semester: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class Student(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    student_id: str
    name: str
    semester: int
    roll_number: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )