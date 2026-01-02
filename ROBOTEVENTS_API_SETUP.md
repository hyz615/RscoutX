# RobotEvents API 配置指南

## 🔑 获取 API Key

1. 访问 RobotEvents 网站：https://www.robotevents.com
2. 注册/登录账号
3. 前往开发者设置：https://www.robotevents.com/api/v2
4. 创建 API Token
5. 复制 API Key

## ⚙️ 配置步骤

### 方法 1: 环境变量（推荐）

在项目根目录创建 `.env` 文件：

```env
ROBOTEVENTS_API_KEY=your_api_key_here
```

### 方法 2: 直接修改配置

编辑 `backend/app/core/config.py`：

```python
ROBOTEVENTS_API_KEY: Optional[str] = "your_api_key_here"
```

## 📊 API 功能说明

### V5RC 数据爬取

新实现的 `RoboteventsScraper` 可以：

✅ **搜索队伍**
- 通过队伍编号（如 `1234A`）搜索
- 自动识别 V5RC 项目

✅ **获取比赛数据**
- 队伍所有历史比赛
- 比赛得分（红方/蓝方）
- 胜负结果
- 对手信息
- 比赛日期和赛事信息

✅ **智能降级**
- 如果 API 调用失败，自动使用模拟数据
- 保证系统正常运行

### API 端点

```
GET /teams
  - 搜索队伍
  - 参数: number, program (V5RC)

GET /matches
  - 获取比赛记录
  - 参数: team[], season[], event[]
```

## 📝 API 限制

- **速率限制**: 通常为 60 requests/minute
- **数据缓存**: 系统自动缓存 30 分钟
- **超时设置**: 30 秒超时
- **重试机制**: 最多重试 3 次

## 🔍 测试 API

启动后端后，在前端输入队伍编号测试：

```
队伍编号: 229V  （世界冠军队伍示例）
```

系统将自动：
1. 从 RobotEvents 搜索队伍
2. 获取所有历史比赛数据
3. 计算统计信息（胜率、平均分等）
4. 显示近期比赛记录

## ⚠️ 注意事项

1. **无 API Key**: 系统会使用模拟数据，但提示"从 RobotEvents API 获取失败"
2. **网络问题**: 确保服务器可以访问 robotevents.com
3. **赛季更新**: 需要更新 `season[]` 参数（当前设为 181）

## 🌐 API 文档

完整 API 文档：https://www.robotevents.com/api/v2

主要字段说明：
```json
{
  "id": 123456,
  "team": {
    "id": 12345,
    "number": "1234A",
    "team_name": "Example Team"
  },
  "event": {
    "id": 56789,
    "name": "VEX Worlds 2024",
    "code": "RE-VRC-24-0001"
  },
  "alliances": [
    {
      "color": "red",
      "score": 85,
      "teams": [...]
    },
    {
      "color": "blue", 
      "score": 72,
      "teams": [...]
    }
  ]
}
```

## 🚀 快速开始

1. 获取 API Key
2. 添加到 `.env` 文件
3. 重启后端：`.\start.bat`
4. 打开前端，搜索任意 V5RC 队伍编号
5. 查看真实的历史数据！
