# 修复脚本使用说明

本目录包含多个用于诊断和修复 `pushback_map.png` 问题的脚本。

## 📝 脚本列表

### 1. `test_map_access.sh` - 地图访问测试（推荐首先运行）
**用途**: 全面测试地图文件是否可以被正确访问
**特点**: 
- 检查文件存在性
- 测试 Python 加载
- 测试 HTTP 访问
- 提供详细诊断信息

**使用方法**:
```bash
chmod +x test_map_access.sh
./test_map_access.sh
```

### 2. `diagnose_pushback_map.sh` - 交互式诊断工具
**用途**: 诊断并提供修复选项
**特点**: 
- 交互式界面
- 自动检测问题
- 提供多种修复方案

**使用方法**:
```bash
chmod +x diagnose_pushback_map.sh
./diagnose_pushback_map.sh
```

### 3. `fix_pushback_map.sh` - 自动修复脚本
**用途**: 自动复制地图文件到根目录
**特点**:
- 无需交互
- 自动执行
- 适合脚本调用

**使用方法**:
```bash
chmod +x fix_pushback_map.sh
./fix_pushback_map.sh
```

### 4. `check_deploy.sh` - 完整部署检查
**用途**: 检查所有部署相关问题
**特点**:
- 全面检查
- 包含系统依赖
- 包含地图文件检查

**使用方法**:
```bash
chmod +x check_deploy.sh
./check_deploy.sh
```

## 🚀 快速开始

### 情况 1: 首次部署
```bash
# 1. 检查环境
./check_deploy.sh

# 2. 如果提示地图文件问题,运行修复
./fix_pushback_map.sh

# 3. 启动服务
sudo ./start_daemon.sh

# 4. 测试地图访问
./test_map_access.sh
```

### 情况 2: 服务已启动但地图不显示
```bash
# 1. 测试地图访问（查看详细诊断）
./test_map_access.sh

# 2. 如果文件不存在,运行修复
./fix_pushback_map.sh

# 3. 重启服务
sudo ./stop.sh
sudo ./start_daemon.sh

# 4. 再次测试
./test_map_access.sh
```

### 情况 3: 不确定是否有问题
```bash
# 运行交互式诊断
./diagnose_pushback_map.sh
```

## 🔍 问题排查流程

```
┌─────────────────────────────┐
│ pushback_map.png 是否存在?  │
└──────────┬──────────────────┘
           │
    ┌──────┴──────┐
    │             │
   是            否
    │             │
    ▼             ▼
  [OK]    frontend/ 中是否存在?
                    │
             ┌──────┴──────┐
             │             │
            是            否
             │             │
             ▼             ▼
      运行 fix_pushback_map.sh   从仓库重新克隆
```

## 📋 验证修复

修复后,验证是否成功:

```bash
# 1. 检查文件是否存在
ls -lh pushback_map.png

# 2. 启动服务
sudo ./start_daemon.sh

# 3. 查看日志
tail -f logs/rscoutx.log

# 应该看到:
# ✅ 找到地图文件: /path/to/RscoutX/pushback_map.png
```

## 🆘 仍然有问题?

如果问题仍然存在:

1. **查看详细日志**:
   ```bash
   tail -100 logs/rscoutx.log
   ```

2. **检查文件权限**:
   ```bash
   ls -la pushback_map.png
   # 应该可读: -rw-r--r--
   ```

3. **手动测试 Python 加载**:
   ```bash
   cd backend
   source venv/bin/activate
   python3 -c "from PIL import Image; img = Image.open('../pushback_map.png'); print('OK')"
   ```

4. **查看详细文档**:
   ```bash
   cat FIX_PUSHBACK_MAP.md
   ```

## 📚 相关文档

- `FIX_PUSHBACK_MAP.md` - 完整的修复说明和技术细节
- `UBUNTU_DEPLOY.md` - Ubuntu/Linux 部署指南
- `README.md` - 项目主文档(包含故障排查章节)

## 💡 提示

- 所有脚本都需要在项目根目录运行
- 部分脚本需要 sudo 权限
- 建议先运行 `check_deploy.sh` 了解整体状态
- 使用 `diagnose_pushback_map.sh` 获得交互式帮助
