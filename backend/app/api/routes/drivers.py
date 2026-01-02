from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime

from app.db.session import get_session
from app.models.models import Driver
from app.schemas.schemas import DriverCreate, DriverRead, DriverUpdate

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("/", response_model=List[DriverRead])
def get_drivers(
    team_id: int = Query(None),
    session: Session = Depends(get_session)
):
    """Get all drivers, optionally filtered by team"""
    statement = select(Driver)
    if team_id:
        statement = statement.where(Driver.team_id == team_id)
    drivers = session.exec(statement).all()
    return drivers


@router.get("/{driver_id}", response_model=DriverRead)
def get_driver(driver_id: int, session: Session = Depends(get_session)):
    """Get driver by ID"""
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.post("/", response_model=DriverRead)
def create_driver(driver_data: DriverCreate, session: Session = Depends(get_session)):
    """Create new driver"""
    driver = Driver(**driver_data.dict())
    session.add(driver)
    session.commit()
    session.refresh(driver)
    return driver


@router.put("/{driver_id}", response_model=DriverRead)
def update_driver(driver_id: int, driver_data: DriverUpdate, session: Session = Depends(get_session)):
    """Update driver"""
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    update_data = driver_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(driver, key, value)
    
    driver.updated_at = datetime.utcnow()
    session.add(driver)
    session.commit()
    session.refresh(driver)
    return driver


@router.delete("/{driver_id}")
def delete_driver(driver_id: int, session: Session = Depends(get_session)):
    """Delete driver"""
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    session.delete(driver)
    session.commit()
    return {"success": True, "message": "Driver deleted"}
