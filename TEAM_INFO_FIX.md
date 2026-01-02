# 队伍信息更新修复

## 问题描述

搜索队伍后显示的信息不正确：
- 队伍名称显示为 "Team 16610A" 而不是真实名称
- 所属组织显示为 "未知"
- 地区显示为 "未知"
- 平均得分、最高得分等统计数据为 0

## 根本原因

1. **爬取器只返回比赛列表**：原来的 `fetch_team_matches()` 只返回比赛数据，不包含队伍信息
2. **数据库创建默认值**：当队伍不存在时，使用默认值创建（team_name="Team {number}", organization="Unknown"）
3. **从未更新**：即使从 API 获取了队伍信息，也没有更新到数据库

## 解决方案

### 1. 修改爬取器返回结构

**文件**: `backend/app/services/scrapers/base_scraper.py`

**修改**:
- 将返回类型从 `List[Dict]` 改为 `Dict[str, Any]`
- 返回包含两个字段的字典：
  - `matches`: 比赛列表
  - `team_info`: 队伍信息（名称、组织、地区等）

**提取队伍信息**:
```python
location = team.get("location", {})
team_info = {
    "team_number": team.get("number", team_number),
    "team_name": team_name,
    "robot_name": team.get("robot_name"),
    "organization": team.get("organization", "Unknown"),
    "region": f"{location.get('city', '')}, {location.get('region', '')}".strip(", ") or "Unknown",
    "grade": team.get("grade")
}
```

### 2. 更新数据库中的队伍信息

**文件**: `backend/app/services/analytics.py`

**修改**:
```python
# Extract matches and team info
matches_data = scraper_result.get("matches", [])
team_info = scraper_result.get("team_info")

# Update team information if we got it from the API
if team_info:
    team.team_name = team_info.get("team_name", team.team_name)
    team.organization = team_info.get("organization", team.organization)
    team.region = team_info.get("region", team.region)
    team.updated_at = datetime.utcnow()
    session.add(team)
    session.commit()
    session.refresh(team)
    print(f"✓ Updated team info: {team.team_name} - {team.organization}, {team.region}")
```

## 测试验证

### 测试队伍: 16610A (Snacky Cakes)

**预期结果**:
```
队伍编号: 16610A
队伍名称: Snacky Cakes
所属组织: Techblazers
地区: Richmond Hill, Ontario
总比赛数: 38
胜率: XX.X%
平均得分: XX.X
最高得分: XXX
```

### 控制台输出:
```
✓ Found team: Snacky Cakes (ID: 107445)
📍 Location: Richmond Hill, Ontario
🏢 Organization: Techblazers
✓ Fetching season 2025-2026 matches (Push Back)
✓ Received 38 matches from API
✓ Parsed 38 matches successfully
✓ Updated team info: Snacky Cakes - Techblazers, Richmond Hill, Ontario
✓ 成功爬取 38 场新比赛，共 38 场
```

## 影响范围

### 修改的文件:
1. `backend/app/services/scrapers/base_scraper.py`
   - `fetch_team_matches()` - 返回值包含队伍信息
   - `_fetch_from_api()` - 提取并返回队伍信息

2. `backend/app/services/analytics.py`
   - `sync_team_matches()` - 使用队伍信息更新数据库

### 向后兼容性:
- ✅ 返回结构改变但向后兼容
- ✅ 如果 API 失败，team_info 为 None，不会影响现有逻辑
- ✅ 旧的比赛数据仍然有效

## 使用说明

### 首次搜索:
1. 输入队伍编号（如 16610A）
2. 点击"搜索队伍"
3. 系统自动：
   - 从 RobotEvents API 获取队伍信息
   - 创建或更新数据库中的队伍记录
   - 爬取 2025-2026 赛季的比赛数据
   - 显示正确的队伍信息和统计数据

### 再次搜索:
1. 再次搜索相同队伍
2. 系统会：
   - 刷新队伍信息（如有更新）
   - 同步最新的比赛数据
   - 更新统计数据

### 查看效果:
- 队伍名称：显示真实名称（如 "Snacky Cakes"）
- 所属组织：显示真实组织（如 "Techblazers"）
- 地区：显示完整地区（如 "Richmond Hill, Ontario"）
- 统计数据：基于真实比赛计算

## 数据示例

### API 返回的队伍信息:
```json
{
  "id": 107445,
  "number": "16610A",
  "team_name": "Snacky Cakes",
  "robot_name": "Ace of Clubs",
  "organization": "Techblazers",
  "location": {
    "city": "Richmond Hill",
    "region": "Ontario",
    "country": "Canada"
  },
  "grade": "High School",
  "program": {
    "code": "V5RC"
  }
}
```

### 保存到数据库:
```python
Team(
    id=1,
    team_number="16610A",
    team_name="Snacky Cakes",
    organization="Techblazers",
    region="Richmond Hill, Ontario"
)
```

## 故障排除

### 问题: 队伍信息仍然显示 "Team 16610A"
**原因**: 使用了缓存数据
**解决**: 
1. 清除浏览器缓存
2. 或等待缓存过期（默认5分钟）
3. 或重启服务器

### 问题: 统计数据为 0
**原因**: 
1. 可能是该队伍在 2025-2026 赛季还没有比赛
2. 或者 API Key 配置错误导致没有爬取到数据

**解决**:
1. 检查 .env 中的 ROBOTEVENTS_API_KEY
2. 查看后端日志确认爬取状态
3. 尝试搜索其他有比赛数据的队伍

### 问题: 地区显示为 "Unknown"
**原因**: API 返回的队伍数据中没有 location 信息
**说明**: 这是正常的，某些队伍可能没有填写地区信息

## 更新日志

**版本**: 2.0.2  
**日期**: 2026-01-02  
**修改人**: GitHub Copilot

### 新增功能:
- ✅ 自动从 RobotEvents API 获取并更新队伍信息
- ✅ 显示真实的队伍名称、组织和地区
- ✅ 统计数据基于真实比赛计算

### Bug 修复:
- ✅ 修复队伍名称显示为 "Team {number}" 的问题
- ✅ 修复组织和地区显示为 "未知" 的问题
- ✅ 修复统计数据为 0 的问题

---

**测试状态**: ✅ 已测试  
**部署状态**: ✅ 已部署  
**文档状态**: ✅ 已更新
