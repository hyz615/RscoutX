// 简化的国际化实现 - 直接翻译文本内容

// 翻译映射表
const textTranslations = {
    zh: {
        // 精确匹配的文本
        "🔍 队伍搜索": "🔍 队伍搜索",
        "队伍编号 Team Number": "队伍编号",
        "🔎 搜索历史数据": "🔎 搜索历史数据",
        "💡 将自动加载该队伍在所有赛事中的历史数据和统计信息": "💡 将自动加载该队伍在所有赛事中的历史数据和统计信息",
        
        "📊 队伍历史信息与数据统计": "📊 队伍历史信息与数据统计",
        "队伍编号": "队伍编号",
        "队伍名称": "队伍名称",
        "所属组织": "所属组织",
        "地区": "地区",
        "参赛次数": "参赛次数",
        "总比赛数": "总比赛数",
        "历史胜率": "历史胜率",
        "平均得分": "平均得分",
        "最高得分": "最高得分",
        "Auton 估算分": "Auton 估算分",
        "📅 近期比赛记录": "📅 近期比赛记录",
        
        "🗺️ Auton 路径绘制": "🗺️ Auton 路径绘制",
        "💡 点击画布添加 Auton 路径点，支持多条 Auton 路径绘制与管理": "💡 点击画布添加 Auton 路径点，支持多条 Auton 路径绘制与管理",
        "绘制模式:": "绘制模式:",
        "点击添加": "点击添加",
        "手动输入": "手动输入",
        "X 坐标:": "X 坐标:",
        "Y 坐标:": "Y 坐标:",
        "添加点": "添加点",
        "当前 Auton:": "当前 Auton:",
        "新建 Auton": "新建 Auton",
        "删除当前 Auton": "删除当前 Auton",
        "清空当前 Auton": "清空当前 Auton",
        "保存 Auton": "保存 Auton",
        "加载 Auton": "加载 Auton",
        "导出完整报告": "导出完整报告",
        "下载所有 Auton 路径图": "下载所有 Auton 路径图",
        
        "🤖 机器人状态标注": "🤖 机器人状态标注",
        "推物块": "推物块",
        "吸入": "吸入",
        "释放": "释放",
        "移动": "移动",
        "待机": "待机",
        "设置为当前状态": "设置为当前状态",
        
        "📝 驾驶员笔记": "📝 驾驶员笔记",
        "记录驾驶习惯、策略偏好、特殊技巧等...": "记录驾驶习惯、策略偏好、特殊技巧等...",
        "自动保存": "自动保存",
        
        "🖨️ 打印预览": "🖨️ 打印预览",
        "打印报告": "打印报告",
        
        // AI 分析部分
        "🤖 AI 对手侦察分析": "🤖 AI 对手侦察分析",
        '📋 将对手的 Auton 路径图、比赛数据、机器人类型和驾驶员习惯发送给 GPT-4o 多模态模型，生成针对性的侦察报告和反制策略。': '📋 将对手的 Auton 路径图、比赛数据、机器人类型和驾驶员习惯发送给 GPT-4o 多模态模型，生成针对性的侦察报告和反制策略。',
        '💡 报告将从"如何针对该对手"的角度，分析其优势、弱点并提供具体的应对方案。': '💡 报告将从"如何针对该对手"的角度，分析其优势、弱点并提供具体的应对方案。',
        "👁️ 预览数据": "👁️ 预览数据",
        "🚀 生成对手分析报告": "🚀 生成对手分析报告",
        "💾 下载所有 Auton 图片": "💾 下载所有 Auton 图片",
        "🗑️ 清除保存数据": "🗑️ 清除保存数据",
        "📊 AI 分析预览数据:": "📊 AI 分析预览数据:",
        
        // 消息提示
        "正在生成 AI 分析报告...": "正在生成 AI 分析报告...",
        "AI 分析报告已生成!": "AI 分析报告已生成!",
        "报告已生成（AI 不可用，显示基础报告）": "报告已生成（AI 不可用，显示基础报告）",
        "已切换到中文": "已切换到中文",
    },
    en: {
        // English translations
        "🔍 队伍搜索": "🔍 Team Search",
        "队伍编号 Team Number": "Team Number",
        "🔎 搜索历史数据": "🔎 Search Historical Data",
        "💡 将自动加载该队伍在所有赛事中的历史数据和统计信息": "💡 Automatically load historical data and statistics for this team across all events",
        
        "📊 队伍历史信息与数据统计": "📊 Team Historical Info & Statistics",
        "队伍编号": "Team Number",
        "队伍名称": "Team Name",
        "所属组织": "Organization",
        "地区": "Region",
        "参赛次数": "Events Participated",
        "总比赛数": "Total Matches",
        "历史胜率": "Win Rate",
        "平均得分": "Average Score",
        "最高得分": "Highest Score",
        "Auton 估算分": "Auton Score Est.",
        "📅 近期比赛记录": "📅 Recent Match History",
        
        "🗺️ Auton 路径绘制": "🗺️ Auton Path Drawing",
        "💡 点击画布添加 Auton 路径点，支持多条 Auton 路径绘制与管理": "💡 Click canvas to add Auton path points, supports drawing and managing multiple Auton paths",
        "绘制模式:": "Drawing Mode:",
        "点击添加": "Click to Add",
        "手动输入": "Manual Input",
        "X 坐标:": "X Coordinate:",
        "Y 坐标:": "Y Coordinate:",
        "添加点": "Add Point",
        "当前 Auton:": "Current Auton:",
        "新建 Auton": "New Auton",
        "删除当前 Auton": "Delete Current Auton",
        "清空当前 Auton": "Clear Current Auton",
        "保存 Auton": "Save Auton",
        "加载 Auton": "Load Auton",
        "导出完整报告": "Export Full Report",
        "下载所有 Auton 路径图": "Download All Auton Paths",
        
        "🤖 机器人状态标注": "🤖 Robot State Annotation",
        "推物块": "Wing Pushing",
        "吸入": "Intaking",
        "释放": "Releasing",
        "移动": "Moving",
        "待机": "Idle",
        "设置为当前状态": "Set as Current State",
        
        "📝 驾驶员笔记": "📝 Driver Notes",
        "记录驾驶习惯、策略偏好、特殊技巧等...": "Record driving habits, strategy preferences, special skills, etc...",
        "自动保存": "Auto-Save",
        
        "🖨️ 打印预览": "🖨️ Print Preview",
        "打印报告": "Print Report",
        
        // AI Analysis Section
        "🤖 AI 对手侦察分析": "🤖 AI Opponent Scouting Analysis",
        '📋 将对手的 Auton 路径图、比赛数据、机器人类型和驾驶员习惯发送给 GPT-4o 多模态模型，生成针对性的侦察报告和反制策略。': '📋 Send opponent Auton paths, match data, robot types, and driver habits to GPT-4o multimodal model to generate targeted scouting reports and counter-strategies.',
        '💡 报告将从"如何针对该对手"的角度，分析其优势、弱点并提供具体的应对方案。': '💡 Reports analyze opponent strengths, weaknesses, and provide specific countermeasures from a "how to counter this opponent" perspective.',
        "👁️ 预览数据": "👁️ Preview Data",
        "🚀 生成对手分析报告": "🚀 Generate Opponent Analysis",
        "💾 下载所有 Auton 图片": "💾 Download All Auton Images",
        "🗑️ 清除保存数据": "🗑️ Clear Saved Data",
        "📊 AI 分析预览数据:": "📊 AI Analysis Preview Data:",
        
        // Messages
        "正在生成 AI 分析报告...": "Generating AI analysis report...",
        "AI 分析报告已生成!": "AI analysis report generated!",
        "报告已生成（AI 不可用，显示基础报告）": "Report generated (AI unavailable, showing basic report)",
        "已切换到中文": "Switched to Chinese",
        "Switched to English": "Switched to English",
    }
};

// 简单的国际化类
class SimpleI18n {
    constructor() {
        this.currentLang = localStorage.getItem('rscoutx_language') || 'zh';
        this.originalTexts = new Map(); // 存储原始文本
    }
    
    setLanguage(lang) {
        if (!textTranslations[lang]) {
            console.error('Language not supported:', lang);
            return;
        }
        
        this.currentLang = lang;
        localStorage.setItem('rscoutx_language', lang);
        this.translatePage();
        
        // 触发事件
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { language: lang }
        }));
    }
    
    getLanguage() {
        return this.currentLang;
    }
    
    // 翻译单个文本（用于动态消息）
    t(text) {
        const translations = textTranslations[this.currentLang];
        return translations[text] || text;
    }
    
    translatePage() {
        const translations = textTranslations[this.currentLang];
        
        // 翻译所有文本节点
        this.translateTextNodes(document.body, translations);
        
        // 翻译 placeholder
        document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
            const originalPlaceholder = el.getAttribute('data-original-placeholder') || el.placeholder;
            if (!el.getAttribute('data-original-placeholder')) {
                el.setAttribute('data-original-placeholder', originalPlaceholder);
            }
            const translated = translations[originalPlaceholder];
            if (translated) {
                el.placeholder = translated;
            }
        });
        
        // 更新页面标题
        if (this.currentLang === 'en') {
            document.title = 'RscoutX - VEX Pushback Scouting System';
        } else {
            document.title = 'RscoutX - VEX Pushback 智能侦察系统';
        }
    }
    
    translateTextNodes(node, translations) {
        // 跳过 script 和 style 标签
        if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.tagName === 'SCRIPT' || node.tagName === 'STYLE') {
                return;
            }
        }
        
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.textContent.trim();
            if (text && translations[text]) {
                // 保存原始文本
                if (!node.parentElement.hasAttribute('data-original-text')) {
                    node.parentElement.setAttribute('data-original-text', text);
                }
                node.textContent = node.textContent.replace(text, translations[text]);
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            // 处理按钮的内部 span
            if (node.tagName === 'BUTTON' && node.querySelector('span')) {
                const span = node.querySelector('span');
                const text = span.textContent.trim();
                if (text && translations[text]) {
                    if (!span.hasAttribute('data-original-text')) {
                        span.setAttribute('data-original-text', text);
                    }
                    span.textContent = translations[text];
                }
            }
            
            // 递归处理子节点
            for (let child of node.childNodes) {
                this.translateTextNodes(child, translations);
            }
        }
    }
}

// 创建全局实例
const i18n = new SimpleI18n();

// 页面加载后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        i18n.translatePage();
    });
} else {
    i18n.translatePage();
}
