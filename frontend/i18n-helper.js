// 页面加载后自动添加国际化支持的辅助脚本
document.addEventListener('DOMContentLoaded', function() {
    // 确保 i18n 已加载
    if (typeof i18n === 'undefined') {
        console.error('i18n.js not loaded! Please include i18n.js before i18n-helper.js');
        return;
    }
    
    // 等待一小段时间确保 DOM 完全加载
    setTimeout(() => {
        // 监听语言变化事件
        window.addEventListener('languageChanged', function(e) {
            const lang = e.detail.language;
            updateDynamicContent(lang);
        });
        
        // 初始化时更新一次
        updateDynamicContent(i18n.getLanguage());
        
        // 更新语言按钮状态
        updateLanguageButtons(i18n.getLanguage());
    }, 200);
});

function updateLanguageButtons(lang) {
    const zhBtn = document.getElementById('langZh');
    const enBtn = document.getElementById('langEn');
    
    if (zhBtn && enBtn) {
        zhBtn.classList.toggle('active', lang === 'zh');
        enBtn.classList.toggle('active', lang === 'en');
    }
}

function updateDynamicContent(lang) {
    const texts = {
        zh: {
            searchTitle: '🔍 队伍搜索',
            teamNumberLabel: '队伍编号',
            teamNumberPlaceholder: '例如: 1234A, 5678B, 9999C',
            searchBtn: '🔎 搜索历史数据',
            searchTip: '💡 将自动加载该队伍在所有赛事中的历史数据和统计信息',
            
            teamInfoTitle: '📊 队伍历史信息与数据统计',
            teamNumber: '队伍编号',
            teamName: '队伍名称',
            organization: '所属组织',
            region: '地区',
            eventCount: '参赛次数',
            totalMatches: '总比赛数',
            winRate: '历史胜率',
            avgScore: '平均得分',
            maxScore: '最高得分',
            autonScore: 'Auton 估算分',
            recentMatches: '📅 近期比赛记录',
            
            autonTitle: '🗺️ Auton 路径绘制',
            autonDescription: '💡 点击画布添加 Auton 路径点，支持多条 Auton 路径绘制与管理',
            canvasMode: '绘制模式',
            clickToAdd: '点击添加',
            manualInput: '手动输入',
            coordX: 'X 坐标',
            coordY: 'Y 坐标',
            addPoint: '添加点',
            currentAuton: '当前 Auton',
            newAuton: '新建 Auton',
            deleteAuton: '删除当前 Auton',
            clearAuton: '清空当前 Auton',
            saveAuton: '保存 Auton',
            loadAuton: '加载 Auton',
            exportReport: '导出完整报告',
            downloadAllAutons: '下载所有 Auton 路径图',
            
            robotStateTitle: '机器人状态标注',
            stateWingPushing: '推物块',
            stateIntaking: '吸入',
            stateReleasing: '释放',
            stateMoving: '移动',
            stateIdle: '待机',
            setCurrentState: '设置为当前状态',
            
            driverNotesTitle: '📝 驾驶员笔记',
            driverNotesPlaceholder: '记录驾驶习惯、策略偏好、特殊技巧等...',
            autoSaveStatus: '自动保存',
            
            printPreviewTitle: '🖨️ 打印预览',
            printBtn: '打印报告',
            
            noData: '暂无数据',
            loading: '加载中...',
            success: '成功',
            error: '错误',
        },
        en: {
            searchTitle: '🔍 Team Search',
            teamNumberLabel: 'Team Number',
            teamNumberPlaceholder: 'e.g.: 1234A, 5678B, 9999C',
            searchBtn: '🔎 Search Historical Data',
            searchTip: '💡 Automatically load historical data and statistics for this team across all events',
            
            teamInfoTitle: '📊 Team Historical Information & Data Statistics',
            teamNumber: 'Team Number',
            teamName: 'Team Name',
            organization: 'Organization',
            region: 'Region',
            eventCount: 'Events Participated',
            totalMatches: 'Total Matches',
            winRate: 'Win Rate',
            avgScore: 'Average Score',
            maxScore: 'Highest Score',
            autonScore: 'Auton Score Est.',
            recentMatches: '📅 Recent Match History',
            
            autonTitle: '🗺️ Auton Path Drawing',
            autonDescription: '💡 Click canvas to add Auton path points, supports drawing and managing multiple Auton paths',
            canvasMode: 'Drawing Mode',
            clickToAdd: 'Click to Add',
            manualInput: 'Manual Input',
            coordX: 'X Coordinate',
            coordY: 'Y Coordinate',
            addPoint: 'Add Point',
            currentAuton: 'Current Auton',
            newAuton: 'New Auton',
            deleteAuton: 'Delete Current Auton',
            clearAuton: 'Clear Current Auton',
            saveAuton: 'Save Auton',
            loadAuton: 'Load Auton',
            exportReport: 'Export Full Report',
            downloadAllAutons: 'Download All Auton Paths',
            
            robotStateTitle: 'Robot State Annotation',
            stateWingPushing: 'Wing Pushing',
            stateIntaking: 'Intaking',
            stateReleasing: 'Releasing',
            stateMoving: 'Moving',
            stateIdle: 'Idle',
            setCurrentState: 'Set as Current State',
            
            driverNotesTitle: '📝 Driver Notes',
            driverNotesPlaceholder: 'Record driving habits, strategy preferences, special skills, etc...',
            autoSaveStatus: 'Auto-Save',
            
            printPreviewTitle: '🖨️ Print Preview',
            printBtn: 'Print Report',
            
            noData: 'No data',
            loading: 'Loading...',
            success: 'Success',
            error: 'Error',
        }
    };
    
    const t = texts[lang];
    
    // 更新主要元素的文本内容
    const updates = [
        { selector: '.section-title', index: 0, key: 'searchTitle' },
        { selector: 'label', index: 0, key: 'teamNumberLabel' },
        { selector: '.btn-primary span', index: 0, key: 'searchBtn' },
    ];
    
    updates.forEach(({ selector, index, key }) => {
        const elements = document.querySelectorAll(selector);
        if (elements[index] && t[key]) {
            elements[index].textContent = t[key];
        }
    });
    
    // 更新 placeholder
    const teamNumberInput = document.getElementById('teamNumber');
    if (teamNumberInput && t.teamNumberPlaceholder) {
        teamNumberInput.placeholder = t.teamNumberPlaceholder;
    }
    
    // 更新提示文本
    const searchTip = document.querySelector('.section:first-of-type > div:last-child');
    if (searchTip && t.searchTip) {
        searchTip.textContent = t.searchTip;
    }
    
    // 更新队伍信息标题
    updateInfoLabels(t);
    
    // 更新 Auton 部分
    updateAutonSection(t);
    
    // 更新驾驶员笔记
    updateDriverNotes(t);
}

function updateInfoLabels(t) {
    const labels = [
        'teamNumber', 'teamName', 'organization', 'region',
        'eventCount', 'totalMatches', 'winRate', 'avgScore',
        'maxScore', 'autonScore'
    ];
    
    document.querySelectorAll('#teamInfoSection .info-label').forEach((label, index) => {
        if (labels[index] && t[labels[index]]) {
            label.textContent = t[labels[index]];
        }
    });
}

function updateAutonSection(t) {
    const autonSectionTitle = document.querySelector('#autonSection .section-title');
    if (autonSectionTitle && t.autonTitle) {
        autonSectionTitle.textContent = t.autonTitle;
    }
    
    // 更新其他 Auton 相关的UI元素
    // 这里可以根据需要添加更多元素的更新
}

function updateDriverNotes(t) {
    const driverNotesTextarea = document.getElementById('driverNotes');
    if (driverNotesTextarea && t.driverNotesPlaceholder) {
        driverNotesTextarea.placeholder = t.driverNotesPlaceholder;
    }
}
