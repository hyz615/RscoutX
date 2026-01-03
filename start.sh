#!/bin/bash

# RscoutX Ubuntu 启动脚本 - 80 端口
# 需要 root 权限运行

echo "🚀 启动 RscoutX 服务..."

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 错误: 需要 root 权限来使用 80 端口"
    echo "请使用: sudo ./start.sh"
    exit 1
fi

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

# 进入 backend 目录
cd backend || exit 1

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 安装/更新依赖
echo "📥 安装依赖..."
venv/bin/pip install -r requirements.txt

# 启动服务
echo "✅ 在 80 端口启动服务..."
echo "访问地址: http://localhost/"
echo "API 文档: http://localhost/docs"
echo ""
echo "按 Ctrl+C 停止服务"

venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
