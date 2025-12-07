from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class RobotBase(BaseModel):
    name: str = Field(..., example="Warehouse Bot A1")
    type: str = Field(..., example="picker")
    status: str = Field(..., example="online")


class RobotCreate(RobotBase):
    id: str = Field(..., example="robot-001")


class Robot(RobotBase):
    id: str
    battery_percent: int = Field(100, ge=0, le=100, example=86)
    location: Optional[str] = Field(None, example="Aisle 5")
    mode: str = Field("idle", example="idle")
    error_state: Optional[str] = Field(None, example="motor_overheat")

    class Config:
        orm_mode = True


class RobotStatusUpdate(BaseModel):
    battery_percent: Optional[int] = Field(None, ge=0, le=100, example=72)
    location: Optional[str] = Field(None, example="Dock 3")
    mode: Optional[str] = Field(None, example="charging")
    error_state: Optional[str] = Field(None, example="low_battery")


class RobotLogCreate(BaseModel):
    level: str = Field(..., example="info")
    message: str = Field(..., example="Robot started picking order #1023")


class RobotLog(BaseModel):
    id: int
    robot_id: str
    level: str
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True


class ErrorResponse(BaseModel):
    detail: str
