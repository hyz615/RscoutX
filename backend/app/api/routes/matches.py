from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.models import Match
from app.schemas.schemas import MatchRead
from app.services.analytics import sync_team_matches, calculate_team_stats

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/sync", response_model=Dict[str, Any])
async def sync_matches(
    team: str = Query(..., description="Team number"),
    event: str = Query(..., description="Event ID"),
    scraper: str = Query("robotevents", description="Scraper type"),
    session: Session = Depends(get_session)
):
    """Sync team matches from external source"""
    try:
        result = await sync_team_matches(session, team, event, scraper)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/{team_id}", response_model=Dict[str, Any])
def get_team_stats(
    team_id: int,
    event_id: str = Query(None),
    session: Session = Depends(get_session)
):
    """Get statistics for a team"""
    stats = calculate_team_stats(session, team_id, event_id)
    return stats


@router.get("/", response_model=List[MatchRead])
def get_matches(
    team_id: int = Query(None),
    event_id: str = Query(None),
    session: Session = Depends(get_session)
):
    """Get matches, optionally filtered by team and/or event"""
    statement = select(Match)
    if team_id:
        statement = statement.where(Match.team_id == team_id)
    if event_id:
        statement = statement.where(Match.event_id == event_id)
    
    statement = statement.order_by(Match.match_date.desc())
    matches = session.exec(statement).all()
    return matches


@router.get("/{match_id}", response_model=MatchRead)
def get_match(match_id: int, session: Session = Depends(get_session)):
    """Get match by ID"""
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match
