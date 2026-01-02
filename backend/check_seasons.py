"""
检查 RobotEvents 可用的赛季
"""

import httpx
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings


async def check_seasons():
    """查看所有可用的赛季"""
    
    print("=" * 70)
    print("🔍 查询 RobotEvents 可用赛季")
    print("=" * 70)
    
    api_key = settings.ROBOTEVENTS_API_KEY
    if not api_key or api_key.strip() == "":
        print("❌ 未配置 API Key")
        return
    
    base_url = "https://www.robotevents.com/api/v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 获取赛季列表
        print(f"\n📡 请求: {base_url}/seasons")
        response = await client.get(f"{base_url}/seasons", headers=headers)
        
        print(f"状态: {response.status_code}\n")
        
        if response.status_code == 200:
            data = response.json()
            seasons = data.get("data", [])
            
            print(f"✓ 找到 {len(seasons)} 个赛季\n")
            print("=" * 70)
            print("最近的赛季:")
            print("=" * 70)
            
            # 只显示最近10个赛季
            for season in seasons[:10]:
                season_id = season.get("id")
                season_name = season.get("name")
                program = season.get("program", {}).get("code", "Unknown")
                start = season.get("start", "Unknown")
                end = season.get("end", "Unknown")
                
                print(f"\nID: {season_id}")
                print(f"名称: {season_name}")
                print(f"项目: {program}")
                print(f"时间: {start} ~ {end}")
            
            # 查找 2025-2026 V5RC 赛季
            print("\n" + "=" * 70)
            print("🔍 查找 2025-2026 VRC 赛季:")
            print("=" * 70)
            
            vrc_2025_seasons = [
                s for s in seasons 
                if "V5RC" in s.get("program", {}).get("code", "")
                and ("2025" in s.get("name", "") or "2026" in s.get("name", ""))
            ]
            
            if vrc_2025_seasons:
                for season in vrc_2025_seasons:
                    print(f"\n✓ 找到: {season.get('name')}")
                    print(f"  ID: {season.get('id')}")
                    print(f"  时间: {season.get('start')} ~ {season.get('end')}")
                    print(f"  使用参数: season[]={season.get('id')}")
            else:
                print("\n⚠️ 未找到 2025-2026 VRC 赛季")
        else:
            print(f"❌ 请求失败: {response.text}")


async def main():
    await check_seasons()


if __name__ == "__main__":
    asyncio.run(main())
