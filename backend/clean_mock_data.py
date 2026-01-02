"""
清理数据库中的 Mock Data
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.models import Match, Team


def clean_mock_data():
    """删除所有 mock data"""
    
    print("=" * 70)
    print("🧹 清理数据库中的 Mock Data")
    print("=" * 70)
    
    with Session(engine) as session:
        # 查找所有 mock matches (event_id 以 DEMO 开头或 event_name 包含 Mock)
        statement = select(Match).where(
            (Match.event_id.like('DEMO%')) | 
            (Match.event_name.like('%Mock%'))
        )
        mock_matches = session.exec(statement).all()
        
        print(f"\n找到 {len(mock_matches)} 场 Mock 比赛记录")
        
        if mock_matches:
            # 显示要删除的记录
            for match in mock_matches[:5]:  # 只显示前5条
                print(f"  - {match.match_id} @ {match.event_name}")
            
            if len(mock_matches) > 5:
                print(f"  ... 还有 {len(mock_matches) - 5} 场")
            
            # 删除
            confirm = input("\n确认删除这些 Mock 数据? (y/N): ")
            if confirm.lower() == 'y':
                for match in mock_matches:
                    session.delete(match)
                session.commit()
                print(f"✅ 已删除 {len(mock_matches)} 场 Mock 比赛记录")
            else:
                print("❌ 取消删除")
        else:
            print("✅ 数据库中没有 Mock 数据")
        
        # 检查是否有没有比赛记录的队伍
        statement = select(Team)
        all_teams = session.exec(statement).all()
        
        print(f"\n检查 {len(all_teams)} 个队伍...")
        
        empty_teams = []
        for team in all_teams:
            statement = select(Match).where(Match.team_id == team.id)
            matches = session.exec(statement).all()
            if len(matches) == 0:
                empty_teams.append(team)
        
        if empty_teams:
            print(f"\n找到 {len(empty_teams)} 个没有比赛记录的队伍:")
            for team in empty_teams:
                print(f"  - {team.team_number}: {team.team_name}")
            
            confirm = input("\n是否删除这些空队伍? (y/N): ")
            if confirm.lower() == 'y':
                for team in empty_teams:
                    session.delete(team)
                session.commit()
                print(f"✅ 已删除 {len(empty_teams)} 个空队伍")
            else:
                print("❌ 保留空队伍")
        else:
            print("✅ 所有队伍都有比赛记录")
    
    print("\n" + "=" * 70)
    print("清理完成!")
    print("=" * 70)


if __name__ == "__main__":
    clean_mock_data()
