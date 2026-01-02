# RscoutX Quick Start Guide

## 🚀 快速开始指南 (Quick Start)

### 1. 首次运行 (First Time Setup)

```bash
# 1. 确保已安装 Python 3.10+
python --version

# 2. 进入项目目录
cd RscoutX

# 3. 启动应用（自动安装依赖）
start.bat

# 4. 等待几秒钟，然后访问:
#    - 前端: http://localhost:3000
#    - API: http://localhost:8000/api/docs
```

### 2. 初始化种子数据 (Seed Data)

在后端目录运行种子数据脚本:

```bash
cd backend
venv\Scripts\activate
python seed_data.py
```

这将创建:
- 2 个示例战队
- 2 个机器人配置
- 2 个驾驶员画像
- 8 场比赛记录

### 3. 配置 LLM (可选)

编辑 `backend/.env`:

**使用 OpenAI:**
```ini
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
```

**使用 Ollama (本地):**
```ini
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### 4. 测试 API

#### 创建战队
```powershell
$headers = @{"Content-Type"="application/json"}
$body = @{
    team_number = "9999X"
    team_name = "Test Team"
    organization = "Test School"
    region = "China"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/teams/" -Method Post -Headers $headers -Body $body
```

#### 同步比赛
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/matches/sync?team=1234A&event=TEST-2024"
```

#### 渲染路径
```powershell
$body = @{
    method = "bezier"
    points = @(
        @{x=100; y=100},
        @{x=300; y=200},
        @{x=500; y=100}
    )
    style = @{color="#FF0000"; width=3}
    coordinate_system = "pixel"
    return_image = $true
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/path/render" -Method Post -Headers $headers -Body $body
```

### 5. 运行测试

```bash
cd backend
venv\Scripts\activate
pip install pytest httpx
pytest tests/ -v
```

### 6. 不同端口启动

```bash
# 端口 80
start.bat 80

# 端口 443 (需要 SSL 证书)
set SSL_CERTFILE=path\to\cert.pem
set SSL_KEYFILE=path\to\key.pem
start.bat 443

# 自定义端口
start.bat 8080
```

### 7. 停止服务

在启动的终端窗口按 `Ctrl+C`

## 🔍 故障排除 (Troubleshooting)

### Python 未找到
```bash
# 下载安装 Python 3.10+
# https://www.python.org/downloads/
```

### 端口已占用
```bash
# 查看占用端口的进程
netstat -ano | findstr :8000

# 结束进程
taskkill /PID <进程ID> /F

# 或使用其他端口
start.bat 8080
```

### 依赖安装失败
```bash
cd backend
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 数据库问题
```bash
# 删除数据库文件重新开始
cd backend
del rscoutx.db
python seed_data.py
```

## 📚 更多信息

查看完整文档: [README.md](README.md)
