#!/bin/bash

# RscoutX Ubuntu 状态检查脚本

echo "📊 RscoutX 服务状态"
echo "===================="

# 检查 PID 文件
if [ ! -f "logs/rscoutx.pid" ]; then
    echo "状态: ❌ 未运行"
    echo "启动服务: sudo ./start_daemon.sh"
    exit 1
fi

# 读取 PID
PID=$(cat logs/rscoutx.pid)

# 检查进程是否存在
if ! ps -p $PID > /dev/null 2>&1; then
    echo "状态: ❌ 未运行 (PID 文件存在但进程不存在)"
    echo "清理: rm logs/rscoutx.pid"
    exit 1
fi

# 显示进程信息
echo "状态: ✅ 运行中"
echo "PID: $PID"
echo ""
echo "进程信息:"
ps -f -p $PID
echo ""
echo "内存使用:"
ps -o pid,vsz,rss,comm -p $PID
echo ""
echo "日志文件: logs/rscoutx.log"
echo "查看日志: tail -f logs/rscoutx.log"
