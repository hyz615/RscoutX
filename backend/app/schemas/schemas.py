from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field


# Team Schemas
class TeamBase(BaseModel):
    team_number: str
    team_name: str
    organization: Optional[str] = None
    region: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    team_name: Optional[str] = None
    organization: Optional[str] = None
    region: Optional[str] = None


class TeamRead(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Robot Schemas
class RobotBase(BaseModel):
    robot_base: str  # sbot, ruiguan, cbot
    foldable: bool = False
    drivetrain: str
    tire_count: int
    notes: Optional[str] = None


class RobotCreate(RobotBase):
    team_id: int


class RobotUpdate(BaseModel):
    robot_base: Optional[str] = None
    foldable: Optional[bool] = None
    drivetrain: Optional[str] = None
    tire_count: Optional[int] = None
    notes: Optional[str] = None


class RobotRead(RobotBase):
    id: int
    team_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Driver Schemas
class DriverBase(BaseModel):
    driver_name: str
    playstyle: str  # aggressive, defensive, balanced
    likes_claw: bool = False
    control_agility: int = Field(ge=1, le=10)
    speed_preference: str  # slow, medium, fast
    tire_count: Optional[int] = None
    notes: Optional[str] = None


class DriverCreate(DriverBase):
    team_id: int


class DriverUpdate(BaseModel):
    driver_name: Optional[str] = None
    playstyle: Optional[str] = None
    likes_claw: Optional[bool] = None
    control_agility: Optional[int] = Field(None, ge=1, le=10)
    speed_preference: Optional[str] = None
    tire_count: Optional[int] = None
    notes: Optional[str] = None


class DriverRead(DriverBase):
    id: int
    team_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Match Schemas
class MatchBase(BaseModel):
    match_id: str
    event_id: str
    event_name: Optional[str] = None
    match_date: Optional[datetime] = None
    alliance: str
    score_for: int
    score_against: int
    result: str
    opponents: Optional[str] = None
    rank_snapshot: Optional[int] = None
    notes: Optional[str] = None


class MatchCreate(MatchBase):
    team_id: int


class MatchRead(MatchBase):
    id: int
    team_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Path Rendering Schemas
class RobotState(BaseModel):
    """Robot state at a specific point"""
    state: str  # wingpushing, intaking, releasing, moving, idle
    color: Optional[str] = None  # Auto-assign if not provided
    icon: Optional[str] = None  # Custom icon name


class PathPoint(BaseModel):
    x: float
    y: float
    t: Optional[float] = None  # time or speed
    speed: Optional[float] = None
    robot_state: Optional[RobotState] = None  # Robot state at this point


class PathStyle(BaseModel):
    color: str = "#FF0000"
    width: int = 3
    opacity: float = 0.8
    gradient: Optional[bool] = False
    arrow: Optional[bool] = False
    show_state_labels: bool = True  # Show state text labels
    state_icon_size: int = 20  # Size of state icons


class PathRenderRequest(BaseModel):
    map_filename: Optional[str] = None
    method: str  # polyline, bezier, spline, astar, heatline
    points: List[PathPoint]
    style: Optional[PathStyle] = PathStyle()
    coordinate_system: str = "pixel"  # pixel or field
    obstacles: Optional[List[Any]] = None  # for astar
    return_image: bool = True
    return_overlay: bool = False


class PathRenderResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    image_base64: Optional[str] = None
    overlay_json: Optional[Any] = None


# Report Schemas
class ReportRequest(BaseModel):
    team_id: int
    event_id: Optional[str] = None
    include_map: bool = True
    include_driver: bool = True
    include_robot: bool = True
    language: str = "zh"  # zh or en


class ReportResponse(BaseModel):
    success: bool
    report_markdown: Optional[str] = None
    report_json: Optional[Any] = None
    message: Optional[str] = None
