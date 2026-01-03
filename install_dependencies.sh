#!/bin/bash

# RscoutX Ubuntu 系统依赖安装脚本

echo "🔧 安装 RscoutX 系统依赖..."
echo ""

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 错误: 需要 root 权限"
    echo "请使用: sudo ./install_dependencies.sh"
    exit 1
fi

echo "📦 更新包列表..."
apt-get update

echo ""
echo "📦 安装 Python 和基础工具..."
apt-get install -y python3 python3-pip python3-venv python3-dev

echo ""
echo "📦 安装 OpenCV 依赖..."
echo "   (解决 libGL.so.1: cannot open shared object file 错误)"
apt-get install -y libgl1-mesa-glx libglib2.0-0

echo ""
echo "📦 安装编译工具..."
apt-get install -y build-essential gcc

echo ""
echo "✅ 系统依赖安装完成！"
echo ""
echo "Python 版本:"
python3 --version
echo ""
echo "下一步:"
echo "1. chmod +x *.sh"
echo "2. sudo ./start.sh"
