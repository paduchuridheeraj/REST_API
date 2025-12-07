from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from . import schemas, models, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Robot Management API",
    description="Simple REST API to manage robots, their status, and logs.",
    version="1.0.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}


@app.post(
    "/robots",
    response_model=schemas.Robot,
    status_code=status.HTTP_201_CREATED,
    tags=["robots"],
)
async def register_robot(
    body: schemas.RobotCreate,
    db: Session = Depends(get_db),
):
    try:
        robot = crud.create_robot(db, body)
        return robot
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.get(
    "/robots",
    response_model=List[schemas.Robot],
    tags=["robots"],
)
async def list_all_robots(
    db: Session = Depends(get_db),
):
    return crud.list_robots(db)


@app.get(
    "/robots/{robot_id}",
    response_model=schemas.Robot,
    tags=["robots"],
)
async def get_robot(
    robot_id: str,
    db: Session = Depends(get_db),
):
    robot = crud.get_robot(db, robot_id)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )
    return robot


@app.patch(
    "/robots/{robot_id}/status",
    response_model=schemas.Robot,
    tags=["robots"],
)
async def update_robot_status(
    robot_id: str,
    body: schemas.RobotStatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        robot = crud.update_robot_status(db, robot_id, body)
        return robot
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )


@app.post(
    "/robots/{robot_id}/logs",
    response_model=schemas.RobotLog,
    status_code=status.HTTP_201_CREATED,
    tags=["logs"],
)
async def create_robot_log(
    robot_id: str,
    body: schemas.RobotLogCreate,
    db: Session = Depends(get_db),
):
    try:
        log = crud.create_robot_log(db, robot_id, body)
        return log
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )


@app.get(
    "/robots/{robot_id}/logs",
    response_model=List[schemas.RobotLog],
    tags=["logs"],
)
async def list_robot_logs(
    robot_id: str,
    db: Session = Depends(get_db),
):
    try:
        logs = crud.get_robot_logs(db, robot_id)
        return logs
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )
