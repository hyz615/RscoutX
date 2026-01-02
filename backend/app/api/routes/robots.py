from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime

from app.db.session import get_session
from app.models.models import Robot
from app.schemas.schemas import RobotCreate, RobotRead, RobotUpdate

router = APIRouter(prefix="/robots", tags=["robots"])


@router.get("/", response_model=List[RobotRead])
def get_robots(
    team_id: int = Query(None),
    session: Session = Depends(get_session)
):
    """Get all robots, optionally filtered by team"""
    statement = select(Robot)
    if team_id:
        statement = statement.where(Robot.team_id == team_id)
    robots = session.exec(statement).all()
    return robots


@router.get("/{robot_id}", response_model=RobotRead)
def get_robot(robot_id: int, session: Session = Depends(get_session)):
    """Get robot by ID"""
    robot = session.get(Robot, robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot


@router.post("/", response_model=RobotRead)
def create_robot(robot_data: RobotCreate, session: Session = Depends(get_session)):
    """Create new robot"""
    robot = Robot(**robot_data.dict())
    session.add(robot)
    session.commit()
    session.refresh(robot)
    return robot


@router.put("/{robot_id}", response_model=RobotRead)
def update_robot(robot_id: int, robot_data: RobotUpdate, session: Session = Depends(get_session)):
    """Update robot"""
    robot = session.get(Robot, robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    
    update_data = robot_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(robot, key, value)
    
    robot.updated_at = datetime.utcnow()
    session.add(robot)
    session.commit()
    session.refresh(robot)
    return robot


@router.delete("/{robot_id}")
def delete_robot(robot_id: int, session: Session = Depends(get_session)):
    """Delete robot"""
    robot = session.get(Robot, robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    
    session.delete(robot)
    session.commit()
    return {"success": True, "message": "Robot deleted"}
