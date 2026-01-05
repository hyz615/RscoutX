// i18n.js - 国际化支持
// Multi-language support for RscoutX

const translations = {
    zh: {
        header: {
            subtitle: "VEX Pushback 智能侦察与分析系统"
        },
        search: {
            title: "🔍 队伍搜索",
            teamNumber: "队伍编号 Team Number",
            placeholder: "例如: 1234A, 5678B, 9999C",
            button: "🔎 搜索历史数据",
            hint: "💡 将自动加载该队伍在所有赛事中的历史数据和统计信息"
        },
        teamInfo: {
            title: "📊 队伍历史信息与数据统计",
            teamNumber: "队伍编号",
            teamName: "队伍名称",
            organization: "所属组织",
            region: "地区",
            eventCount: "参赛次数",
            totalMatches: "总比赛数",
            winRate: "历史胜率",
            avgScore: "平均得分",
            maxScore: "最高得分",
            autonScore: "Auton 估算分",
            recentMatches: "📅 近期比赛记录"
        },
        auton: {
            title: "🗺️ Auton 路径绘制",
            inputMode: "输入模式",
            clickInput: "点击输入",
            manualInput: "手动输入",
            renderMethod: "渲染方法",
            polyline: "折线",
            bezier: "贝塞尔曲线",
            spline: "样条曲线",
            astar: "A* 寻路",
            heatline: "热力线",
            coordinateSystem: "坐标系统",
            pixel: "像素坐标",
            field: "场地坐标 (mm)",
            pathStyle: "路径样式",
            color: "颜色",
            width: "宽度",
            opacity: "不透明度",
            arrow: "显示箭头",
            xCoord: "X 坐标",
            yCoord: "Y 坐标",
            addPoint: "添加点",
            clearPoints: "清除所有点",
            renderPath: "渲染路径",
            exportPath: "导出路径数据",
            robotState: "机器人状态",
            pointsCounter: "已添加点数",
            mapNotFound: "pushback_map.png 未找到 - 使用默认网格"
        },
        driver: {
            title: "👤 驾驶员习惯标记",
            hint: "💡 在地图上标记驾驶习惯特征点位（例如：常用起始点、防守位置等）",
            addHabit: "添加习惯标记"
        },
        aiExport: {
            title: "🤖 AI 数据导出",
            hint: "💡 导出结构化数据用于 LLM 分析和报告生成",
            generateReport: "生成 AI 侦察报告",
            copyJson: "复制 JSON",
            copyMarkdown: "复制 Markdown",
            preview: "数据预览"
        },
        messages: {
            searching: "正在搜索队伍信息...",
            teamNotFound: "未找到队伍信息",
            loadingMatches: "正在加载比赛数据...",
            matchesLoaded: "成功加载比赛数据",
            noMatches: "暂无比赛记录",
            pointAdded: "已添加点",
            invalidCoords: "无效的坐标值",
            pointsCleared: "已清除所有点",
            rendering: "正在渲染路径...",
            renderSuccess: "路径渲染成功",
            renderError: "路径渲染失败",
            copied: "已复制到剪贴板",
            copyFailed: "复制失败",
            generating: "正在生成报告...",
            reportGenerated: "报告生成成功"
        }
    },
    en: {
        header: {
            subtitle: "VEX Pushback Intelligent Scouting & Analysis System"
        },
        search: {
            title: "🔍 Team Search",
            teamNumber: "Team Number",
            placeholder: "e.g., 1234A, 5678B, 9999C",
            button: "🔎 Search History",
            hint: "💡 Automatically load team's historical data and statistics from all events"
        },
        teamInfo: {
            title: "📊 Team History & Statistics",
            teamNumber: "Team Number",
            teamName: "Team Name",
            organization: "Organization",
            region: "Region",
            eventCount: "Events Attended",
            totalMatches: "Total Matches",
            winRate: "Win Rate",
            avgScore: "Average Score",
            maxScore: "Max Score",
            autonScore: "Auton Score Est.",
            recentMatches: "📅 Recent Match History"
        },
        auton: {
            title: "🗺️ Auton Path Drawing",
            inputMode: "Input Mode",
            clickInput: "Click Input",
            manualInput: "Manual Input",
            renderMethod: "Render Method",
            polyline: "Polyline",
            bezier: "Bezier Curve",
            spline: "Spline Curve",
            astar: "A* Pathfinding",
            heatline: "Heatline",
            coordinateSystem: "Coordinate System",
            pixel: "Pixel Coords",
            field: "Field Coords (mm)",
            pathStyle: "Path Style",
            color: "Color",
            width: "Width",
            opacity: "Opacity",
            arrow: "Show Arrows",
            xCoord: "X Coordinate",
            yCoord: "Y Coordinate",
            addPoint: "Add Point",
            clearPoints: "Clear All Points",
            renderPath: "Render Path",
            exportPath: "Export Path Data",
            robotState: "Robot State",
            pointsCounter: "Points Added",
            mapNotFound: "pushback_map.png not found - using default grid"
        },
        driver: {
            title: "👤 Driver Habit Markers",
            hint: "💡 Mark driver habit positions on the map (e.g., starting points, defensive positions)",
            addHabit: "Add Habit Marker"
        },
        aiExport: {
            title: "🤖 AI Data Export",
            hint: "💡 Export structured data for LLM analysis and report generation",
            generateReport: "Generate AI Scouting Report",
            copyJson: "Copy JSON",
            copyMarkdown: "Copy Markdown",
            preview: "Data Preview"
        },
        messages: {
            searching: "Searching for team information...",
            teamNotFound: "Team not found",
            loadingMatches: "Loading match data...",
            matchesLoaded: "Match data loaded successfully",
            noMatches: "No match records found",
            pointAdded: "Point added",
            invalidCoords: "Invalid coordinate values",
            pointsCleared: "All points cleared",
            rendering: "Rendering path...",
            renderSuccess: "Path rendered successfully",
            renderError: "Path rendering failed",
            copied: "Copied to clipboard",
            copyFailed: "Copy failed",
            generating: "Generating report...",
            reportGenerated: "Report generated successfully"
        }
    }
};

let currentLang = 'zh'; // Default language

function switchLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('rscoutx_lang', lang);
    
    // Update button states
    document.getElementById('langZh').classList.toggle('active', lang === 'zh');
    document.getElementById('langEn').classList.toggle('active', lang === 'en');
    
    // Update all translatable elements
    updateTranslations();
}

function updateTranslations() {
    const t = translations[currentLang];
    
    // Update elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const value = getNestedValue(t, key);
        if (value) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                // Don't change input values, only placeholders
                if (el.hasAttribute('data-i18n-placeholder')) {
                    const placeholderKey = el.getAttribute('data-i18n-placeholder');
                    const placeholderValue = getNestedValue(t, placeholderKey);
                    if (placeholderValue) el.placeholder = placeholderValue;
                }
            } else {
                el.textContent = value;
            }
        }
    });
    
    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        const value = getNestedValue(t, key);
        if (value) el.placeholder = value;
    });
}

function getNestedValue(obj, path) {
    return path.split('.').reduce((current, key) => current?.[key], obj);
}

function t(key) {
    return getNestedValue(translations[currentLang], key) || key;
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('rscoutx_lang') || 'zh';
    switchLanguage(savedLang);
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { switchLanguage, t, translations };
}
