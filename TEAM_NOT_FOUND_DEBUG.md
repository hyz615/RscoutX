# 🔍 RobotEvents API 队伍查询指南

## 问题诊断

根据日志显示：
```
🔍 Step 1: Searching for team 16610B...
📊 Team search response: 200
❌ No teams found for 16610B
```

**结论：** API Key 有效，连接正常，但队伍 "16610B" 在 RobotEvents 数据库中不存在。

---

## 可能的原因

### 1. 队伍编号格式错误

VEX 队伍编号有多种格式：
- **标准格式**: `16610A`, `16610B`, `16610C` 等
- **完整格式**: `16610A-1`, `16610B-1` 等（带机器人编号）
- **仅数字**: `16610` （不带字母后缀）

### 2. 队伍尚未注册

- 新队伍可能还没有在 RobotEvents 注册
- 队伍可能已改名或合并
- 队伍可能在不同的赛季使用不同编号

### 3. 区域或项目限制

- 当前只搜索 V5RC 项目
- 可能是其他项目（VRC, VIQC 等）的队伍

---

## 🧪 测试真实队伍编号

### 方法 1: 直接访问 RobotEvents 网站

访问: https://www.robotevents.com/teams/V5RC

**搜索步骤：**
1. 在搜索框输入队伍编号
2. 查看搜索结果
3. 确认队伍是否存在
4. 复制准确的队伍编号

### 方法 2: 使用 API 浏览器测试

访问: https://www.robotevents.com/api/v2

**测试 API：**
```
GET https://www.robotevents.com/api/v2/teams
Parameters:
  - number: 16610A
  - program: V5RC
Headers:
  - Authorization: Bearer YOUR_API_KEY
```

### 方法 3: 使用我们的测试脚本

我将创建一个 Python 脚本来测试队伍：

---

## 🎯 已知有效的测试队伍

以下是一些已知存在的队伍（用于测试）：

### 中国队伍
- **229V** - 深圳中学
- **1721B** - 上海队伍
- **95070A** - 著名队伍
- **315X** - 历史悠久的队伍

### 国际著名队伍
- **62A** - QUEENS
- **169A** - 美国队伍
- **1961Z** - 著名队伍
- **7K** - 新加坡队伍

### 搜索建议

1. **先测试已知队伍**
   ```
   试试搜索: 229V, 315X, 62A
   ```

2. **确认目标队伍编号**
   - 访问 RobotEvents 网站
   - 搜索并确认队伍存在
   - 复制准确编号

3. **检查编号格式**
   - 字母大写（A, B, C）
   - 不要多余空格
   - 不要特殊字符

---

## 📊 API 搜索参数

当前搜索使用的参数：

```python
params = {
    "number": "16610B",      # 队伍编号
    "program": "V5RC"        # VEX V5 机器人竞赛
}
```

### 可选的项目类型

- **V5RC** - VEX V5 Robotics Competition
- **VEXU** - VEX U (大学)
- **VIQC** - VEX IQ Challenge
- **VAIRC** - VEX AI Robotics Competition

### 搜索技巧

**模糊搜索：**
```python
# 搜索所有 16610 开头的队伍
params = {
    "number[0]": "16610",    # 部分匹配
    "program": "V5RC"
}
```

**按地区搜索：**
```python
params = {
    "country": "China",
    "program": "V5RC"
}
```

---

## 🔧 修改搜索逻辑（可选）

如果需要支持模糊搜索，可以修改 `base_scraper.py`：

### 当前代码
```python
team_response = await client.get(
    f"{self.API_URL}/teams",
    params={
        "number": team_number,
        "program": "V5RC"
    },
    headers=headers
)
```

### 增强版（支持部分匹配）
```python
# 先尝试精确匹配
team_response = await client.get(
    f"{self.API_URL}/teams",
    params={
        "number": team_number,
        "program": "V5RC"
    },
    headers=headers
)

teams_data = team_response.json()

# 如果没找到，尝试部分匹配
if not teams_data.get("data"):
    team_response = await client.get(
        f"{self.API_URL}/teams",
        params={
            "number[0]": team_number,  # 部分匹配
            "program": "V5RC"
        },
        headers=headers
    )
```

---

## 🎯 立即测试步骤

### 测试 1: 验证 API Key

访问这个 URL（替换你的 API Key）：
```
https://www.robotevents.com/api/v2/teams?number=229V&program=V5RC
```

在浏览器或 Postman 中添加 Header：
```
Authorization: Bearer YOUR_API_KEY
```

**预期结果：**
```json
{
  "data": [
    {
      "id": 123456,
      "number": "229V",
      "team_name": "...",
      "robot_name": "...",
      "organization": "...",
      "location": {...}
    }
  ]
}
```

### 测试 2: 在前端测试已知队伍

1. 刷新前端页面
2. 输入已知存在的队伍：**229V**
3. 点击搜索
4. 观察结果

**预期：**
- 如果返回真实数据 → API 正常工作
- 如果返回模拟数据 → API 或队伍编号有问题

### 测试 3: 检查 16610B 是否存在

访问: https://www.robotevents.com/teams/V5RC/16610B

**可能结果：**
- **找到队伍** → 复制准确的编号格式
- **404 错误** → 队伍不存在，尝试其他编号
- **需要登录** → 队伍存在但受限

---

## 📝 常见队伍编号问题

### 问题 1: 字母后缀混淆

```
16610B  ✓ (大写 B)
16610b  ✗ (小写 b)
16610 B ✗ (有空格)
```

### 问题 2: 零和字母 O

```
16610  ✓ (数字 0)
1661O  ✗ (字母 O)
```

### 问题 3: 额外后缀

```
16610B    ✓ (标准格式)
16610B-1  ? (可能需要去掉 -1)
16610B_1  ✗ (下划线不对)
```

---

## 🔍 调试建议

### 1. 查看完整的 API 响应

修改 `base_scraper.py` 临时添加日志：
```python
teams_data = team_response.json()
print(f"📋 Full API response: {json.dumps(teams_data, indent=2)}")
```

### 2. 测试不同的队伍编号

在前端依次测试：
- `229V` (已知存在)
- `315X` (已知存在)
- `16610A` (你要查的相似编号)
- `16610B` (你要查的编号)

### 3. 检查网络日志

打开浏览器 F12 → Network 标签
观察发送给 RobotEvents 的实际请求

---

## 💡 建议的解决方案

### 方案 1: 使用已知存在的队伍测试

先测试系统是否正常工作：
```
搜索: 229V
```

如果返回真实数据，说明系统正常，只是 16610B 不存在。

### 方案 2: 查找正确的队伍编号

1. 访问 https://www.robotevents.com
2. 搜索 "16610"
3. 查看所有相关队伍
4. 使用准确的编号

### 方案 3: 联系队伍确认

如果你知道这个队伍：
- 询问他们的官方 VEX 编号
- 确认是否已在 RobotEvents 注册
- 确认是 V5RC 还是其他项目

---

## 🎓 RobotEvents 队伍注册说明

如果是新队伍尚未注册：

1. 访问: https://www.robotevents.com/teams
2. 点击 "Register a Team"
3. 选择项目 (V5RC, VIQC 等)
4. 提供组织信息
5. 获得官方队伍编号
6. 等待 24-48 小时生效

---

## 📞 需要帮助？

**提供以下信息以便进一步诊断：**

1. 队伍来源（学校/组织名称）
2. 所在地区/国家
3. 参加的赛季/年份
4. 尝试搜索其他已知队伍的结果

**测试命令：**
```bash
# 在前端搜索这些队伍，告诉我结果：
229V - 应该返回真实数据
315X - 应该返回真实数据
16610A - 查看是否存在
16610 - 查看是否存在（不带字母）
```

---

**诊断日期：** 2026年1月2日  
**问题：** Team 16610B not found  
**API 状态：** ✅ 正常工作  
**下一步：** 验证队伍编号是否正确或使用已知队伍测试
