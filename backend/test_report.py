import asyncio
import sys
sys.path.insert(0, '.')

from sqlmodel import Session
from app.db.session import engine
from app.services.llm.report_generator import generate_team_report

async def test_report():
    try:
        print("Testing report generation with custom_context...")
        
        with Session(engine) as session:
            result = await generate_team_report(
                session=session,
                team_id=1,  # Assuming team 1 exists
                event_id=None,
                include_map=True,
                include_driver=True,
                include_robot=True,
                language="zh",
                custom_context="机器人类型: sbot\n是否有机翼: 是\n驾驶员习惯标签: 进攻, 防守"
            )
            
            print(f"Success: {result['success']}")
            if not result['success']:
                print(f"Error message: {result.get('message')}")
            else:
                print(f"Report generated! Length: {len(result.get('report_markdown', ''))}")
                
            return result['success']
            
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_report())
    sys.exit(0 if success else 1)
