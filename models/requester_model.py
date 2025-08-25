from sqlalchemy import Column, String, DateTime, Integer, Text, func
from core.database import Base

class AnswerRequestModel(Base):
    __tablename__ = "answer_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    request = Column(Text, nullable=False)
    file_type = Column(String(255), nullable=False)
    date_time = Column(DateTime(timezone=True), server_default=func.now())
    response = Column(Text, nullable=False)