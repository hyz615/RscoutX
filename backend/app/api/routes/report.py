from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.schemas import ReportRequest, ReportResponse
from app.services.llm.report_generator import generate_team_report

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportRequest,
    session: Session = Depends(get_session)
):
    """Generate AI-powered team analysis report"""
    try:
        result = await generate_team_report(
            session=session,
            team_id=request.team_id,
            event_id=request.event_id,
            include_map=request.include_map,
            include_driver=request.include_driver,
            include_robot=request.include_robot,
            language=request.language,
            custom_context=request.custom_context
        )
        
        return ReportResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
