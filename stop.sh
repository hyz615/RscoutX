#!/bin/bash

# RscoutX Ubuntu 停止脚本

echo "🛑 停止 RscoutX 服务..."

# 检查 PID 文件是否存在
if [ ! -f "logs/rscoutx.pid" ]; then
    echo "⚠️  未找到 PID 文件，服务可能未运行"
    exit 1
fi

# 读取 PID
PID=$(cat logs/rscoutx.pid)

# 检查进程是否存在
if ! ps -p $PID > /dev/null 2>&1; then
    echo "⚠️  进程不存在 (PID: $PID)"
    rm logs/rscoutx.pid
    exit 1
fi

# 停止进程
echo "正在停止进程 (PID: $PID)..."
kill $PID

# 等待进程结束
for i in {1..10}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "✅ 服务已停止"
        rm logs/rscoutx.pid
        exit 0
    fi
    sleep 1
done

# 如果进程还在运行，强制杀死
echo "⚠️  正常停止失败，强制终止..."
kill -9 $PID
rm logs/rscoutx.pid
echo "✅ 服务已强制停止"
