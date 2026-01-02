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
    scraper_result = await scraper.fetch_team_matches(team_number, event_id)
    
    # Extract matches and team info
    matches_data = scraper_result.get("matches", [])
    team_info = scraper_result.get("team_info")
    
    # Update team information if we got it from the API
    if team_info:
        team.team_name = team_info.get("team_name", team.team_name)
        team.organization = team_info.get("organization", team.organization)
        team.region = team_info.get("region", team.region)
        team.updated_at = datetime.utcnow()
        session.add(team)
        session.commit()
        session.refresh(team)
        print(f"✓ Updated team info: {team.team_name} - {team.organization}, {team.region}")
    
    # Check if we're using mock data
    is_mock = len(matches_data) > 0 and all(
        m.get('event_id', '').startswith('DEMO') or m.get('event_name', '').startswith('Mock')
        for m in matches_data
    )
    
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
        "total_matches": len(matches_data),
        "mock_data": is_mock
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
            # Frontend expects these field names:
            "avg_score_for": 0.0,
            "avg_score_against": 0.0,
            "max_score_for": 0,
            "min_score_for": 0,
            # Also keep legacy names for compatibility:
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
        # Frontend expects these field names:
        "avg_score_for": total_score / len(matches) if matches else 0.0,
        "avg_score_against": total_conceded / len(matches) if matches else 0.0,
        "max_score_for": max(scores) if scores else 0,
        "min_score_for": min(scores) if scores else 0,
        # Also keep legacy names for compatibility:
        "avg_score": total_score / len(matches) if matches else 0.0,
        "avg_conceded": total_conceded / len(matches) if matches else 0.0,
        "total_points": total_score,
        "highest_score": max(scores) if scores else 0,
        "lowest_score": min(scores) if scores else 0
    }
