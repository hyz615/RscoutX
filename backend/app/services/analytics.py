from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from datetime import datetime

from app.models.models import Team, Match
from app.services.scrapers.base_scraper import get_scraper


async def sync_team_matches(session: Session, team_number: str, event_id: str, 
                           scraper_type: str = "robotevents") -> Dict[str, Any]:
    """Sync team matches from external source to database"""
    
    # Get or create team
    statement = select(Team).where(Team.team_number == team_number)
    team = session.exec(statement).first()
    
    if not team:
        team = Team(
            team_number=team_number,
            team_name=f"Team {team_number}",
            organization="Unknown"
        )
        session.add(team)
        session.commit()
        session.refresh(team)
    
    # Fetch matches from scraper
    scraper = get_scraper(scraper_type)
    matches_data = await scraper.fetch_team_matches(team_number, event_id)
    
    # Store in database
    new_count = 0
    updated_count = 0
    
    for match_data in matches_data:
        # Check if match exists
        statement = select(Match).where(
            Match.team_id == team.id,
            Match.match_id == match_data.get('match_id'),
            Match.event_id == match_data.get('event_id')
        )
        existing_match = session.exec(statement).first()
        
        if existing_match:
            # Update existing
            for key, value in match_data.items():
                if key == 'match_date' and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                setattr(existing_match, key, value)
            existing_match.updated_at = datetime.utcnow()
            updated_count += 1
        else:
            # Create new
            match_date = match_data.get('match_date')
            if isinstance(match_date, str):
                match_date = datetime.fromisoformat(match_date)
            
            new_match = Match(
                team_id=team.id,
                match_id=match_data.get('match_id'),
                event_id=match_data.get('event_id'),
                event_name=match_data.get('event_name'),
                match_date=match_date,
                alliance=match_data.get('alliance', 'red'),
                score_for=match_data.get('score_for', 0),
                score_against=match_data.get('score_against', 0),
                result=match_data.get('result', 'unknown'),
                opponents=match_data.get('opponents'),
                rank_snapshot=match_data.get('rank_snapshot')
            )
            session.add(new_match)
            new_count += 1
    
    session.commit()
    
    return {
        "success": True,
        "team_number": team_number,
        "event_id": event_id,
        "new_matches": new_count,
        "updated_matches": updated_count,
        "total_matches": len(matches_data)
    }


def calculate_team_stats(session: Session, team_id: int, event_id: Optional[str] = None) -> Dict[str, Any]:
    """Calculate statistics for a team"""
    
    statement = select(Match).where(Match.team_id == team_id)
    if event_id:
        statement = statement.where(Match.event_id == event_id)
    
    matches = session.exec(statement).all()
    
    if not matches:
        return {
            "total_matches": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "win_rate": 0.0,
            "avg_score": 0.0,
            "avg_conceded": 0.0,
            "total_points": 0,
            "highest_score": 0,
            "lowest_score": 0
        }
    
    wins = sum(1 for m in matches if m.result == "win")
    losses = sum(1 for m in matches if m.result == "loss")
    ties = sum(1 for m in matches if m.result == "tie")
    
    total_score = sum(m.score_for for m in matches)
    total_conceded = sum(m.score_against for m in matches)
    
    scores = [m.score_for for m in matches]
    
    return {
        "total_matches": len(matches),
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "win_rate": wins / len(matches) if matches else 0.0,
        "avg_score": total_score / len(matches) if matches else 0.0,
        "avg_conceded": total_conceded / len(matches) if matches else 0.0,
        "total_points": total_score,
        "highest_score": max(scores) if scores else 0,
        "lowest_score": min(scores) if scores else 0
    }
