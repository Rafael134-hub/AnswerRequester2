from typing import Optional
from pydantic import BaseModel as SCBaseModel
from datetime import datetime

class ApiRequesterCreateSchema(SCBaseModel):
    request: str
    file_type: str

class ApiRequesterSchema(SCBaseModel):

    request_id: Optional[int] = None
    request: str
    response: Optional[str]
    file_type: str
    date_time: Optional[datetime] = None

    class Config:
        orm_mode = True