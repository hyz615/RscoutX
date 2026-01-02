# 🔄 比赛记录爬取功能修复

## ❌ 问题描述

搜索队伍时，系统无法爬取比赛记录，只显示空白或旧数据。

---

## 🔍 问题原因

1. **前端未调用爬虫 API**
   - 搜索队伍时只从数据库读取数据
   - 没有触发从 RobotEvents 爬取新数据

2. **event_id="ALL" 未正确处理**
   - 后端需要特殊处理 "ALL" 来获取所有赛事数据

3. **字段名不匹配**
   - 前端使用 `matches_added`
   - 后端返回 `new_matches`

---

## ✅ 已修复

### 1. 前端自动爬取

**文件：** `frontend/index_new.html`

**修改：** `searchTeam()` 函数现在会自动调用爬虫 API

```javascript
// 新增的爬虫调用
try {
    showMessage('正在从 RobotEvents 爬取最新比赛数据...', 'info');
    const syncResult = await fetch(
        `${API_BASE}/matches/sync?team=${teamNumber}&event=ALL&scraper=robotevents`
    );
    const syncData = await syncResult.json();
    
    if (syncData.success && syncData.new_matches > 0) {
        showMessage(`成功爬取 ${syncData.new_matches} 场新比赛记录!`, 'success');
    } else if (syncData.mock_data) {
        showMessage('使用模拟数据（未配置 API Key）', 'warning');
    }
} catch (syncError) {
    console.warn('Failed to sync matches:', syncError);
    // 继续显示已有数据
}
```

### 2. 后端处理 "ALL" event_id

**文件：** `backend/app/services/scrapers/base_scraper.py`

**修改：** 正确处理 "ALL" 以获取所有赛事

```python
# Only add event filter if event_id is provided and not "ALL"
if event_id and event_id.upper() != "ALL":
    matches_params["event[]"] = event_id
```

### 3. 添加 mock_data 标记

**文件：** `backend/app/services/analytics.py`

**修改：** 返回是否使用模拟数据的标记

```python
# Check if we're using mock data
is_mock = len(matches_data) > 0 and all(
    m.get('event_id', '').startswith('DEMO') or 
    m.get('event_name', '').startswith('Mock')
    for m in matches_data
)

return {
    "success": True,
    "new_matches": new_count,
    "mock_data": is_mock  # ← 新增
}
```

---

## 🎯 现在的工作流程

### 完整的搜索流程

```
1. 用户输入队伍编号，点击搜索
   ↓
2. 提示："正在加载队伍历史数据..."
   ↓
3. 检查数据库中是否有该队伍
   - 如果没有 → 创建队伍记录
   ↓
4. 调用爬虫 API
   提示："正在从 RobotEvents 爬取最新比赛数据..."
   ↓
5a. 如果配置了有效 API Key：
    → 从 RobotEvents 获取真实数据
    → 保存到数据库
    → 提示："成功爬取 X 场新比赛记录!"
    
5b. 如果没有 API Key：
    → 使用模拟数据
    → 保存到数据库
    → 提示："使用模拟数据（未配置 API Key）"
    
5c. 如果 API 调用失败：
    → 回退到模拟数据
    → 继续显示已有数据
   ↓
6. 从数据库加载所有比赛记录
   ↓
7. 显示队伍信息和比赛历史
   ↓
8. 加载该队伍的 Auton 配置
```

---

## 📊 三种数据源模式

### 模式 1: 真实数据（推荐）

**条件：** 配置了有效的 RobotEvents API Key

**特点：**
- ✅ 获取真实的比赛数据
- ✅ 包含所有赛事历史
- ✅ 数据准确可靠
- ⚠️ 需要申请 API Key

**配置：**
```bash
# backend/.env
ROBOTEVENTS_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
```

### 模式 2: 模拟数据（当前默认）

**条件：** 未配置 API Key 或 Key 无效

**特点：**
- ✅ 立即可用，无需配置
- ✅ 用于演示和开发
- ⚠️ 数据是虚构的
- ⚠️ 每个队伍都返回相同的模拟数据

**提示信息：**
```
⚠️  No RobotEvents API Key configured
ℹ️  Using mock data for demonstration
```

### 模式 3: 数据库缓存

**条件：** 之前已成功爬取过数据

**特点：**
- ✅ 从本地数据库读取
- ✅ 速度快
- ⚠️ 可能不是最新数据
- ℹ️ 重新搜索会更新

---

## 🧪 测试步骤

### 测试 1: 重启后端

```powershell
# 停止当前后端（Ctrl+C）
# 重新启动
.\start.bat
```

**预期：** 后端成功启动，显示启动信息

### 测试 2: 搜索新队伍

1. 刷新前端页面（F5）
2. 输入队伍编号（如：12345A）
3. 点击搜索

**预期消息：**
```
正在加载队伍历史数据...
正在从 RobotEvents 爬取最新比赛数据...
使用模拟数据（未配置 API Key）  ← 如果没有 API Key
成功爬取 5 场新比赛记录!  ← 如果有 API Key
```

**预期结果：**
- ✅ 显示队伍基本信息
- ✅ 显示比赛统计（平均分、最高分等）
- ✅ 显示比赛历史列表（最多 20 场）
- ✅ 每场比赛显示日期、比分、结果

### 测试 3: 再次搜索同一队伍

1. 搜索同一队伍编号
2. 观察消息

**预期：**
- ✅ 可能显示 "No new matches to add"（如果数据已在数据库中）
- ✅ 仍然显示所有比赛记录
- ✅ 数据来自数据库缓存

### 测试 4: 查看控制台日志

**浏览器控制台（F12）：**
```javascript
Sync result: {
  success: true,
  team_number: "12345A",
  event_id: "ALL",
  new_matches: 5,
  updated_matches: 0,
  total_matches: 5,
  mock_data: true  // 或 false
}
```

**后端控制台：**
```
⚠️  No RobotEvents API Key configured
ℹ️  Using mock data for demonstration
📊 Generating mock data for team 12345A
   This is sample data for demonstration purposes
```

---

## 🔑 配置真实 API Key

如果想使用真实数据：

### 步骤 1: 申请 API Key

访问: https://www.robotevents.com/api/v2/accessRequest/create

填写申请表单：
- **Application Name:** RscoutX
- **Description:** VEX V5 team scouting application
- **Usage:** Educational/Development

### 步骤 2: 配置 Key

编辑 `backend/.env`：
```bash
ROBOTEVENTS_API_KEY=你的实际API_Key
```

### 步骤 3: 重启后端

```powershell
.\start.bat
```

### 步骤 4: 测试

搜索真实队伍编号，应该看到：
```
🔄 Attempting to fetch real data from RobotEvents API...
✓ Successfully fetched X matches from RobotEvents
成功爬取 X 场新比赛记录!
```

---

## 📝 模拟数据说明

当使用模拟数据时，每个队伍会生成 5 场虚构比赛：

```javascript
{
  match_id: "Q1", "Q2", "Q3", "SF1", "F1"
  event_id: "DEMO"
  event_name: "Mock Event 2024"
  score_for: 50-100 (随机)
  score_against: 40-90 (随机)
  result: "win" / "loss" / "tie"
  alliance: "red" / "blue" (随机)
}
```

**特征：**
- 事件 ID 以 "DEMO" 开头
- 事件名称包含 "Mock"
- 数据随机生成但结构正确
- 用于演示和测试界面

---

## 🔍 调试信息

### 检查爬虫是否被调用

**浏览器网络面板（F12 → Network）：**
```
GET /api/matches/sync?team=12345A&event=ALL&scraper=robotevents
Status: 200 OK
Response: { success: true, new_matches: 5, ... }
```

### 检查数据库是否保存

**后端日志：**
```
INFO: Syncing matches for team 12345A
INFO: Fetching from RobotEvents API...
INFO: Saved 5 new matches to database
```

### 检查 API Key 状态

**后端启动时：**
```
# 有 API Key
ℹ️  RobotEvents API Key: Configured ✓

# 无 API Key
⚠️  RobotEvents API Key: Not configured
```

---

## ⚠️ 常见问题

### 问题 1: 搜索后没有比赛记录

**可能原因：**
1. 使用模拟数据但未保存到数据库
2. API 调用失败且没有回退
3. 队伍编号不存在

**解决：**
- 查看浏览器控制台错误
- 查看后端日志
- 确认队伍编号正确

### 问题 2: 一直显示"正在爬取..."

**可能原因：**
- API 请求超时
- 网络问题
- 后端未响应

**解决：**
- 检查后端是否运行
- 查看网络面板的请求状态
- 增加超时时间

### 问题 3: 显示模拟数据但想要真实数据

**原因：** 未配置 API Key

**解决：**
1. 申请 RobotEvents API Key
2. 配置到 `.env` 文件
3. 重启后端
4. 重新搜索队伍

---

## 📈 性能优化

### 缓存机制

爬虫使用内存缓存：
- **默认过期时间：** 30 分钟
- **缓存键：** `robotevents_{队伍}_{赛事}`
- **自动刷新：** 过期后重新获取

### 避免重复爬取

- 数据库检查避免重复保存
- 只保存新的或更新的比赛
- 返回 `new_matches` 和 `updated_matches` 计数

### 错误回退

- API 失败 → 模拟数据
- 模拟数据失败 → 显示已有数据
- 确保界面始终可用

---

**修复时间：** 2026年1月2日  
**问题：** 无法爬取比赛记录  
**解决方案：** 添加自动爬取功能并修复相关配置  
**状态：** ✅ 已修复，需重启后端测试
