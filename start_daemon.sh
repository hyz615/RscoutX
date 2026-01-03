#!/bin/bash

# RscoutX Ubuntu 后台守护进程启动脚本 - 80 端口
# 需要 root 权限运行

echo "🚀 启动 RscoutX 后台服务..."

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 错误: 需要 root 权限来使用 80 端口"
    echo "请使用: sudo ./start_daemon.sh"
    exit 1
fi

# 创建日志目录
mkdir -p logs

# 检查是否已经在运行
if [ -f "logs/rscoutx.pid" ]; then
    PID=$(cat logs/rscoutx.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️  服务已在运行 (PID: $PID)"
        echo "如需重启，请先运行: sudo ./stop.sh"
        exit 1
    else
        rm logs/rscoutx.pid
    fi
fi

# 进入 backend 目录
cd backend || exit 1

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 安装依赖
echo "🔧 安装依赖..."
venv/bin/pip install -r requirements.txt > /dev/null 2>&1

# 启动后台进程
echo "🚀 启动后台进程..."
nohup venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 80 > ../logs/rscoutx.log 2>&1 &

# 保存 PID
echo $! > ../logs/rscoutx.pid

cd ..

echo "✅ 服务已在后台启动"
echo "PID: $(cat logs/rscoutx.pid)"
echo "日志文件: logs/rscoutx.log"
echo ""
echo "查看日志: tail -f logs/rscoutx.log"
echo "停止服务: sudo ./stop.sh"
echo "查看状态: ./status.sh"
