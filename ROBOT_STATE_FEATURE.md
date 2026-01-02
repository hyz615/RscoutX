# 🤖 Robot State Visualization Feature

## 功能说明

在路径渲染时，支持标注机器人在不同路径点的状态，包括：
- **wingpushing** (推翼) - 橙红色 ➤
- **intaking** (吸取) - 绿色 ⬇
- **releasing** (释放) - 金色 ⬆
- **moving** (移动) - 蓝色 ●
- **idle** (待机) - 灰色 ○

## API 使用示例

### 1. 基础用法 - 带状态的路径点

```python
# Python
import requests

data = {
    "method": "spline",
    "coordinate_system": "pixel",
    "points": [
        {
            "x": 100,
            "y": 100,
            "robot_state": {
                "state": "idle"
            }
        },
        {
            "x": 200,
            "y": 150,
            "robot_state": {
                "state": "moving"
            }
        },
        {
            "x": 300,
            "y": 200,
            "robot_state": {
                "state": "intaking"
            }
        },
        {
            "x": 400,
            "y": 250,
            "robot_state": {
                "state": "wingpushing"
            }
        },
        {
            "x": 500,
            "y": 300,
            "robot_state": {
                "state": "releasing"
            }
        }
    ],
    "style": {
        "color": "#FF0000",
        "width": 3,
        "show_state_labels": True,
        "state_icon_size": 20
    }
}

response = requests.post("http://localhost:8000/api/path/render/image", json=data)
with open("path_with_states.png", "wb") as f:
    f.write(response.content)
```

### 2. PowerShell 示例

```powershell
$body = @{
    method = "bezier"
    coordinate_system = "pixel"
    points = @(
        @{
            x = 150
            y = 150
            robot_state = @{
                state = "idle"
            }
        },
        @{
            x = 250
            y = 200
            robot_state = @{
                state = "intaking"
                color = "#00FFFF"  # 自定义颜色
            }
        },
        @{
            x = 350
            y = 250
            robot_state = @{
                state = "wingpushing"
            }
        },
        @{
            x = 450
            y = 200
            robot_state = @{
                state = "releasing"
            }
        }
    )
    style = @{
        color = "#0000FF"
        width = 4
        show_state_labels = $true
        state_icon_size = 25
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -OutFile "robot_path.png"

echo "Path rendered with robot states saved to robot_path.png"
```

### 3. cURL 示例

```bash
curl -X POST "http://localhost:8000/api/path/render/image" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "polyline",
    "coordinate_system": "field",
    "points": [
      {
        "x": 500,
        "y": 500,
        "robot_state": {"state": "idle"}
      },
      {
        "x": 1000,
        "y": 1000,
        "robot_state": {"state": "moving"}
      },
      {
        "x": 1500,
        "y": 1500,
        "robot_state": {"state": "intaking"}
      },
      {
        "x": 2000,
        "y": 2000,
        "robot_state": {"state": "wingpushing"}
      },
      {
        "x": 2500,
        "y": 2500,
        "robot_state": {"state": "releasing"}
      }
    ],
    "style": {
      "color": "#FF00FF",
      "width": 5,
      "show_state_labels": true,
      "state_icon_size": 30
    }
  }' \
  --output vex_robot_path.png
```

## 状态颜色参考

| 状态 | 默认颜色 | 图标 | 说明 |
|------|---------|------|------|
| `wingpushing` | `#FF4500` (橙红) | ➤ | 机器人正在推翼推球 |
| `intaking` | `#00FF00` (绿色) | ⬇ | 机器人正在吸取三角球 |
| `releasing` | `#FFD700` (金色) | ⬆ | 机器人正在释放三角球 |
| `moving` | `#1E90FF` (蓝色) | ● | 机器人正在移动 |
| `idle` | `#808080` (灰色) | ○ | 机器人待机/停止 |

## 样式配置选项

```python
style = {
    "color": "#FF0000",           # 路径颜色
    "width": 3,                   # 路径宽度
    "opacity": 0.8,               # 路径透明度
    "arrow": True,                # 是否显示方向箭头
    "show_state_labels": True,    # 是否显示状态标签文字
    "state_icon_size": 20         # 状态图标大小(像素)
}
```

## 前端集成示例

### JavaScript

```javascript
async function renderPathWithStates() {
    const pathData = {
        method: 'spline',
        coordinate_system: 'pixel',
        points: [
            { x: 100, y: 100, robot_state: { state: 'idle' } },
            { x: 200, y: 200, robot_state: { state: 'intaking' } },
            { x: 300, y: 250, robot_state: { state: 'wingpushing' } },
            { x: 400, y: 300, robot_state: { state: 'releasing' } }
        ],
        style: {
            color: '#FF0000',
            width: 3,
            show_state_labels: true,
            state_icon_size: 25
        }
    };

    const response = await fetch('http://localhost:8000/api/path/render/image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pathData)
    });

    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);
    
    document.getElementById('pathImage').src = imageUrl;
}
```

### HTML 表单

```html
<div class="path-editor">
    <h3>Add Point with Robot State</h3>
    
    <label>X:</label>
    <input type="number" id="pointX" value="0">
    
    <label>Y:</label>
    <input type="number" id="pointY" value="0">
    
    <label>Robot State:</label>
    <select id="robotState">
        <option value="">None</option>
        <option value="idle">Idle (待机)</option>
        <option value="moving">Moving (移动)</option>
        <option value="intaking">Intaking (吸取)</option>
        <option value="wingpushing">Wing Pushing (推翼)</option>
        <option value="releasing">Releasing (释放)</option>
    </select>
    
    <button onclick="addPointWithState()">Add Point</button>
</div>

<script>
function addPointWithState() {
    const x = parseFloat(document.getElementById('pointX').value);
    const y = parseFloat(document.getElementById('pointY').value);
    const state = document.getElementById('robotState').value;
    
    const point = { x, y };
    if (state) {
        point.robot_state = { state };
    }
    
    pathPoints.push(point);
    updatePathList();
}
</script>
```

## 高级用法

### 自定义状态颜色

```javascript
{
    "x": 300,
    "y": 200,
    "robot_state": {
        "state": "intaking",
        "color": "#00FFFF"  // 自定义为青色
    }
}
```

### 不显示标签

```javascript
"style": {
    "show_state_labels": false,  // 只显示图标，不显示文字
    "state_icon_size": 15
}
```

### 混合使用（部分点有状态）

```javascript
"points": [
    { "x": 100, "y": 100 },  // 无状态
    { "x": 200, "y": 200, "robot_state": { "state": "intaking" } },  // 有状态
    { "x": 300, "y": 300 },  // 无状态
    { "x": 400, "y": 400, "robot_state": { "state": "releasing" } }  // 有状态
]
```

## 实战场景

### VEX Pushback 比赛路径

```python
# 完整的比赛策略路径
match_path = {
    "method": "spline",
    "coordinate_system": "field",  # 使用场地坐标 (mm)
    "points": [
        # 起点 - 待机
        {"x": 500, "y": 500, "robot_state": {"state": "idle"}},
        
        # 移动到第一个三角球
        {"x": 1200, "y": 800, "robot_state": {"state": "moving"}},
        
        # 吸取三角球
        {"x": 1500, "y": 1000, "robot_state": {"state": "intaking"}},
        
        # 移动到推翼区域
        {"x": 2000, "y": 1500, "robot_state": {"state": "moving"}},
        
        # 推翼推球
        {"x": 2500, "y": 2000, "robot_state": {"state": "wingpushing"}},
        
        # 移动到得分区
        {"x": 3000, "y": 2500, "robot_state": {"state": "moving"}},
        
        # 释放三角球
        {"x": 3200, "y": 2800, "robot_state": {"state": "releasing"}},
        
        # 返回待机
        {"x": 3000, "y": 3000, "robot_state": {"state": "idle"}}
    ],
    "style": {
        "color": "#FF0000",
        "width": 4,
        "arrow": True,
        "show_state_labels": True,
        "state_icon_size": 25
    }
}
```

## 可视化效果

渲染后的图片将显示：
1. **路径线** - 按照选择的方法绘制的平滑曲线
2. **状态标记** - 彩色圆圈表示机器人状态
3. **状态图标** - 图标指示具体动作
4. **状态标签** - 文字说明当前状态(可选)
5. **方向箭头** - 指示运动方向(可选)

## 数据结构

### PathPoint Schema
```python
class PathPoint(BaseModel):
    x: float                              # X 坐标
    y: float                              # Y 坐标
    t: Optional[float] = None            # 时间戳
    speed: Optional[float] = None        # 速度
    robot_state: Optional[RobotState] = None  # 机器人状态
```

### RobotState Schema
```python
class RobotState(BaseModel):
    state: str  # wingpushing/intaking/releasing/moving/idle
    color: Optional[str] = None  # 自定义颜色 (hex)
    icon: Optional[str] = None   # 自定义图标 (未来扩展)
```

### PathStyle Schema
```python
class PathStyle(BaseModel):
    color: str = "#FF0000"
    width: int = 3
    opacity: float = 0.8
    gradient: Optional[bool] = False
    arrow: Optional[bool] = False
    show_state_labels: bool = True       # NEW: 显示状态标签
    state_icon_size: int = 20           # NEW: 状态图标大小
```

## 注意事项

1. **坐标系统**: 
   - `pixel` - 直接使用像素坐标 (0-图片宽高)
   - `field` - 使用场地坐标 (mm, 0-3600)

2. **状态枚举**: 
   - 必须使用预定义的状态名称
   - 不区分大小写

3. **性能**: 
   - 状态标记会增加渲染时间
   - 建议在关键点添加状态，不是每个点都加

4. **可读性**: 
   - 建议 `state_icon_size` 在 15-30 之间
   - 点太多时可以关闭 `show_state_labels`

## 更新日志

**v1.1.0** - 2026-01-02
- ✨ 新增机器人状态可视化功能
- ✨ 支持 5 种预定义状态
- ✨ 支持自定义状态颜色
- ✨ 支持状态图标和文字标签
- ✨ 兼容所有渲染方法 (polyline/bezier/spline/astar/heatline)
