"""
RobotEvents API 队伍测试工具
用于验证队伍编号是否存在于 RobotEvents 数据库中
"""

import httpx
import asyncio
import sys
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings


async def test_team(team_number: str):
    """测试指定的队伍编号"""
    
    print("=" * 60)
    print(f"🔍 测试队伍: {team_number}")
    print("=" * 60)
    
    # 检查 API Key
    api_key = settings.ROBOTEVENTS_API_KEY
    if not api_key or api_key.strip() == "":
        print("❌ 错误: 未配置 API Key")
        print("   请在 .env 文件中设置 ROBOTEVENTS_API_KEY")
        return
    
    print(f"✓ API Key 已配置: {api_key[:20]}...")
    
    # 准备请求
    url = "https://www.robotevents.com/api/v2/teams"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    # 不使用 program 参数，API 在使用该参数时返回空结果
    params = {
        "number": team_number
    }
    
    print(f"\n📡 发送请求到: {url}")
    print(f"   参数: {params}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params, headers=headers)
            
            print(f"\n📊 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # 打印完整的响应数据用于调试
                print(f"\n📋 完整 API 响应:")
                import json
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                
                teams = data.get("data", [])
                
                if teams:
                    print(f"\n✅ 找到 {len(teams)} 个队伍:")
                    for i, team in enumerate(teams, 1):
                        print(f"\n队伍 {i}:")
                        print(f"   ID: {team.get('id')}")
                        print(f"   编号: {team.get('number')}")
                        print(f"   名称: {team.get('team_name')}")
                        print(f"   机器人: {team.get('robot_name')}")
                        print(f"   组织: {team.get('organization')}")
                        
                        loc = team.get('location', {})
                        print(f"   位置: {loc.get('city')}, {loc.get('region')}, {loc.get('country')}")
                else:
                    print(f"\n❌ 队伍 '{team_number}' 在 RobotEvents 数据库中不存在")
                    print("\n💡 建议:")
                    print("   1. 检查队伍编号拼写（区分大小写）")
                    print("   2. 确认队伍已在 RobotEvents 注册")
                    print("   3. 访问 https://www.robotevents.com/teams/V5RC 搜索队伍")
                    print("   4. 尝试搜索其他已知队伍验证 API 是否正常")
                    
            elif response.status_code == 401:
                print("\n❌ 认证失败: API Key 无效")
                print("   请检查 API Key 是否正确")
            elif response.status_code == 403:
                print("\n❌ 权限不足: API Key 没有访问权限")
                print("   请确认 API Key 有效且有正确的权限")
            else:
                print(f"\n❌ 请求失败: {response.status_code}")
                print(f"   响应: {response.text}")
                
    except httpx.TimeoutException:
        print("\n❌ 请求超时: 无法连接到 RobotEvents API")
        print("   请检查网络连接")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print(f"   类型: {type(e).__name__}")


async def test_multiple_teams():
    """测试多个队伍（包括已知存在的队伍）"""
    
    test_teams = [
        ("229V", "深圳中学 - 已知存在"),
        ("315X", "历史悠久队伍 - 已知存在"),
        ("62A", "QUEENS - 已知存在"),
        ("16610A", "目标队伍的变体"),
        ("16610B", "目标队伍"),
        ("16610", "不带字母后缀"),
    ]
    
    print("\n" + "=" * 60)
    print("🧪 批量测试队伍编号")
    print("=" * 60)
    
    for team_number, description in test_teams:
        print(f"\n\n{'='*60}")
        print(f"测试: {team_number} ({description})")
        print("=" * 60)
        await test_team(team_number)
        await asyncio.sleep(1)  # 避免请求过快


async def search_by_prefix(prefix: str):
    """按前缀搜索队伍"""
    
    print("=" * 60)
    print(f"🔍 搜索前缀: {prefix}*")
    print("=" * 60)
    
    api_key = settings.ROBOTEVENTS_API_KEY
    if not api_key or api_key.strip() == "":
        print("❌ 错误: 未配置 API Key")
        return
    
    url = "https://www.robotevents.com/api/v2/teams"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    # 不使用 program 参数
    params = {
        "number[0]": prefix,  # 部分匹配
        "per_page": 10  # 限制结果数量
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                teams = data.get("data", [])
                
                if teams:
                    print(f"\n✅ 找到 {len(teams)} 个以 '{prefix}' 开头的队伍:")
                    for team in teams:
                        print(f"   • {team.get('number')} - {team.get('team_name')}")
                else:
                    print(f"\n❌ 没有找到以 '{prefix}' 开头的队伍")
            else:
                print(f"\n❌ 搜索失败: {response.status_code}")
                
    except Exception as e:
        print(f"\n❌ 错误: {e}")


async def main():
    """主函数"""
    
    print("\n" + "=" * 60)
    print("🤖 RobotEvents API 队伍测试工具")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # 从命令行参数获取队伍编号
        team_number = sys.argv[1]
        
        if team_number.startswith("--prefix="):
            # 前缀搜索
            prefix = team_number.replace("--prefix=", "")
            await search_by_prefix(prefix)
        elif team_number == "--batch":
            # 批量测试
            await test_multiple_teams()
        else:
            # 单个队伍测试
            await test_team(team_number)
    else:
        # 没有参数，显示使用说明
        print("\n使用方法:")
        print("  python test_team.py <队伍编号>        # 测试单个队伍")
        print("  python test_team.py --batch          # 批量测试多个队伍")
        print("  python test_team.py --prefix=16610   # 搜索指定前缀的所有队伍")
        print("\n示例:")
        print("  python test_team.py 229V")
        print("  python test_team.py 16610B")
        print("  python test_team.py --prefix=16610")
        print("  python test_team.py --batch")
        print("\n")
        
        # 默认测试 16610B
        print("未指定队伍编号，将测试 16610B...")
        await test_team("16610B")


if __name__ == "__main__":
    asyncio.run(main())
