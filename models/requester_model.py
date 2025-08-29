from sqlalchemy import Column, String, DateTime, Integer, Text, func , Mapped , mapped_column
from core.database import Base

class AnswerRequestModel(Base):
    __tablename__ = "answer_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    request = Column(Text, nullable=False)
    file_type = Column(String(255), nullable=False)
    date_time = Column(DateTime(timezone=True), server_default=func.now())
    response = Column(Text, nullable=False)
    
class RespostaModel(Base):
    __tablename__ = "resposta"

    id: Mapped[int] = mapped_column(primary_key=True)
    texto: Mapped[str] = mapped_column(String)