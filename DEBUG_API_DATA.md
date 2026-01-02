# 🐛 调试真实 API 数据获取

## 问题描述

即使配置了 RobotEvents API Key，仍然显示模拟数据：
```
Q1 2026/1/2
✅ 红方 50 : 45 胜利
📍 VEX Demo Event ALL
🤝 对手: Team1000, Team2000
```

**模拟数据的特征：**
- 事件名称：`VEX Demo Event ALL`
- 对手队伍：`Team1000, Team2000` (虚构的)
- 比分：50:45 (固定模式)

---

## 🔍 可能的原因

### 1. API Key 未正确读取
- `.env` 文件格式错误
- 环境变量未加载
- API Key 有多余空格

### 2. API 调用失败
- API Key 无效或过期
- 网络连接问题
- API 限流或配额用尽
- 队伍编号不存在

### 3. 缓存问题
- 使用了之前的缓存数据
- 缓存未过期（默认 30 分钟）

---

## ✅ 已添加的调试日志

修改了 `backend/app/services/scrapers/base_scraper.py`，添加详细日志：

### 日志输出示例

**成功的真实 API 调用：**
```
============================================================
🔍 Attempting to fetch data for team: 16610A
   Event filter: ALL
   API Key configured: Yes
   API Key preview: eyJ0eXAiOiJKV1QiLCJh...
============================================================

   📡 Connecting to RobotEvents API...
   API URL: https://www.robotevents.com/api/v2
   🔍 Step 1: Searching for team 16610A...
   📊 Team search response: 200
   ✓ Found team: Example Team (ID: 123456)
   🔍 Step 2: Fetching matches for team ID 123456...
   🎯 Fetching all events (no filter)
   📊 Matches fetch response: 200
   ✓ Received 25 matches from API
   🔄 Parsing match data...
   ✓ Parsed 25 matches successfully
✓ Successfully fetched 25 matches from RobotEvents
✓ Data source: REAL API DATA
```

**API 调用失败：**
```
============================================================
🔍 Attempting to fetch data for team: 16610A
   Event filter: ALL
   API Key configured: Yes
   API Key preview: eyJ0eXAiOiJKV1QiLCJh...
============================================================

🔄 Attempting to fetch real data from RobotEvents API...
   📡 Connecting to RobotEvents API...
   API URL: https://www.robotevents.com/api/v2
   🔍 Step 1: Searching for team 16610A...
   📊 Team search response: 401
   ❌ Team search failed with status 401
   Response: {"error":"Unauthorized","message":"Invalid token"}
❌ Failed to fetch from RobotEvents API: Team search failed: 401 - ...
❌ Error type: Exception
❌ Error details: Team search failed: 401 - Invalid token
⚠️  Falling back to mock data
📊 Generating mock data for team 16610A
   This is sample data for demonstration purposes
✓ Generated 5 sample matches
```

---

## 🧪 调试步骤

### 步骤 1: 重启后端查看日志

```powershell
# 停止当前后端 (Ctrl+C)
.\start.bat
```

**重要：** 后端启动后，不要立即测试，等待完全启动。

### 步骤 2: 搜索队伍并观察后端日志

1. 打开前端页面
2. 搜索队伍：16610A
3. **立即切换到后端终端窗口**
4. 查看详细的日志输出

### 步骤 3: 分析日志

**检查项 1: API Key 是否配置**
```
API Key configured: Yes    ← 应该是 Yes
API Key preview: eyJ0...   ← 应该显示前 20 个字符
```

如果显示 `No`：
- 检查 `.env` 文件中的 `ROBOTEVENTS_API_KEY=`
- 确保没有多余空格
- 确保 Key 不为空

**检查项 2: API 响应状态**
```
📊 Team search response: 200  ← 应该是 200
```

常见错误码：
- `401 Unauthorized` - API Key 无效
- `403 Forbidden` - API Key 权限不足
- `404 Not Found` - 队伍不存在
- `429 Too Many Requests` - 请求过于频繁
- `500 Internal Server Error` - API 服务器错误

**检查项 3: 是否找到队伍**
```
✓ Found team: Example Team (ID: 123456)
```

如果显示 `❌ No teams found`：
- 队伍编号可能不存在
- 尝试其他已知存在的队伍编号

**检查项 4: 数据来源**
```
✓ Data source: REAL API DATA  ← 真实数据
```

如果显示：
```
📊 Generating mock data  ← 模拟数据
```

说明 API 调用失败，已回退到模拟数据。

---

## 🔧 常见问题修复

### 问题 1: API Key 无效 (401)

**症状：**
```
📊 Team search response: 401
❌ Team search failed with status 401
Response: {"error":"Unauthorized"}
```

**原因：** API Key 无效、过期或格式错误

**解决：**
1. 访问 https://www.robotevents.com/api/v2/accessRequest/create
2. 申请新的 API Key
3. 复制完整的 Token
4. 更新 `backend/.env`:
   ```bash
   ROBOTEVENTS_API_KEY=你的新API_Key
   ```
5. 重启后端

### 问题 2: 队伍不存在 (404)

**症状：**
```
✓ Team search response: 200
❌ No teams found for 16610A
```

**原因：** 队伍编号不存在或不在 V5RC 项目中

**解决：**
- 确认队伍编号正确（包括字母后缀）
- 尝试已知存在的队伍：
  - `7842F` (Voltage)
  - `229V` (VRC)
  - `315X`

### 问题 3: 使用了缓存数据

**症状：**
```
✓ Using cached data for team 16610A
```

**原因：** 数据在缓存中，未重新获取

**解决：**
```python
# 清除缓存，在浏览器控制台执行：
await fetch('http://localhost:8000/api/matches/sync?team=16610A&event=ALL&scraper=robotevents')
```

或等待 30 分钟缓存自动过期。

### 问题 4: 网络问题

**症状：**
```
❌ Failed to fetch from RobotEvents API: Connection timeout
```

**原因：** 无法连接到 RobotEvents 服务器

**解决：**
1. 检查网络连接
2. 尝试访问 https://www.robotevents.com
3. 检查防火墙设置
4. 如果在中国，可能需要代理

---

## 📊 验证真实数据

### 真实数据的特征

```
Q12 2024-11-15
✅ 红方 123 : 98 胜利
📍 VEX Robotics High Stakes - North Carolina State Championship
🤝 对手: 7842F, 229V
```

**特征：**
- ✅ 事件名称详细具体
- ✅ 日期是过去的真实日期
- ✅ 对手队伍有实际编号（如 7842F）
- ✅ 比分不是固定模式

### 模拟数据的特征

```
Q1 2026/1/2
✅ 红方 50 : 45 胜利
📍 VEX Demo Event ALL
🤝 对手: Team1000, Team2000
```

**特征：**
- ❌ 事件名称包含 "Demo" 或 "Mock"
- ❌ 日期是今天
- ❌ 对手是 "Team1000" 格式
- ❌ 比分是 50, 60, 70, 80, 90 (递增)

---

## 🎯 完整调试流程

1. **重启后端**
   ```powershell
   .\start.bat
   ```

2. **打开后端终端窗口**
   - 准备查看实时日志

3. **搜索队伍**
   - 在前端输入：16610A
   - 点击搜索

4. **立即查看后端日志**
   - 滚动到最新输出
   - 寻找上面提到的关键日志

5. **根据日志采取行动**
   - 如果 API Key 无效 → 更新 Key
   - 如果队伍不存在 → 换队伍编号
   - 如果网络问题 → 检查连接
   - 如果成功 → 验证数据是否真实

---

## 📝 快速检查清单

- [ ] `.env` 文件中 `ROBOTEVENTS_API_KEY` 已配置
- [ ] API Key 是完整的 JWT token (以 `eyJ` 开头)
- [ ] API Key 没有多余的空格或换行
- [ ] 后端已重启
- [ ] 清除了浏览器缓存或等待 30 分钟
- [ ] 队伍编号确实存在于 RobotEvents
- [ ] 网络可以访问 www.robotevents.com
- [ ] 查看后端日志确认 API 调用状态

---

## 🆘 仍然不工作？

**收集以下信息：**

1. **后端完整日志输出**（从搜索开始到结束）
2. **`.env` 文件中的 API Key 前 20 个字符**
3. **搜索的队伍编号**
4. **显示的数据示例**

**测试 API Key 有效性：**

```powershell
# PowerShell 测试
$headers = @{
    "Authorization" = "Bearer 你的API_Key"
    "Accept" = "application/json"
}
Invoke-RestMethod -Uri "https://www.robotevents.com/api/v2/teams?number=7842F&program=V5RC" -Headers $headers
```

如果返回数据，说明 API Key 有效。
如果返回 401 错误，说明 API Key 无效。

---

**更新时间：** 2026年1月2日  
**状态：** 已添加详细调试日志  
**下一步：** 重启后端并观察日志输出
