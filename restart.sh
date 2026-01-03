#!/bin/bash

# RscoutX Ubuntu 重启脚本

echo "🔄 重启 RscoutX 服务..."

# 停止服务
./stop.sh

# 等待 2 秒
sleep 2

# 启动服务
./start_daemon.sh

echo "✅ 重启完成"
