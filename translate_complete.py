#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete script to translate all Chinese to English in frontend files
"""

import os
import re

def create_comprehensive_replacements():
    """Create comprehensive translation dictionary"""
    return {
        # Headers and titles
        "RscoutX - VEX Pushback 智能侦察系统": "RscoutX - VEX Pushback Scouting System",
        "VEX Pushback 智能侦察与分析系统": "VEX Pushback Intelligent Scouting and Analysis System",
        "智能侦察系统": "Intelligent Scouting System",
        
        # Search section
        "🔍 队伍搜索": "🔍 Team Search",
        "队伍编号": "Team Number",
        "例如: 1234A, 5678B, 9999C": "e.g.: 1234A, 5678B, 9999C",
        "🔎 搜索历史数据": "🔎 Search History",
        "将自动加载该队伍在所有赛事中的历史数据和统计信息": "Automatically load team history and statistics from all events",
        
        # Team info
        "📊 队伍历史信息与数据统计": "📊 Team History and Statistics",
        "队伍名称": "Team Name",
        "所属组织": "Organization",
        "地区": "Region",
        "参赛次数": "Events Attended",
        "总比赛数": "Total Matches",
        "历史胜率": "Win Rate",
        "平均得分": "Average Score",
        "最高得分": "Highest Score",
        "📈 数据趋势图": "📈 Data Trends",
        "近期比赛记录": "Recent Match Records",
        "上一个": "Previous",
        "下一个": "Next",
        
        # Path section
        "🗺️ Auton 路径绘制": "🗺️ Auton Path Drawing",
        "新增": "New",
        "当前": "Current",
        "路径": "Path",
        "选择机器人状态": "Select Robot State",
        "点击地图": "Click Map",
        "路径点": "Path Point",
        "按住拖动绘制连续路径": "Hold and drag to draw continuous path",
        "模拟路径": "Simulate Path",
        "清除路径": "Clear Path",
        "保存路径": "Save Path",
        "从前场启动": "Start from Front",
        "从后场启动": "Start from Back",
        
        # Robot section
        "🤖 机器人类型": "🤖 Robot Type",
        "路边机器人": "Roadside Robot",
        "机翼配置": "Wing Configuration",
        "机器人配备机翼": "Robot Equipped with Wings",
        "已启用机翼推球功能": "Wing push function enabled",
        "瑞冠型": "Ruiguan Type",
        "推球机器人,展开双翼进行推球": "Push robot with expandable wings",
        "自定义": "Custom",
        "底盘类型": "Chassis Type",
        "传动系统": "Drivetrain",
        "轮胎数量": "Tire Count",
        "可折叠": "Foldable",
        
        # Driver section
        "👤 驾驶员习惯": "👤 Driver Habits",
        "驾驶员姓名": "Driver Name",
        "驾驶风格": "Driving Style",
        "进攻型": "Aggressive",
        "防守型": "Defensive",
        "平衡型": "Balanced",
        "控制灵活度": "Control Agility",
        "速度偏好": "Speed Preference",
        "快速": "Fast",
        "中等": "Medium",
        "慢速": "Slow",
        "喜欢使用抓取": "Likes Claw",
        "习惯标签": "Habit Tags",
        "输入": "Input",
        "标签": "Tag",
        "标签将动态": "Tags will dynamically",
        "到这里": "here",
        "在这里记录驾驶员的其他习惯": "Record other driver habits here",
        "偏好策略": "Preferred Strategy",
        "特殊技巧等": "Special Skills, etc.",
        "例如": "e.g.",
        "喜欢使用机械臂抓取": "Prefers using mechanical arm to grab",
        "擅长精准定位": "Good at precise positioning",
        "偏好左侧场地": "Prefers left side of field",
        "备注": "Notes",
        
        # Opponent analysis
        "对手侦察分析": "Opponent Scouting Analysis",
        "将对手的": "Send opponent's",
        "路径图": "Path Diagram",
        "比赛数据": "Match Data",
        "机器人类型和驾驶员习惯发送给": "Robot type and driver habits to",
        "多模态模型": "Multimodal Model",
        "针对性的侦察报告和反制策略": "Targeted scouting report and counter strategy",
        "报告将从": "Report will from",
        "如何针对该对手": "How to target this opponent",
        "的角度": "Perspective",
        "分析其优势": "Analyze their strengths",
        "弱点并提供具体的应对方案": "Weaknesses and provide specific countermeasures",
        "预览数据": "Preview Data",
        "对手分析报告": "Opponent Analysis Report",
        
        # Report section
        "📝 AI 比赛报告": "📝 AI Match Report",
        "生成报告": "Generate Report",
        "语言选择": "Language",
        "中文": "Chinese",
        "英文": "English",
        "包含地图": "Include Map",
        "包含驾驶员": "Include Driver",
        "包含机器人": "Include Robot",
        "复制 Markdown": "Copy Markdown",
        "复制 JSON": "Copy JSON",
        
        # Admin section
        "⚙️ 管理员": "⚙️ Admin",
        "机器人管理": "Robot Management",
        "驾驶员管理": "Driver Management",
        "添加机器人": "Add Robot",
        "添加驾驶员": "Add Driver",
        "机器人列表": "Robot List",
        "驾驶员列表": "Driver List",
        
        # Data management
        "所有": "All",
        "图片": "Images",
        "清除所有自动": "Clear All Auto",
        "的数据": "Data",
        "清除": "Clear",
        "数据": "Data",
        "分析预览数据": "Analyze Preview Data",
        
        # Time related
        "进攻": "Attack",
        "防守": "Defense",
        "最后": "Last",
        "秒进攻": "Second Attack",
        
        # Common buttons
        "搜索": "Search",
        "查询": "Query",
        "提交": "Submit",
        "取消": "Cancel",
        "确定": "Confirm",
        "保存": "Save",
        "删除": "Delete",
        "编辑": "Edit",
        "添加": "Add",
        "重置": "Reset",
        "刷新": "Refresh",
        "下载": "Download",
        "上传": "Upload",
        "导出": "Export",
        "导入": "Import",
        "生成": "Generate",
        "渲染": "Render",
        
        # Status messages
        "加载中": "Loading",
        "请稍候": "Please wait",
        "成功": "Success",
        "失败": "Failed",
        "错误": "Error",
        "警告": "Warning",
        "提示": "Info",
        "数据加载成功": "Data loaded successfully",
        "数据加载失败": "Failed to load data",
        "操作成功": "Operation successful",
        "操作失败": "Operation failed",
        "请输入队伍编号": "Please enter team number",
        "请选择赛事": "Please select event",
        "确认删除吗": "Confirm deletion?",
        "数据已保存": "Data saved",
        "数据已删除": "Data deleted",
        "未找到数据": "Data not found",
        "网络错误": "Network error",
        "服务器错误": "Server error",
        
        # Map related
        "pushback_map.png 未找到 - 使用默认网格": "pushback_map.png not found - using default grid",
        "使用空白地图。点击添加点。": "Using blank map. Click to add points.",
        "地图加载错误": "Error loading map",
    }

def process_file(filepath, replacements):
    """Process a single file with replacements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements (sort by length descending to avoid partial replacements)
        sorted_replacements = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
        for chinese, english in sorted_replacements:
            content = content.replace(chinese, english)
        
        # Change lang attribute
        content = content.replace('lang="zh-CN"', 'lang="en"')
        content = content.replace('lang="zh"', 'lang="en"')
        content = content.replace('lang=\'zh-CN\'', 'lang=\'en\'')
        content = content.replace('lang=\'zh\'', 'lang=\'en\'')
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Count remaining Chinese characters
            remaining = len(re.findall(r'[\u4e00-\u9fa5]', content))
            print(f"✓ Processed: {os.path.basename(filepath)} ({remaining} Chinese chars remaining)")
            return True
        else:
            remaining = len(re.findall(r'[\u4e00-\u9fa5]', content))
            print(f"- No changes: {os.path.basename(filepath)} ({remaining} Chinese chars remaining)")
            return False
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main function"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    files_to_process = [
        os.path.join(script_dir, "frontend", "index.html"),
        os.path.join(script_dir, "frontend", "app.js"),
    ]
    
    replacements = create_comprehensive_replacements()
    
    print(f"Starting translation to English ({len(replacements)} replacements)...\n")
    
    processed_count = 0
    for filepath in files_to_process:
        if os.path.exists(filepath):
            if process_file(filepath, replacements):
                processed_count += 1
        else:
            print(f"✗ File not found: {filepath}")
    
    print(f"\nCompleted! Processed {processed_count} file(s).")

if __name__ == "__main__":
    main()
