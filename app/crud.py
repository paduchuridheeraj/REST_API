from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas


def create_robot(db: Session, data: schemas.RobotCreate) -> models.Robot:
    existing = db.query(models.Robot).filter(models.Robot.id == data.id).first()
    if existing:
        raise ValueError("Robot with this ID already exists")
    robot = models.Robot(
        id=data.id,
        name=data.name,
        type=data.type,
        status=data.status,
        battery_percent=100,
        location=None,
        mode="idle",
        error_state=None,
    )
    db.add(robot)
    db.commit()
    db.refresh(robot)
    return robot


def get_robot(db: Session, robot_id: str) -> Optional[models.Robot]:
    return db.query(models.Robot).filter(models.Robot.id == robot_id).first()


def list_robots(db: Session) -> List[models.Robot]:
    return db.query(models.Robot).all()


def update_robot_status(
    db: Session,
    robot_id: str,
    data: schemas.RobotStatusUpdate,
) -> models.Robot:
    robot = db.query(models.Robot).filter(models.Robot.id == robot_id).first()
    if not robot:
        raise KeyError("Robot not found")
    if data.battery_percent is not None:
        robot.battery_percent = data.battery_percent
    if data.location is not None:
        robot.location = data.location
    if data.mode is not None:
        robot.mode = data.mode
    if data.error_state is not None:
        robot.error_state = data.error_state
    db.commit()
    db.refresh(robot)
    return robot


def create_robot_log(
    db: Session,
    robot_id: str,
    data: schemas.RobotLogCreate,
) -> models.RobotLog:
    robot = get_robot(db, robot_id)
    if not robot:
        raise KeyError("Robot not found")
    log = models.RobotLog(
        robot_id=robot_id,
        level=data.level,
        message=data.message,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_robot_logs(db: Session, robot_id: str) -> List[models.RobotLog]:
    robot = get_robot(db, robot_id)
    if not robot:
        raise KeyError("Robot not found")
    return (
        db.query(models.RobotLog)
        .filter(models.RobotLog.robot_id == robot_id)
        .order_by(models.RobotLog.timestamp.desc())
        .all()
    )
