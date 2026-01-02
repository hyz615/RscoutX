"""
测试比赛数据 API 端点
"""

import httpx
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings


async def test_team_matches(team_number: str):
    """测试获取队伍的比赛数据"""
    
    print("=" * 70)
    print(f"🔍 测试队伍: {team_number}")
    print("=" * 70)
    
    api_key = settings.ROBOTEVENTS_API_KEY
    if not api_key or api_key.strip() == "":
        print("❌ 未配置 API Key")
        return
    
    print(f"✓ API Key: {api_key[:30]}...\n")
    
    base_url = "https://www.robotevents.com/api/v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: 搜索队伍
        print("Step 1: 搜索队伍")
        team_response = await client.get(
            f"{base_url}/teams",
            params={"number": team_number},
            headers=headers
        )
        
        print(f"  状态: {team_response.status_code}")
        
        if team_response.status_code != 200:
            print(f"  ❌ 失败: {team_response.text}")
            return
        
        teams_data = team_response.json()
        teams = teams_data.get("data", [])
        
        if not teams:
            print(f"  ❌ 未找到队伍 {team_number}")
            return
        
        team = teams[0]
        team_id = team["id"]
        team_name = team.get("team_name", "Unknown")
        
        print(f"  ✓ 找到: {team_name} (ID: {team_id})")
        print(f"  组织: {team.get('organization', 'N/A')}")
        print(f"  地区: {team.get('location', {}).get('city', 'N/A')}, {team.get('location', {}).get('region', 'N/A')}")
        
        # Step 2: 获取比赛记录
        print(f"\nStep 2: 获取比赛记录 (2025-2026 赛季)")
        matches_response = await client.get(
            f"{base_url}/teams/{team_id}/matches",
            params={
                "season[]": "197",  # 2025-2026 Push Back
                "per_page": 250
            },
            headers=headers
        )
        
        print(f"  状态: {matches_response.status_code}")
        
        if matches_response.status_code != 200:
            print(f"  ❌ 失败: {matches_response.text[:200]}")
            return
        
        matches_data = matches_response.json()
        matches = matches_data.get("data", [])
        
        print(f"  ✓ 找到 {len(matches)} 场比赛")
        
        if matches:
            print(f"\n📋 前 5 场比赛:")
            for i, match in enumerate(matches[:5], 1):
                event = match.get("event", {})
                print(f"\n  比赛 {i}:")
                print(f"    赛事: {event.get('name', 'Unknown')}")
                print(f"    名称: {match.get('name', 'Unknown')}")
                print(f"    时间: {match.get('started', 'Unknown')}")
                
                # 显示联盟信息
                alliances = match.get("alliances", [])
                if alliances and len(alliances) >= 2:
                    red = alliances[0]
                    blue = alliances[1]
                    print(f"    红方: {red.get('score', 0)} 分")
                    print(f"    蓝方: {blue.get('score', 0)} 分")
        
        # Step 3: 测试事件筛选
        print(f"\n\nStep 3: 获取最近赛事列表")
        events_response = await client.get(
            f"{base_url}/teams/{team_id}/events",
            params={"per_page": 5},
            headers=headers
        )
        
        if events_response.status_code == 200:
            events_data = events_response.json()
            events = events_data.get("data", [])
            print(f"  ✓ 找到 {len(events)} 个最近赛事")
            
            for i, event in enumerate(events[:3], 1):
                print(f"    {i}. {event.get('name')} ({event.get('start')})")


async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python test_matches.py <队伍编号>")
        print("示例: python test_matches.py 16610A")
        return
    
    team_number = sys.argv[1]
    await test_team_matches(team_number)


if __name__ == "__main__":
    asyncio.run(main())
