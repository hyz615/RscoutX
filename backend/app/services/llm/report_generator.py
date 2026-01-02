from typing import Dict, Any, Optional
import json
from sqlmodel import Session, select

from app.models.models import Team, Robot, Driver, Match
from app.services.llm.providers import get_llm_provider
from app.services.analytics import calculate_team_stats
from app.prompts.report_prompts import (
    REPORT_SYSTEM_PROMPT_ZH,
    REPORT_SYSTEM_PROMPT_EN,
    REPORT_PROMPT_TEMPLATE_ZH,
    REPORT_PROMPT_TEMPLATE_EN
)


async def generate_team_report(
    session: Session,
    team_id: int,
    event_id: Optional[str] = None,
    include_map: bool = True,
    include_driver: bool = True,
    include_robot: bool = True,
    language: str = "zh",
    custom_context: Optional[str] = None
) -> Dict[str, Any]:
    """Generate AI-powered team analysis report"""
    
    # Get team
    team = session.get(Team, team_id)
    if not team:
        return {
            "success": False,
            "message": "Team not found"
        }
    
    # Initialize variables
    robots = []
    drivers = []
    
    # If custom_context provided, use it directly (includes robot + driver info)
    if custom_context:
        combined_info = custom_context
    else:
        # Get robot info from database
        robot_info = "无机器人信息" if language == "zh" else "No robot information"
        if include_robot:
            statement = select(Robot).where(Robot.team_id == team_id)
            robots = session.exec(statement).all()
            if robots:
                robot = robots[0]  # Use first robot
                if language == "zh":
                    robot_info = f"""
- 底盘类型: {robot.robot_base}
- 可折叠: {'是' if robot.foldable else '否'}
- 传动系统: {robot.drivetrain}
- 轮子数量: {robot.tire_count}
- 备注: {robot.notes or '无'}
"""
                else:
                    robot_info = f"""
- Robot Base: {robot.robot_base}
- Foldable: {'Yes' if robot.foldable else 'No'}
- Drivetrain: {robot.drivetrain}
- Tire Count: {robot.tire_count}
- Notes: {robot.notes or 'None'}
"""
        
        # Get driver info from database
        driver_info = "无驾驶员信息" if language == "zh" else "No driver information"
        if include_driver:
            statement = select(Driver).where(Driver.team_id == team_id)
            drivers = session.exec(statement).all()
            if drivers:
                driver = drivers[0]  # Use first driver
                if language == "zh":
                    driver_info = f"""
- 姓名: {driver.driver_name}
- 风格: {driver.playstyle}
- 喜欢抓取: {'是' if driver.likes_claw else '否'}
- 控制灵活度: {driver.control_agility}/10
- 速度偏好: {driver.speed_preference}
- 备注: {driver.notes or '无'}
"""
                else:
                    driver_info = f"""
- Name: {driver.driver_name}
- Playstyle: {driver.playstyle}
- Likes Claw: {'Yes' if driver.likes_claw else 'No'}
- Control Agility: {driver.control_agility}/10
- Speed Preference: {driver.speed_preference}
- Notes: {driver.notes or 'None'}
"""
        
        combined_info = f"## 机器人配置\n{robot_info}\n\n## 驾驶员习惯\n{driver_info}" if language == "zh" else f"## Robot Configuration\n{robot_info}\n\n## Driver Habits\n{driver_info}"
    
    # Get match stats
    stats = calculate_team_stats(session, team_id, event_id)
    
    # Get recent matches
    statement = select(Match).where(Match.team_id == team_id)
    if event_id:
        statement = statement.where(Match.event_id == event_id)
    statement = statement.order_by(Match.match_date.desc()).limit(5)
    matches = session.exec(statement).all()
    
    recent_matches_str = ""
    for match in matches:
        if language == "zh":
            recent_matches_str += f"- {match.match_id}: {match.alliance}方联盟, {match.score_for}:{match.score_against}, 结果: {match.result}\n"
        else:
            recent_matches_str += f"- {match.match_id}: {match.alliance} alliance, {match.score_for}:{match.score_against}, result: {match.result}\n"
    
    if not recent_matches_str:
        recent_matches_str = "无比赛记录" if language == "zh" else "No match records"
    
    # Build prompt
    if language == "zh":
        system_prompt = REPORT_SYSTEM_PROMPT_ZH
        prompt_template = REPORT_PROMPT_TEMPLATE_ZH
    else:
        system_prompt = REPORT_SYSTEM_PROMPT_EN
        prompt_template = REPORT_PROMPT_TEMPLATE_EN
    
    prompt = prompt_template.format(
        team_number=team.team_number,
        team_name=team.team_name,
        organization=team.organization or "Unknown",
        region=team.region or "Unknown",
        combined_info=combined_info,
        total_matches=stats['total_matches'],
        win_rate=stats['win_rate'],
        avg_score=stats['avg_score'],
        avg_conceded=stats['avg_conceded'],
        highest_score=stats['highest_score'],
        lowest_score=stats['lowest_score'],
        recent_matches=recent_matches_str
    )
    
    # Generate report using LLM
    try:
        llm = get_llm_provider()
        report_markdown = await llm.generate(prompt, system_prompt)
        
        # Build structured JSON
        report_json = {
            "team": {
                "team_number": team.team_number,
                "team_name": team.team_name,
                "organization": team.organization,
                "region": team.region
            },
            "robot": {
                "robot_base": robots[0].robot_base if (include_robot and robots) else None,
                "foldable": robots[0].foldable if (include_robot and robots) else None,
                "drivetrain": robots[0].drivetrain if (include_robot and robots) else None,
                "tire_count": robots[0].tire_count if (include_robot and robots) else None
            } if include_robot else None,
            "driver": {
                "driver_name": drivers[0].driver_name if (include_driver and drivers) else None,
                "playstyle": drivers[0].playstyle if (include_driver and drivers) else None,
                "control_agility": drivers[0].control_agility if (include_driver and drivers) else None,
                "speed_preference": drivers[0].speed_preference if (include_driver and drivers) else None
            } if include_driver else None,
            "statistics": stats,
            "recent_matches": [
                {
                    "match_id": m.match_id,
                    "alliance": m.alliance,
                    "score_for": m.score_for,
                    "score_against": m.score_against,
                    "result": m.result
                } for m in matches
            ]
        }
        
        return {
            "success": True,
            "report_markdown": report_markdown,
            "report_json": report_json
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to generate report: {str(e)}"
        }
