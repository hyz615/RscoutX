#!/bin/bash

# 测试 pushback_map.png 文件访问

echo "🔍 测试 pushback_map.png 访问"
echo "=============================="
echo ""

# 1. 检查文件是否存在
echo "1️⃣  检查文件是否存在..."
if [ -f "pushback_map.png" ]; then
    echo "   ✅ pushback_map.png 存在于根目录"
    ls -lh pushback_map.png
else
    echo "   ❌ pushback_map.png 不在根目录"
    if [ -f "frontend/pushback_map.png" ]; then
        echo "   ⚠️  但存在于 frontend 目录"
        echo "   💡 建议运行: ./fix_pushback_map.sh"
    fi
fi
echo ""

# 2. 测试 Python 能否加载
echo "2️⃣  测试 Python PIL 能否加载..."
if [ -f "backend/venv/bin/python3" ]; then
    if [ -f "pushback_map.png" ]; then
        backend/venv/bin/python3 << 'EOF'
try:
    from PIL import Image
    import os
    
    # Test loading from root
    img = Image.open('pushback_map.png')
    print(f"   ✅ Python 成功加载 pushback_map.png")
    print(f"   📐 尺寸: {img.size[0]}x{img.size[1]}")
    print(f"   🎨 模式: {img.mode}")
    
    # Test absolute path
    abs_path = os.path.abspath('pushback_map.png')
    print(f"   📍 绝对路径: {abs_path}")
except Exception as e:
    print(f"   ❌ Python 加载失败: {e}")
EOF
    else
        echo "   ⏭️  跳过 (文件不存在)"
    fi
else
    echo "   ⏭️  跳过 (虚拟环境不存在)"
fi
echo ""

# 3. 测试后端是否运行
echo "3️⃣  检查后端服务..."
if [ -f "logs/rscoutx.pid" ]; then
    PID=$(cat logs/rscoutx.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   ✅ 后端服务正在运行 (PID: $PID)"
        
        # Wait a moment for service to be ready
        sleep 1
        
        # Test HTTP access
        echo ""
        echo "4️⃣  测试 HTTP 访问..."
        
        # Try different ports
        for PORT in 80 8000; do
            echo "   测试端口 $PORT..."
            
            # Test map endpoint
            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/pushback_map.png 2>/dev/null)
            if [ "$HTTP_CODE" = "200" ]; then
                echo "      ✅ /pushback_map.png 可访问 (HTTP $HTTP_CODE)"
                
                # Get file info
                SIZE=$(curl -s -I http://localhost:$PORT/pushback_map.png 2>/dev/null | grep -i content-length | awk '{print $2}' | tr -d '\r')
                if [ ! -z "$SIZE" ]; then
                    SIZE_KB=$((SIZE / 1024))
                    echo "      📦 大小: ${SIZE_KB} KB"
                fi
            elif [ "$HTTP_CODE" = "000" ]; then
                echo "      ⚠️  无法连接到端口 $PORT"
            else
                echo "      ❌ /pushback_map.png 返回 HTTP $HTTP_CODE"
            fi
            
            # Test API health
            HEALTH=$(curl -s http://localhost:$PORT/api/health 2>/dev/null)
            if [ ! -z "$HEALTH" ]; then
                echo "      ✅ API 健康检查通过"
            fi
        done
    else
        echo "   ⚠️  PID 文件存在但服务未运行"
    fi
else
    echo "   ⚠️  后端服务未运行"
    echo "   💡 启动服务: sudo ./start_daemon.sh"
fi

echo ""
echo "=============================="
echo "📋 摘要"
echo ""

# Summary
if [ -f "pushback_map.png" ]; then
    echo "✅ 文件存在"
else
    echo "❌ 文件不存在 - 运行 ./fix_pushback_map.sh"
    exit 1
fi

if [ -f "logs/rscoutx.pid" ]; then
    PID=$(cat logs/rscoutx.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ 服务运行中"
        
        # Quick test
        for PORT in 80 8000; do
            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/pushback_map.png 2>/dev/null)
            if [ "$HTTP_CODE" = "200" ]; then
                echo "✅ HTTP 访问正常 (端口 $PORT)"
                echo ""
                echo "🌐 前端访问地址:"
                echo "   http://localhost:$PORT/"
                exit 0
            fi
        done
        
        echo "⚠️  HTTP 访问异常 - 检查日志: tail -f logs/rscoutx.log"
    else
        echo "❌ 服务未运行 - 启动: sudo ./start_daemon.sh"
    fi
else
    echo "❌ 服务未运行 - 启动: sudo ./start_daemon.sh"
fi

echo ""
echo "💡 需要帮助? 运行: ./diagnose_pushback_map.sh"
