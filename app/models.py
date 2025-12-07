from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Robot(Base):
    __tablename__ = "robots"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    battery_percent = Column(Integer, default=100)
    location = Column(String, nullable=True)
    mode = Column(String, default="idle")
    error_state = Column(String, nullable=True)

    logs = relationship("RobotLog", back_populates="robot", cascade="all, delete")


class RobotLog(Base):
    __tablename__ = "robot_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    robot_id = Column(String, ForeignKey("robots.id"), nullable=False)
    level = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    robot = relationship("Robot", back_populates="logs")
