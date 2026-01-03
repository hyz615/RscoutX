#!/bin/bash

# 修复 pushback_map.png 文件位置

echo "🔧 修复 pushback_map.png 文件位置..."
echo ""

# 检查根目录是否已有文件
if [ -f "pushback_map.png" ]; then
    echo "✅ pushback_map.png 已存在于根目录"
    ls -lh pushback_map.png
    exit 0
fi

# 从 frontend 复制
if [ -f "frontend/pushback_map.png" ]; then
    echo "📋 从 frontend 目录复制 pushback_map.png 到根目录..."
    cp frontend/pushback_map.png .
    if [ -f "pushback_map.png" ]; then
        echo "✅ 复制成功！"
        ls -lh pushback_map.png
    else
        echo "❌ 复制失败"
        exit 1
    fi
else
    echo "❌ 错误: frontend/pushback_map.png 不存在"
    echo ""
    echo "请确保 pushback_map.png 文件存在于以下任一位置:"
    echo "  - 项目根目录"
    echo "  - frontend 目录"
    exit 1
fi

echo ""
echo "✅ 完成！现在可以启动服务了:"
echo "   sudo ./start_daemon.sh"
