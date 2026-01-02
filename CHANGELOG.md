# RscoutX 更新日志

## 2026-01-02 - 重大更新

### ✨ 新功能

#### 1. 全新界面设计
- **新版 index.html**：完整重新设计的用户界面
- **旧版备份**：原版本保存为 `index_old.html`
- **6 大功能模块**：
  - 队伍搜索与信息展示
  - 比赛历史记录
  - Auton 路径绘制（多路径支持）
  - 机器人配置记录
  - 驾驶员笔记
  - AI 分析报告生成

#### 2. 自动数据爬取
- **RobotEvents API 集成**：自动从官方数据库获取比赛数据
- **2025-2026 赛季筛选**：只获取当前赛季（Push Back）的数据
- **实时同步**：搜索队伍时自动爬取最新数据
- **增量更新**：智能识别新比赛和已有比赛

#### 3. 数据持久化
- **队伍隔离存储**：每个队伍的数据独立保存
- **自动保存**：1 秒防抖，所有操作自动保存到 localStorage
- **数据库存储**：比赛数据保存到 SQLite 数据库
- **快速切换**：切换队伍时自动加载对应数据

#### 4. 多路径 Auton 支持
- **多路径管理**：支持创建、切换、删除多个 Auton 路径
- **独立命名**：每个 Auton 可以自定义名称
- **颜色区分**：不同 Auton 使用不同颜色绘制
- **路径编辑**：可以编辑、删除任意路径点

#### 5. AI 分析功能
- **GPT-4o 集成**：使用 OpenAI GPT-4o 模型分析数据
- **智能报告**：基于比赛数据生成分析报告
- **降级支持**：API 不可用时使用基础统计报告

### 🔧 技术改进

#### API 修复
- ✅ 修复了 RobotEvents API 端点错误
  - 旧：`/api/v2/matches` (404)
  - 新：`/api/v2/teams/{team_id}/matches` (正确)

- ✅ 移除了导致空结果的 `program` 参数
  - 旧：`{"number": "229V", "program": "V5RC"}` → 0 结果
  - 新：`{"number": "229V"}` → 成功找到队伍

- ✅ 添加了正确的赛季筛选
  - 使用赛季 ID: `197` (VEX V5 Robotics Competition 2025-2026: Push Back)
  - 设置 `per_page: 250` 获取更多数据

#### 数据刷新机制
- ✅ 爬取完成后自动刷新统计数据
- ✅ 爬取完成后自动刷新比赛列表
- ✅ 实时显示爬取进度和结果
- ✅ 详细的成功消息（比赛数、胜率、平均分）

#### 路由优化
- ✅ 修复了 FastAPI 路由冲突
  - 特定路由（`/sync`）放在动态路由（`/{match_id}`）之前
  - 避免 422 Unprocessable Entity 错误

### 📊 数据展示

#### 队伍信息卡片
- 队伍编号、名称、组织、地区
- 总比赛数、胜率、平均分、最高分
- 自动 Auton 分数（平均分 × 30%）
- 参赛事件数量

#### 比赛历史
- 显示最近 20 场比赛
- 按时间倒序排列
- 彩色边框区分胜负
- 联盟颜色标识（红/蓝）
- 显示对手信息和分数

### 🛠️ 配置文件

#### `.env` 配置
```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# RobotEvents API
ROBOTEVENTS_API_KEY=your_robotevents_token_here

# LLM Provider
LLM_PROVIDER=openai
```

### 📝 使用说明

#### 启动应用
```bash
# Windows
.\start.bat

# 或手动启动
cd backend
python -m uvicorn app.main:app --reload --port 8000

cd ../frontend
python -m http.server 3000
```

#### 访问地址
- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8000/api
- **API 文档**: http://localhost:8000/api/docs

#### 搜索队伍
1. 输入队伍编号（如：16610A、16610V、229V）
2. 点击"搜索队伍"
3. 系统自动：
   - 从 RobotEvents 爬取 2025-2026 赛季数据
   - 保存到数据库
   - 显示统计信息和比赛历史
   - 加载该队伍的 Auton 路径和配置

#### 绘制 Auton 路径
1. 点击"新增 Auton"创建新路径
2. 在地图上点击绘制路径点
3. 使用"删除最后一点"撤销
4. 切换不同 Auton 查看/编辑
5. 所有更改自动保存

#### 记录机器人配置
- 填写各个系统的配置信息
- 自动保存，切换队伍时自动加载

#### 生成 AI 报告
1. 确保配置了 OpenAI API Key
2. 点击"生成 AI 分析报告"
3. 系统分析队伍数据生成报告
4. 可以导出 JSON 格式

### 🐛 已修复的问题

1. ✅ RobotEvents API 返回 200 但数据为空
   - 原因：使用了 `program: "V5RC"` 参数
   - 解决：移除该参数

2. ✅ API 404 错误：路由未找到
   - 原因：使用了错误的端点 `/matches`
   - 解决：改用 `/teams/{team_id}/matches`

3. ✅ 爬取成功但页面不更新
   - 原因：使用爬取前的旧数据
   - 解决：爬取后重新获取最新数据

4. ✅ 422 路由冲突
   - 原因：`/sync` 被 `/{match_id}` 捕获
   - 解决：调整路由顺序

5. ✅ AI 生成失败
   - 原因：使用了不存在的模型 "gpt-5.2"
   - 解决：改用 "gpt-4o"

6. ✅ updateAutonInfo 未定义
   - 原因：函数被调用但未声明
   - 解决：添加函数定义

7. ✅ 获取所有历史数据包括旧赛季
   - 原因：未筛选赛季
   - 解决：添加赛季 ID 197 筛选

### 🔮 未来计划

- [ ] 添加队伍对比功能
- [ ] 支持技能赛成绩追踪
- [ ] 添加赛事日程提醒
- [ ] 导出 PDF 报告
- [ ] 移动端适配
- [ ] 离线模式支持
- [ ] 多语言支持（英文）

### 📦 依赖版本

#### 后端
- FastAPI: 0.104.1
- Uvicorn: 0.24.0
- SQLModel: 0.0.14
- SQLAlchemy: 2.0.23
- httpx: 0.25.2
- OpenAI: 1.3.7

#### 前端
- Vanilla JavaScript (无框架)
- HTML5 Canvas API
- LocalStorage API
- Fetch API

### 🙏 致谢

- RobotEvents API: 提供比赛数据
- OpenAI: GPT-4o 模型
- VEX Robotics: Push Back 游戏地图

---

**版本**: 2.0.0  
**日期**: 2026-01-02  
**作者**: GitHub Copilot & User
