# 驾驶员习惯标签功能 + AI 报告改进

## 更新日期
2026年1月2日

## 功能概述

### 1. 驾驶员习惯标签系统
为驾驶员习惯部分添加了标签（tag）功能，用户可以：
- 使用默认标签：`进攻`、`防守`、`最后20秒进攻`、`double park`
- 点击标签进行选择/取消选择（激活的标签会高亮显示）
- 添加自定义标签
- 删除自定义标签（默认标签不可删除）
- 标签数据自动保存到 LocalStorage

### 2. AI 报告生成改进
修改了 AI 报告生成逻辑，确保：
- AI 基于用户实际填写的机器人配置（类型、是否有机翼）进行分析
- AI 基于用户选择的驾驶员习惯标签进行分析
- AI 基于用户绘制的 Auton 路径数量和复杂度分析自动赛能力
- **不再输出"没有提供数据"或"缺乏信息"**等内容

## 前端修改 (frontend/index.html)

### HTML 结构
在驾驶员习惯部分添加：
```html
<!-- 习惯标签 -->
<div style="margin-bottom: 15px;">
    <div style="display: flex; gap: 10px; margin-bottom: 10px; align-items: center;">
        <label style="font-weight: 600; color: var(--text-dark);">习惯标签:</label>
        <input type="text" id="customTagInput" placeholder="输入自定义标签" 
            onkeypress="if(event.key === 'Enter') addCustomTag()">
        <button onclick="addCustomTag()">添加</button>
    </div>
    <div id="driverTags" style="display: flex; flex-wrap: wrap; gap: 8px;">
        <!-- 标签将动态添加到这里 -->
    </div>
</div>
```

### CSS 样式
添加标签样式：
- `.driver-tag` - 标签容器
- `.driver-tag.active` - 激活状态（蓝色高亮）
- `.tag-text` - 标签文本
- `.tag-remove` - 删除按钮（仅自定义标签显示）

### JavaScript 功能

#### 全局变量
```javascript
let driverTags = [];  // 当前选中的标签数组
const defaultTags = ['进攻', '防守', '最后20秒进攻', 'double park'];
```

#### 核心函数
1. `initializeDriverTags()` - 初始化标签系统（默认标签）
2. `renderDriverTags()` - 渲染所有标签到 DOM
3. `createTagElement(tagText, isDefault)` - 创建单个标签元素
4. `toggleTag(tagText)` - 切换标签选中状态
5. `addCustomTag()` - 添加自定义标签
6. `removeTag(tagText)` - 删除自定义标签

#### 数据持久化
- 标签数据保存在 `driverTags` 数组中
- 通过 `saveData()` 保存到 LocalStorage（键: `rscoutx_team_{teamId}`）
- 通过 `loadTeamDataFromStorage()` 加载标签数据
- `resetToDefaults()` 重置时清空标签

#### AI 导出集成
修改 `exportToAI()` 函数，在 `custom_context` 中包含标签信息：
```javascript
custom_context: `
机器人类型: ${selectedRobotType || '未选择'}
是否有机翼: ${hasWing ? '是 ✓' : '否'}
驾驶员习惯标签: ${driverTags.length > 0 ? driverTags.join(', ') : '无'}
驾驶员其他习惯: ${driverNotes || '无'}
Auton 数量: ${autons.length}
总路径点数: ${autons.reduce((sum, a) => sum + a.points.length, 0)}
...
`
```

## 后端修改

### 1. Schemas (backend/app/schemas/schemas.py)
在 `ReportRequest` 添加 `custom_context` 字段：
```python
class ReportRequest(BaseModel):
    team_id: int
    event_id: Optional[str] = None
    include_map: bool = True
    include_driver: bool = True
    include_robot: bool = True
    language: str = "zh"
    custom_context: Optional[str] = None  # 新增
```

### 2. API Routes (backend/app/api/routes/report.py)
传递 `custom_context` 到报告生成器：
```python
result = await generate_team_report(
    session=session,
    team_id=request.team_id,
    event_id=request.event_id,
    include_map=request.include_map,
    include_driver=request.include_driver,
    include_robot=request.include_robot,
    language=request.language,
    custom_context=request.custom_context  # 新增
)
```

### 3. Report Generator (backend/app/services/llm/report_generator.py)

#### 函数签名
添加 `custom_context` 参数：
```python
async def generate_team_report(
    session: Session,
    team_id: int,
    event_id: Optional[str] = None,
    include_map: bool = True,
    include_driver: bool = True,
    include_robot: bool = True,
    language: str = "zh",
    custom_context: Optional[str] = None  # 新增
) -> Dict[str, Any]:
```

#### 逻辑改进
- **优先使用 `custom_context`**：如果前端提供了 custom_context，直接使用它，不再查询数据库的 Robot 和 Driver 表
- **后备查询数据库**：如果没有 custom_context，才从数据库查询机器人和驾驶员信息
- **统一格式**：将 robot_info 和 driver_info 合并为 `combined_info`

### 4. Prompts (backend/app/prompts/report_prompts.py)

#### 系统提示词强化
在 `REPORT_SYSTEM_PROMPT_ZH` 中添加重要提示：
```python
**重要提示**：
- 用户已经提供了机器人配置信息（类型、是否有机翼等），请务必基于这些信息进行分析
- 用户已经提供了驾驶员习惯标签（如"进攻"、"防守"、"最后20秒进攻"、"double park"等），请针对这些习惯进行深入分析
- 用户已经绘制了自动赛程序路径图（Auton），请根据路径的数量和复杂度评估自动赛能力
- 绝对不要说"没有提供数据"或"缺乏信息"，而是要充分利用已提供的所有信息进行深入分析
```

#### 提示词模板简化
将 `robot_info` 和 `driver_info` 合并为 `combined_info`：
```python
REPORT_PROMPT_TEMPLATE_ZH = """...
## 战队信息
- 队号: {team_number}
- 队名: {team_name}
- 组织: {organization}
- 地区: {region}

{combined_info}

## 比赛统计
...
```

## 使用流程

### 用户操作
1. 搜索队伍（例如：16610A）
2. 在"机器人配置"部分选择机器人类型（如 sbot）和是否有机翼
3. 在"驾驶员习惯"部分：
   - 点击默认标签（进攻、防守等）进行选择
   - 输入自定义标签并点击"添加"按钮
   - 点击自定义标签上的 × 可删除
4. 绘制 Auton 路径
5. 点击"生成 AI 分析报告"

### 数据流
```
前端 → LocalStorage (自动保存)
前端 → API (/api/report/generate) 
    → custom_context 包含：
       - 机器人类型
       - 是否有机翼
       - 驾驶员习惯标签
       - Auton 数量和路径点数
后端 → OpenAI GPT-4o
    → 使用 custom_context 而非数据库数据
    → 生成针对性分析报告
```

## AI 报告改进效果

### 之前的问题
```markdown
## 2. 机器人配置分析
目前没有提供具体的机器人配置数据，因此无法进行详细分析。

## 3. 驾驶员习惯分析
由于缺乏具体的驾驶员信息，我们无法提供详细的驾驶员习惯分析。

## 7. 自动赛程序分析
没有提供自动赛程序的具体数据...
```

### 改进后
```markdown
## 2. 机器人配置分析
该队伍使用 sbot 类型机器人，配备机翼。sbot 具有良好的稳定性和推力，
配合机翼可以有效进行大范围推球操作...

## 3. 驾驶员习惯分析
根据标记的习惯标签：
- **进攻型打法**：该驾驶员倾向于主动进攻，积极推球得分
- **最后20秒进攻**：善于利用比赛末期进行最后冲刺
- **double park**：具备 double park 技巧，可在自动赛和手动赛获得额外分数

## 7. 自动赛程序分析
该队伍绘制了 3 条 Auton 路径，总计 45 个路径点，显示出较为复杂的
自动赛设计。路径数量充足，表明能够应对不同的场地位置和策略需求...
```

## 技术要点

### 1. 标签状态管理
- 默认标签始终显示，但可以选择/取消选择
- 自定义标签可以删除
- `driverTags` 数组只包含激活的标签名

### 2. 数据隔离
- 每个队伍的数据独立存储（`rscoutx_team_{teamId}`）
- 切换队伍时自动加载对应的标签数据

### 3. 自动保存
- 标签选择/取消选择触发 `triggerAutoSave()`
- 添加/删除自定义标签触发 `triggerAutoSave()`
- 1 秒防抖，避免频繁保存

### 4. AI 上下文优化
- 将所有用户输入的信息整合到 `custom_context`
- 后端优先使用 `custom_context`，确保 AI 基于用户实际操作进行分析
- 强化系统提示词，指导 AI 充分利用提供的信息

## 测试建议

1. **标签功能测试**
   - 点击默认标签，验证激活/取消状态
   - 添加自定义标签，验证显示和删除功能
   - 切换队伍，验证标签数据隔离

2. **数据持久化测试**
   - 选择标签后刷新页面，验证数据恢复
   - 切换队伍，验证不同队伍的标签独立

3. **AI 报告测试**
   - 选择机器人类型 + 标签 + 绘制 Auton
   - 生成 AI 报告，验证报告包含：
     - 机器人配置分析（基于选择的类型）
     - 驾驶员习惯分析（基于选择的标签）
     - 自动赛分析（基于绘制的路径）

## 已知限制

1. 默认标签是硬编码的中文，未来可以考虑国际化
2. 标签系统目前是纯前端实现，未同步到数据库
3. AI 分析质量依赖于 OpenAI API 的可用性和配置

## 未来改进方向

1. **标签预设管理**：允许用户自定义默认标签列表
2. **标签分类**：将标签分为"进攻风格"、"防守风格"、"特殊技巧"等类别
3. **数据库同步**：将标签数据同步到后端数据库
4. **标签推荐**：基于比赛数据自动推荐标签
5. **多语言支持**：支持中英文标签切换
