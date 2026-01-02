# 🗺️ 地图文件放置指南

## 问题说明

Auton 路径绘制区域需要显示 VEX Pushback 场地地图（`pushback_map.png`），但可能因为路径问题无法加载。

## ✅ 解决方案

### 方法 1: 复制到 frontend 目录（推荐）

```bash
# 在项目根目录执行
copy pushback_map.png frontend\pushback_map.png
```

### 方法 2: 保持在根目录（使用相对路径）

确保 `pushback_map.png` 在项目根目录，系统会自动尝试多个路径：
1. `./pushback_map.png`
2. `../pushback_map.png`
3. `/pushback_map.png`
4. `pushback_map.png`

## 📁 推荐的文件结构

```
RscoutX/
├── pushback_map.png          ← 原始文件
├── frontend/
│   ├── pushback_map.png      ← 复制到这里（推荐）
│   ├── index_new.html
│   ├── app.js
│   └── styles.css
├── backend/
└── start.bat
```

## 🔍 验证方法

### 1. 打开浏览器开发者工具

按 `F12` 打开控制台，查看日志：

**成功加载：**
```
✓ Map loaded from: ./pushback_map.png
```

**加载失败：**
```
✗ Failed to load from: ./pushback_map.png
✗ Failed to load from: ../pushback_map.png
✗ Failed to load from: /pushback_map.png
✗ Failed to load from: pushback_map.png
⚠️ Could not load pushback_map.png from any path, using default grid
```

### 2. 检查显示效果

**地图成功加载：**
- 显示实际的 VEX Pushback 场地图片
- 可以在真实场地上绘制路径

**地图加载失败（使用默认网格）：**
- 显示黑色背景 + 灰色网格
- 红色边框标记场地范围
- 中心十字线
- 提示文字："pushback_map.png 未找到 - 使用默认网格"

## 🚀 快速修复步骤

1. **确认文件存在**：
```bash
# 检查根目录
dir pushback_map.png

# 如果不存在，请添加该文件
```

2. **复制到 frontend 目录**：
```bash
copy pushback_map.png frontend\pushback_map.png
```

3. **刷新页面**：
```
按 Ctrl+F5 强制刷新浏览器
```

4. **检查控制台**：
- 打开 F12 开发者工具
- 查看 Console 标签
- 确认看到 "✓ Map loaded from: ..." 消息

## 📝 地图文件要求

### 文件规格：
- **文件名**: `pushback_map.png`（必须完全匹配）
- **格式**: PNG 或 JPG
- **推荐尺寸**: 800x800 像素或更大
- **内容**: VEX V5 Pushback 场地俯视图

### 如果没有地图文件：

**选项 1: 使用默认网格**
- 系统会自动显示网格布局
- 仍可正常绘制路径点

**选项 2: 下载场地图**
- 从 VEX 官方网站下载 Pushback 场地图
- 保存为 `pushback_map.png`
- 放置到 `frontend/` 目录

**选项 3: 创建自定义地图**
- 使用任何图像编辑软件
- 绘制 3600mm x 3600mm 的场地布局
- 导出为 PNG 格式

## 🎨 增强的默认网格

如果地图文件未找到，新版本会显示更好的默认网格：

✅ **特性**：
- 深色背景（#1a1a1a）
- 50px 间隔的网格线
- 红色场地边界
- 中心十字线
- 友好的提示文字
- 仍可正常使用所有绘制功能

## 🔧 故障排除

### 问题 1: 地图不显示
**解决**：
1. 检查文件名拼写（区分大小写）
2. 确认文件格式（PNG/JPG）
3. 复制到 `frontend/` 目录
4. 清除浏览器缓存（Ctrl+Shift+Delete）

### 问题 2: 地图显示但很模糊
**解决**：
1. 使用高分辨率图片（至少 800x800）
2. 确保图片未被压缩
3. 使用 PNG 格式保持清晰度

### 问题 3: 路径点位置不准确
**解决**：
1. 确保地图是正方形（1:1 比例）
2. 地图应该填满整个 Canvas
3. 使用标准 VEX 场地尺寸（3600mm x 3600mm）

## 📊 技术细节

### Canvas 尺寸：
- 宽度: 800px
- 高度: 800px
- 坐标系: 左上角 (0,0) 到右下角 (800,800)

### 地图加载逻辑：
```javascript
// 尝试 4 个可能的路径
possiblePaths = [
    './pushback_map.png',    // 同级目录
    '../pushback_map.png',   // 父级目录
    '/pushback_map.png',     // 服务器根目录
    'pushback_map.png'       // 相对当前目录
]

// 按顺序尝试，第一个成功的就使用
// 全部失败则显示默认网格
```

## ✨ 更新内容

**新增功能**：
- ✅ 多路径自动尝试
- ✅ 控制台日志提示
- ✅ 增强的默认网格显示
- ✅ 更友好的错误提示

---

**快速命令**：
```bash
# 一键复制地图文件
copy pushback_map.png frontend\pushback_map.png

# 启动服务
.\start.bat

# 打开浏览器
start http://localhost:3000/index_new.html
```

现在地图应该能正常显示了！🎉
