from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class RobotBase(str, Enum):
    SBOT = "sbot"
    RUIGUAN = "ruiguan"
    CBOT = "cbot"


class Playstyle(str, Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    BALANCED = "balanced"


class SpeedPreference(str, Enum):
    SLOW = "slow"
    MEDIUM = "medium"
    FAST = "fast"


class MatchResult(str, Enum):
    WIN = "win"
    LOSS = "loss"
    TIE = "tie"


class Team(SQLModel, table=True):
    __tablename__ = "teams"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    team_number: str = Field(index=True, unique=True)
    team_name: str
    organization: Optional[str] = None
    region: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    robots: List["Robot"] = Relationship(back_populates="team")
    drivers: List["Driver"] = Relationship(back_populates="team")
    matches: List["Match"] = Relationship(back_populates="team")


class Robot(SQLModel, table=True):
    __tablename__ = "robots"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="teams.id")
    robot_base: str  # sbot, ruiguan, cbot
    foldable: bool = False
    drivetrain: str
    tire_count: int
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    team: Optional[Team] = Relationship(back_populates="robots")


class Driver(SQLModel, table=True):
    __tablename__ = "drivers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="teams.id")
    driver_name: str
    playstyle: str  # aggressive, defensive, balanced
    likes_claw: bool = False
    control_agility: int = Field(ge=1, le=10)  # 1-10
    speed_preference: str  # slow, medium, fast
    tire_count: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    team: Optional[Team] = Relationship(back_populates="drivers")


class Match(SQLModel, table=True):
    __tablename__ = "matches"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="teams.id")
    match_id: str = Field(index=True)
    event_id: str = Field(index=True)
    event_name: Optional[str] = None
    match_date: Optional[datetime] = None
    alliance: str  # red or blue
    score_for: int
    score_against: int
    result: str  # win, loss, tie
    opponents: Optional[str] = None  # JSON string or comma-separated
    rank_snapshot: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    team: Optional[Team] = Relationship(back_populates="matches")


class PathRecord(SQLModel, table=True):
    __tablename__ = "path_records"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="teams.id")
    match_id: Optional[int] = Field(default=None, foreign_key="matches.id")
    path_name: str
    method: str  # polyline, bezier, spline, astar, heatline
    points_json: str  # JSON string of points
    style_json: Optional[str] = None  # JSON string of style config
    image_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
