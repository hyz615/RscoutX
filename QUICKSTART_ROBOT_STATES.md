# 🚀 Quick Start - Robot State Feature

## 立即开始使用机器人状态可视化功能

### 1. 启动服务

```batch
REM 方式一：普通启动
start.bat

REM 方式二：调试模式（推荐，可以看到详细日志）
debug_backend.bat

REM 在另一个终端启动前端
cd frontend
python -m http.server 3000
```

### 2. 使用 Web UI 

1. 打开浏览器访问: **http://localhost:3000**
2. 点击顶部 **Map** 标签
3. 添加路径点：
   - 输入 X, Y 坐标
   - 选择 **Robot State** (可选)
     - 🔵 Idle - 待机
     - 🔵 Moving - 移动
     - 🟢 Intaking - 吸取三角球
     - 🟠 Wing Pushing - 推翼推球
     - 🟡 Releasing - 释放三角球
   - 点击 **Add Point**
4. 重复添加多个点
5. 点击 **Render Path** 查看结果

### 3. 使用 API 测试

```powershell
# PowerShell 快速测试
$body = @{
    method = "spline"
    coordinate_system = "pixel"
    points = @(
        @{ x=100; y=100; robot_state=@{state="idle"} },
        @{ x=200; y=200; robot_state=@{state="intaking"} },
        @{ x=300; y=300; robot_state=@{state="wingpushing"} },
        @{ x=400; y=400; robot_state=@{state="releasing"} }
    )
    style = @{
        color = "#FF0000"
        width = 3
        show_state_labels = $true
        state_icon_size = 20
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -OutFile "my_robot_path.png"

# 查看生成的图片
Start-Process "my_robot_path.png"
```

### 4. 运行完整测试

```powershell
# 自动测试所有功能
.\test_robot_states.ps1

# 这将生成 5 个测试图片:
# - test_path_polyline.png      (简单折线 + 状态)
# - test_path_bezier.png         (贝塞尔曲线 + 自定义颜色状态)
# - test_path_vex_match.png      (VEX 比赛模拟路径)
# - test_path_mixed.png          (混合：部分点有状态)
# - test_path_no_labels.png      (仅图标，无标签)
```

### 5. VEX 比赛场景示例

```python
# Python 完整比赛路径
import requests

match_strategy = {
    "method": "spline",
    "coordinate_system": "field",  # 场地坐标系 (mm)
    "points": [
        # 自动阶段开始
        {"x": 500, "y": 500, "robot_state": {"state": "idle"}},
        
        # 移动到第一个三角球
        {"x": 1200, "y": 800, "robot_state": {"state": "moving"}},
        
        # 吸取第一个球
        {"x": 1500, "y": 1000, "robot_state": {"state": "intaking"}},
        
        # 移动到推翼区
        {"x": 2000, "y": 1500, "robot_state": {"state": "moving"}},
        
        # 执行推翼动作
        {"x": 2500, "y": 2000, "robot_state": {"state": "wingpushing"}},
        
        # 移动到得分区
        {"x": 3000, "y": 2500, "robot_state": {"state": "moving"}},
        
        # 释放球
        {"x": 3200, "y": 2800, "robot_state": {"state": "releasing"}},
        
        # 返回待机位置
        {"x": 3000, "y": 3000, "robot_state": {"state": "idle"}}
    ],
    "style": {
        "color": "#FF0000",
        "width": 5,
        "arrow": True,
        "show_state_labels": True,
        "state_icon_size": 30
    }
}

response = requests.post(
    "http://localhost:8000/api/path/render/image",
    json=match_strategy
)

with open("vex_match_strategy.png", "wb") as f:
    f.write(response.content)

print("✓ Match strategy visualization saved!")
```

## 状态说明

| 状态 | 颜色 | 图标 | 用途 |
|------|-----|------|------|
| **idle** | 灰色 | ○ | 机器人待机或停止 |
| **moving** | 蓝色 | ● | 机器人正在移动（无特殊动作）|
| **intaking** | 绿色 | ⬇ | 机器人正在吸取三角球 |
| **wingpushing** | 橙红色 | ➤ | 机器人正在用推翼推球 |
| **releasing** | 金色 | ⬆ | 机器人正在释放/投放三角球 |

## 常见问题

### Q: 不想显示状态标签文字？
```javascript
"style": {
    "show_state_labels": false,  // 只显示图标
    "state_icon_size": 15
}
```

### Q: 想要更大的状态标记？
```javascript
"style": {
    "state_icon_size": 30  // 默认是 20
}
```

### Q: 可以自定义状态颜色吗？
```javascript
"robot_state": {
    "state": "intaking",
    "color": "#00FFFF"  // 自定义为青色
}
```

### Q: 可以部分点不加状态吗？
可以！只在关键点添加状态即可：
```javascript
"points": [
    {"x": 100, "y": 100},  // 无状态
    {"x": 200, "y": 200, "robot_state": {"state": "intaking"}},  // 有状态
    {"x": 300, "y": 300}   // 无状态
]
```

## API 端点

- **POST** `/api/path/render` - 返回 JSON (带 base64 图片)
- **POST** `/api/path/render/image` - 直接返回 PNG 图片

## 查看 API 文档

浏览器访问: **http://localhost:8000/api/docs**

在 Swagger UI 中可以交互式测试所有 API！

## 更多示例

查看完整文档: **ROBOT_STATE_FEATURE.md**

---

**祝你使用愉快！** 🎉

如果有问题，请查看:
- `ROBOT_STATE_FEATURE.md` - 完整功能文档
- `BUGFIX_SUMMARY.md` - 故障排查
- `WINDOWS_DEFENDER_FIX.md` - Windows Defender 问题
