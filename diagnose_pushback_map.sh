#!/bin/bash
# 
# 快速修复指南: pushback_map.png 未找到
# ============================================

echo "🔍 诊断 pushback_map.png 问题..."
echo ""

# 1. 检查文件是否存在
if [ -f "pushback_map.png" ]; then
    echo "✅ [OK] pushback_map.png 已存在于根目录"
    ls -lh pushback_map.png
    echo ""
    echo "问题可能已解决,请尝试重启服务:"
    echo "  sudo ./stop.sh"
    echo "  sudo ./start_daemon.sh"
    exit 0
fi

echo "❌ [问题] pushback_map.png 不在根目录"
echo ""

# 2. 检查 frontend 目录
if [ -f "frontend/pushback_map.png" ]; then
    echo "✅ 找到 frontend/pushback_map.png"
    echo ""
    echo "修复选项:"
    echo "  [1] 自动复制 (推荐)"
    echo "  [2] 手动复制"
    echo "  [3] 取消"
    echo ""
    read -p "请选择 (1-3): " choice
    
    case $choice in
        1)
            echo ""
            echo "📋 正在复制文件..."
            cp frontend/pushback_map.png .
            if [ -f "pushback_map.png" ]; then
                echo "✅ 复制成功！"
                ls -lh pushback_map.png
                echo ""
                echo "现在可以启动服务:"
                echo "  sudo ./start_daemon.sh"
            else
                echo "❌ 复制失败"
            fi
            ;;
        2)
            echo ""
            echo "手动复制命令:"
            echo "  cp frontend/pushback_map.png ."
            ;;
        *)
            echo "已取消"
            ;;
    esac
else
    echo "❌ frontend/pushback_map.png 也不存在"
    echo ""
    echo "请确保:"
    echo "  1. 您在 RscoutX 项目根目录"
    echo "  2. frontend 目录存在"
    echo "  3. pushback_map.png 文件存在"
    echo ""
    echo "如果文件丢失,请从 Git 仓库重新克隆"
fi

echo ""
echo "更多帮助:"
echo "  - 运行完整检查: ./check_deploy.sh"
echo "  - 查看文档: cat FIX_PUSHBACK_MAP.md"
echo "  - 查看日志: tail -f logs/rscoutx.log"
