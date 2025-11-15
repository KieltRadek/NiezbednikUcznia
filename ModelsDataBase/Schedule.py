from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date
from ModelsDataBase.DataBase import Base

class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    day_of_week = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    subject = Column(String)
    room = Column(String)
    date = Column(Date)
    type = Column(String)
    student_count = Column(Integer)
    teacher = Column(String)
    code = Column(String)
    group = Column(String)
    building = Column(String)