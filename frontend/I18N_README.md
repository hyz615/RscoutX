# 国际化功能说明文档

## 📚 功能概述

RscoutX 现已支持中英双语界面切换功能，用户可以通过界面右上角的语言切换按钮在中文和英文之间自由切换。

## 🎯 实现方式

### 1. 核心文件

- **`i18n.js`**: 国际化核心库
  - 包含完整的中英文翻译文本
  - 提供语言切换和文本翻译功能
  - 支持 localStorage 持久化保存用户语言偏好

- **`i18n-helper.js`**: 辅助脚本
  - 自动更新页面动态内容
  - 处理复杂 UI 元素的翻译
  - 监听语言变化事件

### 2. 使用方法

#### 在 HTML 中使用 data-i18n 属性

```html
<!-- 基本文本翻译 -->
<h1 data-i18n="title">默认文本</h1>

<!-- placeholder 翻译 -->
<input data-i18n-placeholder="team_number" placeholder="默认占位符">

<!-- title 属性翻译 -->
<button data-i18n-title="btn_delete" title="默认提示">删除</button>
```

#### 在 JavaScript 中使用

```javascript
// 获取翻译文本
const text = i18n.t('team_number');

// 切换语言
i18n.setLanguage('en'); // 或 'zh'

// 获取当前语言
const currentLang = i18n.getLanguage();

// 监听语言变化
window.addEventListener('languageChanged', (e) => {
    console.log('Language changed to:', e.detail.language);
    // 执行自定义更新逻辑
});
```

### 3. 语言切换按钮

页面右上角提供了语言切换按钮：
- 🇨🇳 中文
- 🇺🇸 English

点击按钮即可立即切换界面语言，选择会自动保存到浏览器本地存储。

## 📝 翻译文本管理

### 添加新的翻译文本

编辑 `i18n.js` 文件中的 `translations` 对象：

```javascript
const translations = {
    zh: {
        // 添加中文翻译
        new_key: "新文本",
    },
    en: {
        // 添加英文翻译
        new_key: "New Text",
    }
};
```

### 当前已支持的翻译项

- **Header**: 标题、副标题
- **Navigation**: 导航菜单项
- **Dashboard**: 仪表板相关文本
- **Map**: 地图渲染相关文本
- **Admin**: 机器人和驾驶员管理
- **Report**: 报告生成相关
- **Messages**: 提示信息
- **Common**: 通用按钮和标签

## 🔧 技术细节

### 自动初始化

页面加载时会自动：
1. 从 localStorage 读取用户上次选择的语言
2. 如果没有保存的语言偏好，默认使用中文
3. 更新所有带 `data-i18n` 属性的元素
4. 更新页面标题和 HTML lang 属性

### 语言持久化

用户选择的语言会保存到 localStorage，key 为 `rscoutx_language`，下次访问时会自动应用之前的语言选择。

### 动态内容更新

对于通过 JavaScript 动态生成的内容，`i18n-helper.js` 提供了 `updateDynamicContent()` 函数来更新这些元素。

## 🎨 样式定制

语言切换按钮的样式可以在 `index.html` 的 CSS 部分找到：

```css
.language-switcher {
    position: absolute;
    top: 20px;
    right: 30px;
    /* ... */
}

.language-switcher .lang-btn {
    /* 按钮样式 */
}

.language-switcher .lang-btn.active {
    /* 激活状态样式 */
}
```

## 📱 响应式支持

语言切换按钮在移动设备上也能正常显示和使用，会根据屏幕尺寸自动调整位置。

## 🚀 未来扩展

### 添加新语言

如果需要添加更多语言支持（如日语、韩语等）：

1. 在 `i18n.js` 的 `translations` 对象中添加新语言的翻译
2. 在语言切换器中添加对应的按钮
3. 更新 `switchLanguage()` 函数支持新语言

示例：

```javascript
const translations = {
    zh: { /* 中文翻译 */ },
    en: { /* 英文翻译 */ },
    ja: { /* 日语翻译 */ },
};
```

```html
<button class="lang-btn" onclick="switchLanguage('ja')">
    <span class="lang-icon">🇯🇵</span> 日本語
</button>
```

## 💡 最佳实践

1. **统一键名**: 使用描述性的键名，如 `btn_delete` 而不是 `delete1`
2. **分组管理**: 按功能模块组织翻译文本
3. **保持同步**: 添加新功能时同时更新中英文翻译
4. **测试验证**: 在两种语言下都测试新功能
5. **保留原文**: 对于专有名词（如 VEX、Auton），保持原文不翻译

## 🐛 故障排查

### 翻译不生效

1. 检查 `i18n.js` 和 `i18n-helper.js` 是否正确加载
2. 查看浏览器控制台是否有错误信息
3. 确认 `data-i18n` 属性的键名在翻译对象中存在
4. 检查脚本加载顺序是否正确

### 切换后部分文本未更新

- 动态生成的内容需要在 `i18n-helper.js` 中添加更新逻辑
- 检查元素是否在 `updateDynamicContent()` 函数中被处理

### 语言选择不保存

- 检查浏览器是否禁用了 localStorage
- 查看浏览器隐私设置

## 📞 支持

如有问题或建议，请提交 Issue 或查看项目文档。
