"""
详细的 RobotEvents API 诊断工具
"""

import httpx
import asyncio
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings


async def detailed_api_test():
    """详细测试 RobotEvents API"""
    
    print("=" * 70)
    print("🔍 RobotEvents API 详细诊断")
    print("=" * 70)
    
    api_key = settings.ROBOTEVENTS_API_KEY
    if not api_key or api_key.strip() == "":
        print("❌ 错误: 未配置 API Key")
        return
    
    print(f"\n✓ API Key: {api_key[:30]}...")
    print(f"  长度: {len(api_key)} 字符")
    
    # 测试 1: 基础连接测试
    print("\n" + "=" * 70)
    print("测试 1: 基础 API 连接")
    print("=" * 70)
    
    base_url = "https://www.robotevents.com/api/v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 测试基础连接
            print(f"\n📡 测试基础端点: {base_url}/seasons")
            response = await client.get(f"{base_url}/seasons", headers=headers)
            print(f"   状态: {response.status_code}")
            
            if response.status_code == 200:
                seasons = response.json()
                print(f"   ✓ API 连接成功")
                print(f"   可用赛季数: {len(seasons.get('data', []))}")
                if seasons.get('data'):
                    latest = seasons['data'][0]
                    print(f"   最新赛季: {latest.get('name')} (ID: {latest.get('id')})")
            elif response.status_code == 401:
                print(f"   ❌ API Key 无效或过期")
                print(f"   响应: {response.text}")
                return
            else:
                print(f"   ⚠️  非预期状态: {response.text}")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return
    
    # 测试 2: 搜索队伍（多种方式）
    print("\n" + "=" * 70)
    print("测试 2: 队伍搜索 - 多种参数组合")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "基础搜索（当前代码）",
            "params": {
                "number": "229V",
                "program": "V5RC"
            }
        },
        {
            "name": "添加 myTeams 参数",
            "params": {
                "number": "229V",
                "program": "V5RC",
                "myTeams": "false"
            }
        },
        {
            "name": "使用 number[0] 部分匹配",
            "params": {
                "number[0]": "229",
                "program": "V5RC"
            }
        },
        {
            "name": "不限制 program",
            "params": {
                "number": "229V"
            }
        },
        {
            "name": "使用 per_page",
            "params": {
                "number": "229V",
                "program": "V5RC",
                "per_page": 50
            }
        }
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i, test in enumerate(test_cases, 1):
            print(f"\n测试 2.{i}: {test['name']}")
            print(f"   参数: {test['params']}")
            
            try:
                response = await client.get(
                    f"{base_url}/teams",
                    params=test['params'],
                    headers=headers
                )
                
                print(f"   状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    teams = data.get("data", [])
                    print(f"   找到队伍数: {len(teams)}")
                    
                    # 打印分页信息
                    meta = data.get("meta", {})
                    if meta:
                        print(f"   分页: 当前页 {meta.get('current_page')}/{meta.get('last_page')}")
                        print(f"   总数: {meta.get('total')} 个队伍")
                    
                    # 打印前几个队伍
                    for team in teams[:3]:
                        print(f"      • {team.get('number')} - {team.get('team_name')}")
                    
                    if teams:
                        print(f"   ✓ 找到队伍!")
                        # 打印第一个队伍的完整信息
                        print(f"\n   📋 第一个队伍详细信息:")
                        print(json.dumps(teams[0], indent=6, ensure_ascii=False)[:800])
                        break  # 找到就停止
                else:
                    print(f"   ❌ 错误: {response.text[:200]}")
                    
            except Exception as e:
                print(f"   ❌ 异常: {e}")
            
            await asyncio.sleep(0.5)  # 避免请求过快
    
    # 测试 3: 检查 API 限制
    print("\n" + "=" * 70)
    print("测试 3: API 使用限制")
    print("=" * 70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{base_url}/teams", params={"per_page": 1}, headers=headers)
        
        # 检查响应头中的限制信息
        rate_limit = response.headers.get("X-RateLimit-Limit")
        rate_remaining = response.headers.get("X-RateLimit-Remaining")
        
        if rate_limit:
            print(f"   请求限制: {rate_remaining}/{rate_limit}")
        else:
            print(f"   未找到限制信息")
        
        print(f"   响应头:")
        for key in ["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]:
            if key in response.headers:
                print(f"      {key}: {response.headers[key]}")
    
    # 测试 4: 测试已知的国际队伍
    print("\n" + "=" * 70)
    print("测试 4: 测试国际知名队伍")
    print("=" * 70)
    
    international_teams = ["62A", "169A", "7K", "1961Z"]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for team_num in international_teams:
            print(f"\n   测试: {team_num}")
            response = await client.get(
                f"{base_url}/teams",
                params={"number": team_num, "program": "V5RC"},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                teams = data.get("data", [])
                if teams:
                    print(f"      ✓ 找到: {teams[0].get('team_name')}")
                else:
                    print(f"      ✗ 未找到")
            else:
                print(f"      ✗ 错误: {response.status_code}")
            
            await asyncio.sleep(0.3)


async def test_programs():
    """测试不同的 program 参数"""
    
    print("\n" + "=" * 70)
    print("测试 5: 尝试不同的 program 值")
    print("=" * 70)
    
    api_key = settings.ROBOTEVENTS_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    programs = [
        ("V5RC", "VEX V5 Robotics Competition"),
        ("VEXU", "VEX U"),
        ("VIQC", "VEX IQ Challenge"),
        ("VAIRC", "VEX AI Robotics Competition"),
        ("V5", "V5 (简写)"),
        (None, "不指定 program")
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for program, description in programs:
            params = {"number": "229V"}
            if program:
                params["program"] = program
            
            print(f"\n   Program: {program or '(无)'} - {description}")
            print(f"   参数: {params}")
            
            try:
                response = await client.get(
                    "https://www.robotevents.com/api/v2/teams",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    teams = data.get("data", [])
                    print(f"   结果: 找到 {len(teams)} 个队伍")
                    if teams:
                        print(f"   ✓ 成功! 队伍: {teams[0].get('team_name')}")
                else:
                    print(f"   错误: {response.status_code}")
                    
            except Exception as e:
                print(f"   异常: {e}")
            
            await asyncio.sleep(0.3)


async def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("🤖 RobotEvents API 完整诊断报告")
    print("=" * 70)
    
    await detailed_api_test()
    await test_programs()
    
    print("\n" + "=" * 70)
    print("诊断完成")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
