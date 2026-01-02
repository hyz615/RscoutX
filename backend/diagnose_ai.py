"""
诊断 AI 报告生成问题
"""
import asyncio
import sys
import json
sys.path.insert(0, '.')

from sqlmodel import Session, select
from app.db.session import engine
from app.models.models import Team
from app.services.llm.report_generator import generate_team_report

async def diagnose():
    print("=== RscoutX AI 报告诊断工具 ===\n")
    
    # 1. 检查数据库中的队伍
    print("1. 检查数据库中的队伍...")
    with Session(engine) as session:
        teams = session.exec(select(Team).limit(5)).all()
        if not teams:
            print("   ❌ 数据库中没有队伍数据")
            return False
        print(f"   ✓ 找到 {len(teams)} 个队伍")
        for team in teams[:3]:
            print(f"     - {team.team_number}: {team.team_name}")
    
    # 2. 测试 LLM provider
    print("\n2. 测试 LLM provider...")
    try:
        from app.services.llm.providers import get_llm_provider
        llm = get_llm_provider()
        test_result = await llm.generate("说'测试成功'", "你是助手")
        print(f"   ✓ LLM 工作正常: {test_result[:50]}...")
    except Exception as e:
        print(f"   ❌ LLM 错误: {e}")
        return False
    
    # 3. 测试报告生成（无 custom_context）
    print("\n3. 测试报告生成（从数据库）...")
    try:
        with Session(engine) as session:
            team_id = teams[0].id
            result = await generate_team_report(
                session=session,
                team_id=team_id,
                language="zh"
            )
            if result['success']:
                print(f"   ✓ 报告生成成功（{len(result['report_markdown'])} 字符）")
            else:
                print(f"   ❌ 报告生成失败: {result.get('message')}")
                return False
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. 测试报告生成（带 custom_context）
    print("\n4. 测试报告生成（带 custom_context）...")
    try:
        with Session(engine) as session:
            team_id = teams[0].id
            custom_context = """
机器人类型: sbot
是否有机翼: 是 ✓
驾驶员习惯标签: 进攻, 防守, 最后20秒进攻
驾驶员其他习惯: 擅长快速移动
Auton 数量: 3
总路径点数: 45
历史比赛数: 10
参赛次数: 3
"""
            result = await generate_team_report(
                session=session,
                team_id=team_id,
                language="zh",
                custom_context=custom_context
            )
            if result['success']:
                print(f"   ✓ 报告生成成功（{len(result['report_markdown'])} 字符）")
                print(f"\n   报告预览:")
                print("   " + "-" * 50)
                lines = result['report_markdown'].split('\n')[:10]
                for line in lines:
                    print(f"   {line}")
                print("   " + "-" * 50)
            else:
                print(f"   ❌ 报告生成失败: {result.get('message')}")
                return False
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n=== 所有测试通过 ✓ ===")
    return True

if __name__ == "__main__":
    success = asyncio.run(diagnose())
    sys.exit(0 if success else 1)
