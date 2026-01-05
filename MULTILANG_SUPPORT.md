# 多语言支持说明 / Multi-language Support

## 📋 已完成的工作

### 1. 创建了 i18n.js 多语言支持文件
✅ **位置**: `frontend/i18n.js`

**功能**:
- 支持中文和英文切换
- 包含所有界面文本的翻译
- 自动保存用户语言偏好到 localStorage
- 提供简单的 API 供其他脚本使用

### 2. 添加了 CSS 样式
✅ 在 `frontend/index.html` 中添加了语言切换按钮的样式

```css
.lang-switch {
    position: absolute;
    top: 30px;
    right: 30px;
    display: flex;
    gap: 10px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 5px;
}

.lang-btn {
    padding: 8px 16px;
    border: none;
    background: transparent;
    color: white;
    cursor: pointer;
    border-radius: 15px;
    font-weight: bold;
    transition: all 0.3s;
}

.lang-btn.active {
    background: white;
    color: var(--primary);
}
```

### 3. 引入了 i18n.js 脚本
✅ 在 `</head>` 之前添加了:
```html
<script src="i18n.js"></script>
```

## 🔧 如何在 HTML 中使用多语言

### 方法 1: 使用 data-i18n 属性

```html
<!-- 文本内容 -->
<p data-i18n="header.subtitle">VEX Pushback 智能侦察与分析系统</p>

<!-- 按钮文本 -->
<button onclick="searchTeam()">
    <span data-i18n="search.button">🔎 搜索历史数据</span>
</button>

<!-- 标签文本 -->
<label data-i18n="search.teamNumber">队伍编号 Team Number</label>
```

### 方法 2: 输入框 placeholder

```html
<input type="text" 
       id="teamNumber" 
       data-i18n-placeholder="search.placeholder" 
       placeholder="例如: 1234A, 5678B, 9999C">
```

### 方法 3: 在 JavaScript 中使用

```javascript
// 获取翻译文本
const message = t('messages.searching');
showMessage(message, 'info');

// 在动态生成的内容中
element.innerHTML = `<h3>${t('teamInfo.recentMatches')}</h3>`;
```

## 📝 添加语言切换按钮

在 header 中添加:

```html
<div class="header">
    <div class="lang-switch">
        <button class="lang-btn active" onclick="switchLanguage('zh')" id="langZh">中文</button>
        <button class="lang-btn" onclick="switchLanguage('en')" id="langEn">English</button>
    </div>
    <h1>🤖 RscoutX</h1>
    <p data-i18n="header.subtitle">VEX Pushback 智能侦察与分析系统</p>
</div>
```

## 🌐 支持的翻译键

### Header
- `header.subtitle`

### Search Section
- `search.title`
- `search.teamNumber`
- `search.placeholder`
- `search.button`
- `search.hint`

### Team Info Section
- `teamInfo.title`
- `teamInfo.teamNumber`
- `teamInfo.teamName`
- `teamInfo.organization`
- `teamInfo.region`
- `teamInfo.eventCount`
- `teamInfo.totalMatches`
- `teamInfo.winRate`
- `teamInfo.avgScore`
- `teamInfo.maxScore`
- `teamInfo.autonScore`
- `teamInfo.recentMatches`

### Auton Section
- `auton.title`
- `auton.inputMode`
- `auton.clickInput`
- `auton.manualInput`
- `auton.renderMethod`
- `auton.polyline`
- `auton.bezier`
- `auton.spline`
- `auton.astar`
- `auton.heatline`
- `auton.coordinateSystem`
- `auton.pixel`
- `auton.field`
- `auton.pathStyle`
- `auton.color`
- `auton.width`
- `auton.opacity`
- `auton.arrow`
- `auton.xCoord`
- `auton.yCoord`
- `auton.addPoint`
- `auton.clearPoints`
- `auton.renderPath`
- `auton.exportPath`
- `auton.robotState`
- `auton.pointsCounter`
- `auton.mapNotFound`

### Driver Section
- `driver.title`
- `driver.hint`
- `driver.addHabit`

### AI Export Section
- `aiExport.title`
- `aiExport.hint`
- `aiExport.generateReport`
- `aiExport.copyJson`
- `aiExport.copyMarkdown`
- `aiExport.preview`

### Messages
- `messages.searching`
- `messages.teamNotFound`
- `messages.loadingMatches`
- `messages.matchesLoaded`
- `messages.noMatches`
- `messages.pointAdded`
- `messages.invalidCoords`
- `messages.pointsCleared`
- `messages.rendering`
- `messages.renderSuccess`
- `messages.renderError`
- `messages.copied`
- `messages.copyFailed`
- `messages.generating`
- `messages.reportGenerated`

## 🔨 完整实现步骤

### 步骤 1: 在所有需要翻译的 HTML 元素上添加 data-i18n 属性

```html
<!-- 之前 -->
<div class="section-title">
    🔍 队伍搜索
</div>

<!-- 之后 -->
<div class="section-title">
    <span data-i18n="search.title">🔍 队伍搜索</span>
</div>
```

### 步骤 2: 更新 JavaScript 中的消息

```javascript
// 之前
showMessage('正在搜索队伍信息...', 'info');

// 之后
showMessage(t('messages.searching'), 'info');
```

### 步骤 3: 测试语言切换

1. 打开页面
2. 点击右上角的 "English" 按钮
3. 检查所有文本是否正确切换
4. 刷新页面,确认语言偏好被保存

## 📦 文件清单

新增文件:
- ✅ `frontend/i18n.js` - 多语言支持核心文件
- ✅ `MULTILANG_SUPPORT.md` - 本说明文档

修改文件:
- ✅ `frontend/index.html` - 添加语言切换按钮样式和 i18n.js 引用

## 🎯 下一步

如需完全启用多语言,需要:

1. **在 index.html 中添加 data-i18n 属性**
   - 给所有标题、标签、按钮添加 `data-i18n` 属性
   - 给输入框添加 `data-i18n-placeholder` 属性

2. **更新 JavaScript 消息**
   - 将所有 `showMessage()` 调用改为使用 `t()` 函数

3. **添加语言切换按钮**
   - 在 header 中添加语言切换按钮 HTML

## 💡 快速测试

创建一个简单的测试页面:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>i18n Test</title>
    <script src="i18n.js"></script>
    <style>
        .lang-btn { padding: 10px; margin: 5px; cursor: pointer; }
        .lang-btn.active { background: #667eea; color: white; }
    </style>
</head>
<body>
    <button class="lang-btn active" onclick="switchLanguage('zh')" id="langZh">中文</button>
    <button class="lang-btn" onclick="switchLanguage('en')" id="langEn">English</button>
    
    <h1 data-i18n="header.subtitle">VEX Pushback 智能侦察与分析系统</h1>
    <p data-i18n="search.hint">💡 将自动加载该队伍在所有赛事中的历史数据和统计信息</p>
    
    <script>
        console.log('Current language:', currentLang);
        console.log('Search title:', t('search.title'));
    </script>
</body>
</html>
```

## ✨ 优势

1. **简单易用**: 只需添加 `data-i18n` 属性
2. **自动保存**: 语言偏好保存到 localStorage
3. **即时切换**: 无需刷新页面
4. **易于扩展**: 添加新语言只需在 `translations` 对象中添加新条目
5. **向后兼容**: 默认显示中文,不影响现有功能

## 🌍 添加更多语言

在 `i18n.js` 中添加新语言:

```javascript
const translations = {
    zh: { /* 中文翻译 */ },
    en: { /* 英文翻译 */ },
    ja: { /* 日语翻译 */ },  // 新增
    ko: { /* 韩语翻译 */ }   // 新增
};
```

然后添加相应的切换按钮即可。
