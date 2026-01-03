#!/bin/bash

# RscoutX 部署验证脚本

echo "🔍 RscoutX 部署检查"
echo "===================="
echo ""

# 检查项目结构
echo "📁 检查项目结构..."
if [ -d "frontend" ]; then
    echo "  ✅ frontend 目录存在"
    if [ -f "frontend/index.html" ]; then
        echo "  ✅ frontend/index.html 存在"
    else
        echo "  ❌ frontend/index.html 不存在"
    fi
else
    echo "  ❌ frontend 目录不存在"
fi

if [ -d "backend" ]; then
    echo "  ✅ backend 目录存在"
else
    echo "  ❌ backend 目录不存在"
fi

# 检查场地地图文件
if [ -f "pushback_map.png" ]; then
    echo "  ✅ pushback_map.png 存在（根目录）"
else
    echo "  ⚠️  pushback_map.png 不存在（根目录）"
    if [ -f "frontend/pushback_map.png" ]; then
        echo "     💡 提示: 可以从 frontend 目录复制: cp frontend/pushback_map.png ."
    else
        echo "     ❌ frontend/pushback_map.png 也不存在"
    fi
fi

echo ""

# 检查 Python
echo "🐍 检查 Python..."
if command -v python3 &> /dev/null; then
    echo "  ✅ Python 3 已安装: $(python3 --version)"
else
    echo "  ❌ Python 3 未安装"
fi

echo ""

# 检查系统依赖
echo "📦 检查系统依赖..."
if ldconfig -p | grep libGL.so.1 > /dev/null 2>&1; then
    echo "  ✅ libGL.so.1 已安装"
else
    echo "  ❌ libGL.so.1 未安装 (需要: sudo apt-get install -y libgl1-mesa-glx)"
fi

if ldconfig -p | grep libglib-2.0.so > /dev/null 2>&1; then
    echo "  ✅ libglib-2.0 已安装"
else
    echo "  ❌ libglib-2.0 未安装 (需要: sudo apt-get install -y libglib2.0-0)"
fi

echo ""

# 检查虚拟环境
echo "🔧 检查虚拟环境..."
if [ -d "backend/venv" ]; then
    echo "  ✅ 虚拟环境已创建"
    if [ -f "backend/venv/bin/uvicorn" ]; then
        echo "  ✅ uvicorn 已安装"
        backend/venv/bin/uvicorn --version
    else
        echo "  ❌ uvicorn 未安装"
    fi
else
    echo "  ⚠️  虚拟环境未创建 (运行 start.sh 会自动创建)"
fi

echo ""

# 检查服务状态
echo "🚀 检查服务状态..."
if [ -f "logs/rscoutx.pid" ]; then
    PID=$(cat logs/rscoutx.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "  ✅ 服务正在运行 (PID: $PID)"
    else
        echo "  ⚠️  PID 文件存在但服务未运行"
    fi
else
    echo "  ⚠️  服务未运行"
fi

echo ""
echo "===================="
echo "💡 下一步:"
echo ""
echo "1. 如果有 ❌ 错误，请先解决:"
echo "   sudo ./install_dependencies.sh"
echo ""
echo "2. 启动服务:"
echo "   sudo ./start_daemon.sh"
echo ""
echo "3. 访问应用:"
echo "   http://your-server-ip/"
echo "   http://your-server-ip/api/v1/docs"
