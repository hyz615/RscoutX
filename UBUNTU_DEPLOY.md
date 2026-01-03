# Ubuntu 部署快速指南

## 📋 系统要求

- Ubuntu 18.04+ / Debian 10+
- Python 3.8+
- Root 权限（用于 80 端口）

##  快速启动

### 0. 检查项目结构（重要！）
```bash
# 确保项目结构正确
ls -la
# 必须包含以下文件和目录:
# - backend/           # 后端代码
# - frontend/          # 前端代码
# - pushback_map.png   # 场地地图（必须在根目录）
# - *.sh               # 启动脚本

# 如果 pushback_map.png 不存在，请从 frontend 目录复制
if [ ! -f "pushback_map.png" ]; then
    cp frontend/pushback_map.png . 2>/dev/null || echo "警告: pushback_map.png 未找到"
fi
```

### 1. 安装系统依赖（重要！）
```bash
# 方式 A: 使用一键安装脚本（推荐）
chmod +x install_dependencies.sh
sudo ./install_dependencies.sh

# 方式 B: 手动安装
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv python3-dev
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
sudo apt-get install -y build-essential gcc
```

### 2. 设置权限
```bash
chmod +x *.sh
```

### 3. 验证部署环境（可选但推荐）
```bash
./check_deploy.sh
```
这会检查所有依赖和项目结构是否正确。

### 4. 启动服务（后台运行）
```bash
sudo ./start_daemon.sh
```

### 5. 查看状态
```bash
./status.sh
```

### 6. 查看日志
```bash
tail -f logs/rscoutx.log
```

##  管理命令

- **启动**: `sudo ./start_daemon.sh`
- **停止**: `sudo ./stop.sh`
- **重启**: `sudo ./restart.sh`
- **状态**: `./status.sh`

##  访问地址

- **前端界面**: http://your-server-ip/
- **API 文档**: http://your-server-ip/api/v1/docs
- **健康检查**: http://your-server-ip/api/v1/health

> 注意：确保 frontend 文件夹和 backend 文件夹在同一目录下

## 🧪 测试安装

在启动前，可以先测试虚拟环境：

```bash
cd backend
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/uvicorn --version
```

如果看到版本号，说明安装成功！

##  systemd 服务（可选）

1. 编辑 `rscoutx.service` 修改路径
2. `sudo cp rscoutx.service /etc/systemd/system/`
3. `sudo systemctl enable rscoutx`
4. `sudo systemctl start rscoutx`

##  故障排查

**访问根路径显示 API 而不是前端界面:**
```bash
# 检查项目结构，frontend 和 backend 应该在同一层
ls -la
# 应该看到:
# - frontend/
# - backend/
# - start.sh

# 检查 frontend 目录是否存在 index.html
ls frontend/index.html

# 如果 frontend 不存在或位置不对，需要调整项目结构
```

**libGL.so.1: cannot open shared object file 错误:**
```bash
# 这是最常见的错误！安装 OpenCV 系统依赖
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0

# 或者运行一键安装脚本
sudo ./install_dependencies.sh
```

**端口被占用:**
```bash
sudo lsof -i :80
sudo kill -9 <PID>
```

**uvicorn: command not found 错误:**
```bash
# 确保在 backend 目录下
cd backend

# 手动安装依赖
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# 验证安装
venv/bin/uvicorn --version
```

**权限问题:**
```bash
# 必须使用 sudo 运行（80 端口需要 root 权限）
sudo ./start.sh
```

**查看完整日志:**
```bash
tail -f logs/rscoutx.log
```

**依赖安装失败:**
```bash
# 安装系统依赖
sudo apt-get update
sudo apt-get install python3-dev python3-pip python3-venv build-essential
```
