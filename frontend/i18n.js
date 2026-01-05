// 国际化语言包
const translations = {
    zh: {
        // Header
        title: "RscoutX - VEX Pushback 智能侦察系统",
        subtitle: "数据驱动的竞赛分析平台",
        
        // Navigation
        nav_dashboard: "仪表板",
        nav_map: "地图",
        nav_admin: "管理",
        nav_report: "报告",
        
        // Dashboard
        dashboard_title: "📊 比赛数据仪表板",
        team_number: "队号",
        event_id: "赛事 ID",
        btn_sync: "同步比赛",
        btn_stats: "查看统计",
        stats_title: "📈 比赛统计",
        total_matches: "总场次",
        wins: "胜场",
        losses: "败场",
        win_rate: "胜率",
        avg_score: "平均得分",
        highest_score: "最高得分",
        lowest_score: "最低得分",
        
        // Map
        map_title: "🗺️ 路径渲染",
        render_method: "渲染方法",
        method_polyline: "折线",
        method_bezier: "贝塞尔曲线",
        method_spline: "样条曲线",
        method_astar: "A* 寻路",
        method_heatline: "热力线",
        coordinate_system: "坐标系统",
        coord_pixel: "像素坐标",
        coord_field: "场地坐标 (mm)",
        input_mode: "输入模式",
        mode_click: "点击画布",
        mode_manual: "手动输入",
        path_x: "X 坐标",
        path_y: "Y 坐标",
        btn_add_point: "添加点",
        btn_render: "渲染路径",
        btn_clear: "清除路径",
        path_points: "路径点",
        no_points: "暂无路径点",
        
        // Admin - Robots
        admin_robots_title: "🤖 机器人管理",
        robot_team_id: "队伍 ID",
        robot_base: "底盘类型",
        robot_base_sbot: "SBOT",
        robot_base_ruiguan: "瑞冠",
        robot_base_cbot: "CBOT",
        robot_foldable: "可折叠",
        robot_drivetrain: "传动系统",
        robot_tire_count: "轮胎数量",
        robot_notes: "备注",
        btn_create_robot: "创建机器人",
        btn_load_robots: "加载机器人列表",
        robot_list: "机器人列表",
        no_robots: "暂无机器人数据",
        btn_delete: "删除",
        
        // Admin - Drivers
        admin_drivers_title: "👤 驾驶员管理",
        driver_team_id: "队伍 ID",
        driver_name: "驾驶员姓名",
        driver_playstyle: "驾驶风格",
        playstyle_aggressive: "进攻型",
        playstyle_defensive: "防守型",
        playstyle_balanced: "平衡型",
        driver_likes_claw: "喜欢使用抓取",
        driver_control_agility: "控制灵活度 (1-10)",
        driver_speed_preference: "速度偏好",
        speed_slow: "慢速",
        speed_medium: "中速",
        speed_fast: "快速",
        driver_notes: "备注",
        btn_create_driver: "创建驾驶员",
        btn_load_drivers: "加载驾驶员列表",
        driver_list: "驾驶员列表",
        no_drivers: "暂无驾驶员数据",
        
        // Report
        report_title: "📝 AI 战队报告生成",
        report_team_id: "队伍 ID",
        report_event_id: "赛事 ID (可选)",
        report_include_map: "包含地图分析",
        report_include_driver: "包含驾驶员分析",
        report_include_robot: "包含机器人分析",
        report_language: "报告语言",
        report_lang_zh: "中文",
        report_lang_en: "英文",
        btn_generate_report: "生成报告",
        report_result: "报告结果",
        report_loading: "生成中...",
        btn_copy_markdown: "复制 Markdown",
        btn_copy_json: "复制 JSON",
        
        // Messages
        msg_success: "操作成功",
        msg_error: "操作失败",
        msg_loading: "加载中...",
        msg_copied: "已复制到剪贴板",
        msg_sync_success: "比赛数据同步成功",
        msg_create_success: "创建成功",
        msg_delete_success: "删除成功",
        msg_delete_confirm: "确定要删除吗?",
        
        // Common
        yes: "是",
        no: "否",
        cancel: "取消",
        confirm: "确认",
        close: "关闭",
        save: "保存",
        edit: "编辑",
        delete: "删除",
        create: "创建",
        update: "更新",
        search: "搜索",
        filter: "筛选",
        reset: "重置",
        refresh: "刷新",
        loading: "加载中...",
        no_data: "暂无数据",
        error: "错误",
        success: "成功",
        warning: "警告",
        info: "信息",
    },
    
    en: {
        // Header
        title: "RscoutX - VEX Pushback Scouting System",
        subtitle: "Data-Driven Competition Analysis Platform",
        
        // Navigation
        nav_dashboard: "Dashboard",
        nav_map: "Map",
        nav_admin: "Admin",
        nav_report: "Report",
        
        // Dashboard
        dashboard_title: "📊 Match Data Dashboard",
        team_number: "Team Number",
        event_id: "Event ID",
        btn_sync: "Sync Matches",
        btn_stats: "View Stats",
        stats_title: "📈 Match Statistics",
        total_matches: "Total Matches",
        wins: "Wins",
        losses: "Losses",
        win_rate: "Win Rate",
        avg_score: "Avg Score",
        highest_score: "Highest Score",
        lowest_score: "Lowest Score",
        
        // Map
        map_title: "🗺️ Path Rendering",
        render_method: "Render Method",
        method_polyline: "Polyline",
        method_bezier: "Bezier Curve",
        method_spline: "Spline Curve",
        method_astar: "A* Pathfinding",
        method_heatline: "Heatline",
        coordinate_system: "Coordinate System",
        coord_pixel: "Pixel Coordinates",
        coord_field: "Field Coordinates (mm)",
        input_mode: "Input Mode",
        mode_click: "Click Canvas",
        mode_manual: "Manual Input",
        path_x: "X Coordinate",
        path_y: "Y Coordinate",
        btn_add_point: "Add Point",
        btn_render: "Render Path",
        btn_clear: "Clear Path",
        path_points: "Path Points",
        no_points: "No path points",
        
        // Admin - Robots
        admin_robots_title: "🤖 Robot Management",
        robot_team_id: "Team ID",
        robot_base: "Robot Base",
        robot_base_sbot: "SBOT",
        robot_base_ruiguan: "Ruiguan",
        robot_base_cbot: "CBOT",
        robot_foldable: "Foldable",
        robot_drivetrain: "Drivetrain",
        robot_tire_count: "Tire Count",
        robot_notes: "Notes",
        btn_create_robot: "Create Robot",
        btn_load_robots: "Load Robot List",
        robot_list: "Robot List",
        no_robots: "No robot data",
        btn_delete: "Delete",
        
        // Admin - Drivers
        admin_drivers_title: "👤 Driver Management",
        driver_team_id: "Team ID",
        driver_name: "Driver Name",
        driver_playstyle: "Playstyle",
        playstyle_aggressive: "Aggressive",
        playstyle_defensive: "Defensive",
        playstyle_balanced: "Balanced",
        driver_likes_claw: "Likes Using Claw",
        driver_control_agility: "Control Agility (1-10)",
        driver_speed_preference: "Speed Preference",
        speed_slow: "Slow",
        speed_medium: "Medium",
        speed_fast: "Fast",
        driver_notes: "Notes",
        btn_create_driver: "Create Driver",
        btn_load_drivers: "Load Driver List",
        driver_list: "Driver List",
        no_drivers: "No driver data",
        
        // Report
        report_title: "📝 AI Team Report Generation",
        report_team_id: "Team ID",
        report_event_id: "Event ID (Optional)",
        report_include_map: "Include Map Analysis",
        report_include_driver: "Include Driver Analysis",
        report_include_robot: "Include Robot Analysis",
        report_language: "Report Language",
        report_lang_zh: "Chinese",
        report_lang_en: "English",
        btn_generate_report: "Generate Report",
        report_result: "Report Result",
        report_loading: "Generating...",
        btn_copy_markdown: "Copy Markdown",
        btn_copy_json: "Copy JSON",
        
        // Messages
        msg_success: "Success",
        msg_error: "Error",
        msg_loading: "Loading...",
        msg_copied: "Copied to clipboard",
        msg_sync_success: "Match data synced successfully",
        msg_create_success: "Created successfully",
        msg_delete_success: "Deleted successfully",
        msg_delete_confirm: "Are you sure you want to delete?",
        
        // Common
        yes: "Yes",
        no: "No",
        cancel: "Cancel",
        confirm: "Confirm",
        close: "Close",
        save: "Save",
        edit: "Edit",
        delete: "Delete",
        create: "Create",
        update: "Update",
        search: "Search",
        filter: "Filter",
        reset: "Reset",
        refresh: "Refresh",
        loading: "Loading...",
        no_data: "No data",
        error: "Error",
        success: "Success",
        warning: "Warning",
        info: "Info",
    }
};

// 国际化管理器
class I18n {
    constructor() {
        // 从 localStorage 读取保存的语言，默认中文
        this.currentLang = localStorage.getItem('rscoutx_language') || 'zh';
    }
    
    // 获取翻译文本
    t(key) {
        const keys = key.split('.');
        let value = translations[this.currentLang];
        
        for (const k of keys) {
            value = value?.[k];
        }
        
        return value || key;
    }
    
    // 切换语言
    setLanguage(lang) {
        if (translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('rscoutx_language', lang);
            this.updatePageLanguage();
        }
    }
    
    // 获取当前语言
    getLanguage() {
        return this.currentLang;
    }
    
    // 更新页面中所有带 data-i18n 属性的元素
    updatePageLanguage() {
        // 更新 HTML lang 属性
        document.documentElement.lang = this.currentLang === 'zh' ? 'zh-CN' : 'en';
        
        // 更新所有带 data-i18n 属性的元素
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            // 根据元素类型更新不同属性
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.type === 'button' || element.type === 'submit') {
                    element.value = translation;
                } else {
                    element.placeholder = translation;
                }
            } else if (element.tagName === 'OPTION') {
                element.textContent = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // 更新 placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
        
        // 更新 title
        document.querySelectorAll('[data-i18n-title]').forEach(element => {
            const key = element.getAttribute('data-i18n-title');
            element.title = this.t(key);
        });
        
        // 更新页面标题
        document.title = this.t('title');
        
        // 触发语言变化事件
        window.dispatchEvent(new CustomEvent('languageChanged', { 
            detail: { language: this.currentLang } 
        }));
    }
}

// 创建全局实例
const i18n = new I18n();

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        i18n.updatePageLanguage();
    });
} else {
    i18n.updatePageLanguage();
}
