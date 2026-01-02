"""
Seed data script for RscoutX
Creates sample teams, robots, drivers, and matches for testing
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import Session
from app.db.session import engine, init_db
from app.models.models import Team, Robot, Driver, Match


def seed_database():
    """Seed database with sample data"""
    
    # Initialize database
    init_db()
    
    with Session(engine) as session:
        # Check if data already exists
        existing_team = session.query(Team).first()
        if existing_team:
            print("Database already contains data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create Team 1: Dragon Robotics
        team1 = Team(
            team_number="1234A",
            team_name="Dragon Robotics",
            organization="Dragon High School",
            region="China - Guangdong"
        )
        session.add(team1)
        session.commit()
        session.refresh(team1)
        
        # Create Team 2: Phoenix Alliance
        team2 = Team(
            team_number="5678B",
            team_name="Phoenix Alliance",
            organization="Phoenix Academy",
            region="China - Shanghai"
        )
        session.add(team2)
        session.commit()
        session.refresh(team2)
        
        print(f"✓ Created teams: {team1.team_number}, {team2.team_number}")
        
        # Create Robot for Team 1
        robot1 = Robot(
            team_id=team1.id,
            robot_base="sbot",
            foldable=True,
            drivetrain="4-motor X-drive",
            tire_count=4,
            notes="High-speed design with omni wheels. Foldable intake mechanism."
        )
        session.add(robot1)
        
        # Create Robot for Team 2
        robot2 = Robot(
            team_id=team2.id,
            robot_base="ruiguan",
            foldable=False,
            drivetrain="6-motor tank",
            tire_count=6,
            notes="Heavy-duty design. Excellent pushing power."
        )
        session.add(robot2)
        session.commit()
        
        print(f"✓ Created robots for both teams")
        
        # Create Driver for Team 1
        driver1 = Driver(
            team_id=team1.id,
            driver_name="Alex Chen",
            playstyle="aggressive",
            likes_claw=True,
            control_agility=9,
            speed_preference="fast",
            tire_count=4,
            notes="Experienced driver with 2 years competition history. Excellent at autonomous."
        )
        session.add(driver1)
        
        # Create Driver for Team 2
        driver2 = Driver(
            team_id=team2.id,
            driver_name="Emma Wang",
            playstyle="balanced",
            likes_claw=False,
            control_agility=7,
            speed_preference="medium",
            tire_count=6,
            notes="Strategic player. Focus on defense and positioning."
        )
        session.add(driver2)
        session.commit()
        
        print(f"✓ Created drivers for both teams")
        
        # Create Matches for Team 1
        base_date = datetime.utcnow() - timedelta(days=7)
        
        matches_team1 = [
            Match(
                team_id=team1.id,
                match_id="Q1",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date,
                alliance="red",
                score_for=85,
                score_against=72,
                result="win",
                opponents="5678B, 9999C",
                rank_snapshot=1
            ),
            Match(
                team_id=team1.id,
                match_id="Q2",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date + timedelta(hours=2),
                alliance="blue",
                score_for=92,
                score_against=78,
                result="win",
                opponents="3333D, 4444E",
                rank_snapshot=1
            ),
            Match(
                team_id=team1.id,
                match_id="Q3",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date + timedelta(hours=4),
                alliance="red",
                score_for=68,
                score_against=88,
                result="loss",
                opponents="5678B, 7777F",
                rank_snapshot=2
            ),
            Match(
                team_id=team1.id,
                match_id="Q4",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date + timedelta(hours=6),
                alliance="blue",
                score_for=95,
                score_against=71,
                result="win",
                opponents="2222G, 6666H",
                rank_snapshot=1
            ),
            Match(
                team_id=team1.id,
                match_id="SF1",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date + timedelta(days=1),
                alliance="red",
                score_for=102,
                score_against=89,
                result="win",
                opponents="5678B, 8888I",
                rank_snapshot=1
            )
        ]
        
        for match in matches_team1:
            session.add(match)
        
        # Create Matches for Team 2
        matches_team2 = [
            Match(
                team_id=team2.id,
                match_id="Q1",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date,
                alliance="blue",
                score_for=72,
                score_against=85,
                result="loss",
                opponents="1234A, 9999J",
                rank_snapshot=4
            ),
            Match(
                team_id=team2.id,
                match_id="Q2",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date + timedelta(hours=2),
                alliance="red",
                score_for=81,
                score_against=75,
                result="win",
                opponents="3333K, 4444L",
                rank_snapshot=3
            ),
            Match(
                team_id=team2.id,
                match_id="Q3",
                event_id="RE-VRC-24-1234",
                event_name="VEX Regional Championship 2024",
                match_date=base_date + timedelta(hours=4),
                alliance="blue",
                score_for=88,
                score_against=68,
                result="win",
                opponents="1234A, 7777M",
                rank_snapshot=2
            )
        ]
        
        for match in matches_team2:
            session.add(match)
        
        session.commit()
        
        print(f"✓ Created {len(matches_team1)} matches for Team 1")
        print(f"✓ Created {len(matches_team2)} matches for Team 2")
        
        print("\n" + "="*50)
        print("Database seeding completed successfully!")
        print("="*50)
        print("\nSample Data Summary:")
        print(f"  Teams: 2 ({team1.team_number}, {team2.team_number})")
        print(f"  Robots: 2")
        print(f"  Drivers: 2")
        print(f"  Matches: {len(matches_team1) + len(matches_team2)}")
        print("\nYou can now:")
        print("  1. Start the application: start.bat")
        print("  2. View API docs: http://localhost:8000/api/docs")
        print("  3. Access frontend: http://localhost:3000")
        print("  4. Generate reports for Team ID 1 or 2")


if __name__ == "__main__":
    seed_database()
