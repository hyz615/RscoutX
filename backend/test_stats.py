"""
测试队伍统计数据 API
"""

import httpx
import asyncio


async def test_team_stats():
    """测试队伍统计数据"""
    
    print("=" * 70)
    print("🔍 测试队伍统计数据 API")
    print("=" * 70)
    
    # 假设已经有队伍 ID 1 (16610A) 在数据库中
    team_id = 1
    
    api_url = f"http://localhost:8000/api/matches/stats/{team_id}"
    
    print(f"\n📡 请求: {api_url}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url)
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                stats = response.json()
                
                print(f"\n✅ 统计数据:")
                print(f"   总比赛数: {stats.get('total_matches', 0)}")
                print(f"   胜场: {stats.get('wins', 0)}")
                print(f"   负场: {stats.get('losses', 0)}")
                print(f"   平局: {stats.get('ties', 0)}")
                print(f"   胜率: {stats.get('win_rate', 0) * 100:.1f}%")
                print(f"\n📊 得分统计:")
                print(f"   平均得分 (avg_score_for): {stats.get('avg_score_for', 0):.1f}")
                print(f"   平均失分 (avg_score_against): {stats.get('avg_score_against', 0):.1f}")
                print(f"   最高得分 (max_score_for): {stats.get('max_score_for', 0)}")
                print(f"   最低得分 (min_score_for): {stats.get('min_score_for', 0)}")
                print(f"\n🔍 字段检查:")
                print(f"   是否包含 avg_score_for: {'✓' if 'avg_score_for' in stats else '✗'}")
                print(f"   是否包含 max_score_for: {'✓' if 'max_score_for' in stats else '✗'}")
                
                # 检查是否有数据
                if stats.get('total_matches', 0) == 0:
                    print(f"\n⚠️  警告: 队伍没有比赛记录")
                    print(f"   请先搜索队伍以爬取数据")
                elif stats.get('avg_score_for', 0) == 0:
                    print(f"\n⚠️  警告: 平均得分为 0")
                    print(f"   可能是字段名不匹配或数据计算错误")
                else:
                    print(f"\n✅ 数据正常!")
                    
            else:
                print(f"❌ 请求失败: {response.text}")
                
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 70)


async def test_matches_list():
    """测试比赛列表"""
    
    print("\n🔍 测试比赛列表 API")
    print("=" * 70)
    
    team_id = 1
    api_url = f"http://localhost:8000/api/matches/?team_id={team_id}"
    
    print(f"\n📡 请求: {api_url}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url)
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                matches = response.json()
                
                print(f"\n✅ 找到 {len(matches)} 场比赛")
                
                if matches:
                    # 显示前3场比赛
                    print(f"\n前 3 场比赛:")
                    for i, match in enumerate(matches[:3], 1):
                        print(f"\n   比赛 {i}:")
                        print(f"      比赛ID: {match.get('match_id')}")
                        print(f"      赛事: {match.get('event_name')}")
                        print(f"      联盟: {match.get('alliance')}")
                        print(f"      得分: {match.get('score_for')}")
                        print(f"      失分: {match.get('score_against')}")
                        print(f"      结果: {match.get('result')}")
                else:
                    print(f"\n⚠️  没有比赛记录")
                    
            else:
                print(f"❌ 请求失败: {response.text}")
                
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    print("\n" + "=" * 70)


async def main():
    """主函数"""
    await test_team_stats()
    await test_matches_list()


if __name__ == "__main__":
    asyncio.run(main())
