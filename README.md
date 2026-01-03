# 🤖 RscoutX - VEX V5 Pushback 智能侦查系统

[English](#english) | [中文](#chinese)

---

<a name="chinese"></a>
## 📋 项目简介

RscoutX 是一个专为 VEX V5 Pushback 竞赛设计的综合数据分析和侦查系统。支持场地地图路径渲染、机器人类型分析、驾驶员习惯画像、比赛历史抓取以及 AI 驱动的战队报告生成。

### ✨ 核心功能

1. **🗺️ 场地地图路径渲染**
   - 支持多种渲染方法：折线、贝塞尔曲线、样条曲线、A* 寻路、热力线
   - 像素/场地坐标系统转换
   - 可自定义样式（颜色、宽度、透明度、箭头）
   - 支持障碍物避让

2. **🔧 机器人类型管理**
   - 底盘类型：SBOT、瑞冠、CBOT（可扩展）
   - 可折叠性、传动系统、轮胎数量等属性
   - 完整的 CRUD Web 管理界面

3. **👤 驾驶员习惯画像**
   - 比赛风格：进攻型/防守型/平衡型
   - 控制灵活度（1-10）、速度偏好
   - 是否喜欢使用抓取机构
   - 完整的 CRUD Web 管理界面

4. **📊 比赛历史抓取**
   - 可插拔的爬虫架构（适配器模式）
   - 支持 RobotEvents 和自定义数据源
   - 可配置的 HTML 解析规则
   - 智能缓存和重试机制

5. **🤖 AI 战队报告生成**
   - 支持 OpenAI GPT 和 Ollama 本地模型
   - 中英文双语报告
   - 输出 Markdown 和 JSON 格式
   - 包含优势分析、风险评估、对抗策略

## 🏗️ 项目结构

```
RscoutX/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py            # 应用入口
│   │   ├── core/
│   │   │   └── config.py      # 配置管理
│   │   ├── db/
│   │   │   └── session.py     # 数据库会话
│   │   ├── models/
│   │   │   └── models.py      # SQLModel 数据模型
│   │   ├── schemas/
│   │   │   └── schemas.py     # Pydantic 模式
│   │   ├── api/routes/        # API 路由
│   │   │   ├── teams.py
│   │   │   ├── robots.py
│   │   │   ├── drivers.py
│   │   │   ├── matches.py
│   │   │   ├── path.py
│   │   │   └── report.py
│   │   ├── services/          # 业务逻辑
│   │   │   ├── path_renderer.py
│   │   │   ├── analytics.py
│   │   │   ├── scrapers/
│   │   │   │   └── base_scraper.py
│   │   │   └── llm/
│   │   │       ├── providers.py
│   │   │       └── report_generator.py
│   │   └── prompts/           # LLM 提示模板
│   │       └── report_prompts.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/                   # HTML+CSS+JS 前端
│   ├── index.html             # 主页面
│   ├── app.js                 # 应用逻辑
│   ├── styles.css             # 样式
│   └── package.json
├── pushback_map.png           # 场地地图（必须在根目录）
├── start.bat                  # Windows 启动脚本
└── README.md
```

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Windows 操作系统（使用 start.bat）
- （可选）OpenAI API 密钥或 Ollama 本地部署

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-repo/RscoutX.git
   cd RscoutX
   ```

2. **配置环境变量**
   ```bash
   cd backend
   copy .env.example .env
   # 编辑 .env 文件，填入 OPENAI_API_KEY 或配置 Ollama
   ```

3. **一键启动**
   ```bash
   # 默认端口 8000
   start.bat
   
   # 或指定端口
   start.bat 80
   start.bat 443
   start.bat 8080
   ```

4. **访问应用**
   - 前端界面: http://localhost:3000
   - API 文档: http://localhost:8000/api/docs
   - 后端 API: http://localhost:8000/api

### SSL/HTTPS 配置（端口 443）

设置环境变量后启动：
```bash
set SSL_CERTFILE=path\to\cert.pem
set SSL_KEYFILE=path\to\key.pem
start.bat 443
```

或使用反向代理（Nginx/Caddy）。

## 📖 API 使用示例

### 1. 创建战队
```bash
curl -X POST "http://localhost:8000/api/teams/" \
  -H "Content-Type: application/json" \
  -d "{\"team_number\": \"1234A\", \"team_name\": \"Dragon Robotics\", \"organization\": \"Example School\", \"region\": \"China\"}"
```

### 2. 创建机器人配置
```bash
curl -X POST "http://localhost:8000/api/robots/" \
  -H "Content-Type: application/json" \
  -d "{\"team_id\": 1, \"robot_base\": \"sbot\", \"foldable\": true, \"drivetrain\": \"4-motor tank\", \"tire_count\": 4, \"notes\": \"High grip tires\"}"
```

### 3. 创建驾驶员画像
```bash
curl -X POST "http://localhost:8000/api/drivers/" \
  -H "Content-Type: application/json" \
  -d "{\"team_id\": 1, \"driver_name\": \"Alex\", \"playstyle\": \"aggressive\", \"likes_claw\": true, \"control_agility\": 8, \"speed_preference\": \"fast\", \"notes\": \"Experienced driver\"}"
```

### 4. 同步比赛数据
```bash
curl "http://localhost:8000/api/matches/sync?team=1234A&event=RE-VRC-23-1234"
```

### 5. 渲染路径
```bash
curl -X POST "http://localhost:8000/api/path/render/image" \
  -H "Content-Type: application/json" \
  -d "{\"method\": \"bezier\", \"points\": [{\"x\": 100, \"y\": 100}, {\"x\": 300, \"y\": 200}, {\"x\": 500, \"y\": 100}], \"style\": {\"color\": \"#FF0000\", \"width\": 3}, \"coordinate_system\": \"pixel\"}" \
  --output path_render.png
```

### 6. 生成 AI 报告
```bash
curl -X POST "http://localhost:8000/api/report/generate" \
  -H "Content-Type: application/json" \
  -d "{\"team_id\": 1, \"event_id\": \"RE-VRC-23-1234\", \"include_map\": true, \"include_driver\": true, \"include_robot\": true, \"language\": \"zh\"}"
```

## 🎯 Web 界面使用

### Dashboard（仪表板）
1. 输入队号和赛事 ID
2. 点击"Sync Matches"同步比赛数据
3. 查看统计数据和趋势图表

### Map（地图）
1. 选择渲染方法（折线/贝塞尔/样条/A*/热力线）
2. 选择坐标系统（像素/场地）
3. 添加路径点
4. 点击"Render Path"查看结果

### Admin（管理）
- **机器人管理**: 创建、查看、删除机器人配置
- **驾驶员管理**: 创建、查看、删除驾驶员画像

### Report（报告）
1. 输入队伍 ID 和赛事 ID（可选）
2. 选择语言（中文/英文）
3. 点击"Generate Report"生成 AI 报告
4. 复制 Markdown 或 JSON 格式

## 🔧 开发

### 手动启动后端
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 手动启动前端
```bash
cd frontend
python -m http.server 3000
```

### 运行测试
```bash
cd backend
pytest tests/
```

## 🌐 部署

### Linux/Ubuntu 部署
详见 [UBUNTU_DEPLOY.md](UBUNTU_DEPLOY.md)

快速命令:
```bash
# 检查环境
./check_deploy.sh

# 修复地图文件位置
./fix_pushback_map.sh

# 启动服务
sudo ./start_daemon.sh
```

### 生产环境
建议使用 Nginx/Caddy 作为反向代理：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api {
        proxy_pass http://localhost:8000;
    }
    
    location / {
        proxy_pass http://localhost:3000;
    }
}
```

## 🐛 故障排查

### Linux 部署时提示 pushback_map.png 未找到

**问题原因**: 后端配置使用相对路径,在 Linux 工作目录不同时可能找不到文件。

**解决方案 1 - 自动修复（推荐）**:
```bash
chmod +x fix_pushback_map.sh
./fix_pushback_map.sh
```

**解决方案 2 - 手动复制**:
```bash
# 确保 pushback_map.png 在项目根目录
cp frontend/pushback_map.png .
```

**解决方案 3 - 检查文件位置**:
```bash
# 运行检查脚本
./check_deploy.sh

# 查看后端日志中的路径信息
tail -f logs/rscoutx.log
```

**验证修复**:
- 启动服务后,检查日志中是否有 "✅ 找到地图文件" 或 "⚠️ 警告: 地图文件未找到"
- 访问地图渲染 API,确认能正常加载背景图

### 其他常见问题

**问题**: 服务启动失败
```bash
# 检查 Python 环境
python3 --version
which python3

# 检查依赖安装
cd backend
venv/bin/pip list | grep fastapi
```

**问题**: 端口被占用
```bash
# 检查端口占用
sudo lsof -i :80
sudo lsof -i :8000

# 结束占用进程
sudo kill -9 <PID>
```

## 📝 配置说明

### 环境变量 (.env)

```ini
# 数据库
DATABASE_URL=sqlite:///./rscoutx.db

# LLM 提供者
LLM_PROVIDER=openai  # 或 ollama
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# 爬虫
SCRAPER_CACHE_MINUTES=30
SCRAPER_TIMEOUT_SECONDS=30

# 地图
MAP_IMAGE_PATH=../pushback_map.png
```

## 🤝 贡献

欢迎提交 Pull Request 和 Issue!

## 📄 许可证

MIT License

---

<a name="english"></a>
## 📋 Project Overview

RscoutX is a comprehensive data analysis and scouting system designed for VEX V5 Pushback competitions. Features include field map path rendering, robot type analysis, driver habit profiling, match history scraping, and AI-powered team report generation.

### ✨ Key Features

1. **🗺️ Field Map Path Rendering**
   - Multiple rendering methods: polyline, bezier, spline, A*, heatline
   - Pixel/field coordinate system conversion
   - Customizable styles (color, width, opacity, arrows)
   - Obstacle avoidance support

2. **🔧 Robot Type Management**
   - Robot bases: SBOT, Ruiguan, CBOT (extensible)
   - Attributes: foldable, drivetrain, tire count
   - Full CRUD web interface

3. **👤 Driver Habit Profiling**
   - Playstyle: aggressive/defensive/balanced
   - Control agility (1-10), speed preference
   - Claw preference tracking
   - Full CRUD web interface

4. **📊 Match History Scraping**
   - Pluggable scraper architecture (adapter pattern)
   - RobotEvents and custom source support
   - Configurable HTML parsing rules
   - Smart caching and retry logic

5. **🤖 AI Team Report Generation**
   - OpenAI GPT and Ollama support
   - Bilingual reports (Chinese/English)
   - Markdown and JSON output
   - Strengths, risks, and counter-strategies

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Windows OS (for start.bat)
- (Optional) OpenAI API key or Ollama

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-repo/RscoutX.git
   cd RscoutX
   ```

2. **Configure Environment**
   ```bash
   cd backend
   copy .env.example .env
   # Edit .env and add your OPENAI_API_KEY or configure Ollama
   ```

3. **One-Click Start**
   ```bash
   # Default port 8000
   start.bat
   
   # Or specify port
   start.bat 80
   start.bat 443
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/api/docs
   - Backend API: http://localhost:8000/api

### SSL/HTTPS Setup (Port 443)

Set environment variables before starting:
```bash
set SSL_CERTFILE=path\to\cert.pem
set SSL_KEYFILE=path\to\key.pem
start.bat 443
```

Or use a reverse proxy (Nginx/Caddy).

## 📖 API Examples

See Chinese section above for curl examples.

## 🎯 Web Interface Guide

### Dashboard
- Enter team number and event ID
- Sync matches
- View statistics

### Map
- Select rendering method
- Add path points
- Render and preview

### Admin
- Manage robots
- Manage drivers

### Report
- Generate AI-powered reports
- Copy Markdown or JSON

## 🔧 Development

### Manual Backend Start
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Manual Frontend Start
```bash
cd frontend
python -m http.server 3000
```

## 🤝 Contributing

Pull requests and issues welcome!

## 📄 License

MIT License

---

**Made with ❤️ for VEX Robotics Community**
