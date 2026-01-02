from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from app.db.session import get_session
from app.models.models import Team
from app.schemas.schemas import TeamCreate, TeamRead, TeamUpdate

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=List[TeamRead])
def get_teams(session: Session = Depends(get_session)):
    """Get all teams"""
    teams = session.exec(select(Team)).all()
    return teams


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, session: Session = Depends(get_session)):
    """Get team by ID"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/", response_model=TeamRead)
def create_team(team_data: TeamCreate, session: Session = Depends(get_session)):
    """Create new team"""
    # Check if team number already exists
    existing = session.exec(select(Team).where(Team.team_number == team_data.team_number)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team number already exists")
    
    team = Team(**team_data.dict())
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.put("/{team_id}", response_model=TeamRead)
def update_team(team_id: int, team_data: TeamUpdate, session: Session = Depends(get_session)):
    """Update team"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    update_data = team_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(team, key, value)
    
    team.updated_at = datetime.utcnow()
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.delete("/{team_id}")
def delete_team(team_id: int, session: Session = Depends(get_session)):
    """Delete team"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    session.delete(team)
    session.commit()
    return {"success": True, "message": "Team deleted"}
