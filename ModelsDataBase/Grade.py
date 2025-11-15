from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from ModelsDataBase.DataBase import Base

class Grade(Base):
    __tablename__ = "grades"

    id            = Column(Integer, primary_key=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    date          = Column(Date,   nullable=False)
    subject       = Column(String, nullable=False)
    grade_value   = Column(Float,  nullable=False)
    comment       = Column(String, default="")
