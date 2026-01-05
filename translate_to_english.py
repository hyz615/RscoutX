#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to remove Chinese text and replace with English in frontend files
"""

import os
import re

# Define replacements
replacements = {
    # Title and headers
    "RscoutX - VEX Pushback 智能侦察系统": "RscoutX - VEX Pushback Scouting System",
    "VEX Pushback 智能侦察与分析系统": "VEX Pushback Intelligent Scouting and Analysis System",
    
    # Menu items
    "🔍 队伍搜索": "🔍 Team Search",
    "队伍编号 Team Number": "Team Number",
    "例如: 1234A, 5678B, 9999C": "e.g.: 1234A, 5678B, 9999C",
    "🔎 搜索历史数据": "🔎 Search History",
    "💡 将自动加载该队伍在所有赛事中的历史数据和统计信息": "💡 Automatically load team history and statistics from all events",
    "💡 将自动加载该队伍在所有赛事中的历史数据": "💡 Automatically load team history from all events",
    
    # Team info
    "📊 队伍历史信息与数据统计": "📊 Team History and Statistics",
    "队伍编号": "Team Number",
    "队伍名称": "Team Name",
    "所属组织": "Organization",
    "地区": "Region",
    "参赛次数": "Events Attended",
    "总比赛数": "Total Matches",
    "历史胜率": "Win Rate",
    "平均得分": "Average Score",
    "最高得分": "Highest Score",
    "Auton 估算分": "Auton Estimated Score",
    "📈 数据趋势图": "📈 Data Trends",
    
    # Map section
    "🗺️ Auton 路径绘制": "🗺️ Auton Path Drawing",
    "从前场启动": "Start from Front",
    "从后场启动": "Start from Back",
    "模拟路径": "Simulate Path",
    "清除路径": "Clear Path",
    "保存路径": "Save Path",
    "💡 点击地图Add路径点 | 按住拖动绘制路径": "💡 Click map to add points | Hold and drag to draw path",
    "路径点列表": "Path Points List",
    
    # Robot section
    "🤖 机器人类型": "🤖 Robot Type",
    "瑞冠型": "Ruiguan Type",
    "推球机器人,展开双翼进行推球": "Push robot with expandable wings",
    "自定义": "Custom",
    "机器人配备机翼 (Has Wing)": "Robot has Wings",
    "✓ 已启用机翼推球功能": "✓ Wing push function enabled",
    
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
    "备注": "Notes",
    
    # Buttons
    "搜索": "Search",
    "查询": "Query",
    "提交": "Submit",
    "取消": "Cancel",
    "确定": "Confirm",
    "保存": "Save",
    "删除": "Delete",
    "编辑": "Edit",
    "添加": "Add",
    "清空": "Clear",
    "重置": "Reset",
    "刷新": "Refresh",
    "下载": "Download",
    "上传": "Upload",
    "导出": "Export",
    "导入": "Import",
    "生成": "Generate",
    "渲染": "Render",
    
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
    "底盘类型": "Chassis Type",
    "传动系统": "Drivetrain",
    "轮胎数量": "Tire Count",
    "可折叠": "Foldable",
    
    # Status messages
    "加载中": "Loading",
    "加载中...": "Loading...",
    "请稍候": "Please wait",
    "请稍候...": "Please wait...",
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
    "VEX Pushback Field Map": "VEX Pushback Field Map",
    "Click to add path points": "Click to add path points",
    "路径渲染": "Path Rendering",
    "坐标系统": "Coordinate System",
    "像素坐标": "Pixel Coordinates",
    "场地坐标": "Field Coordinates",
    "渲染方法": "Rendering Method",
    "折线": "Polyline",
    "贝塞尔曲线": "Bezier Curve",
    "样条曲线": "Spline",
    "热力线": "Heatline",
    "点击添加路径点": "Click to add path points",
    "添加点": "Add Point",
}

def process_file(filepath):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for chinese, english in replacements.items():
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
            print(f"✓ Processed: {filepath}")
            return True
        else:
            print(f"- No changes: {filepath}")
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
    
    print("Starting translation to English...\n")
    
    processed_count = 0
    for filepath in files_to_process:
        if os.path.exists(filepath):
            if process_file(filepath):
                processed_count += 1
        else:
            print(f"✗ File not found: {filepath}")
    
    print(f"\nCompleted! Processed {processed_count} file(s).")

if __name__ == "__main__":
    main()
