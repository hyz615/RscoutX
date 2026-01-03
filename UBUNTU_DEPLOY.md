# Ubuntu 部署快速指南

##  快速启动

### 1. 设置权限
```bash
chmod +x *.sh
```

### 2. 启动服务（后台运行）
```bash
sudo ./start_daemon.sh
```

### 3. 查看状态
```bash
./status.sh
```

### 4. 查看日志
```bash
tail -f logs/rscoutx.log
```

##  管理命令

- **启动**: `sudo ./start_daemon.sh`
- **停止**: `sudo ./stop.sh`
- **重启**: `sudo ./restart.sh`
- **状态**: `./status.sh`

##  访问地址

- 前端: http://your-server-ip/
- API 文档: http://your-server-ip/docs

##  systemd 服务（可选）

1. 编辑 `rscoutx.service` 修改路径
2. `sudo cp rscoutx.service /etc/systemd/system/`
3. `sudo systemctl enable rscoutx`
4. `sudo systemctl start rscoutx`

##  故障排查

**端口被占用:**
```bash
sudo lsof -i :80
sudo kill -9 <PID>
```

**查看完整日志:**
```bash
tail -f logs/rscoutx.log
```
