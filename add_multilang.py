#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动为 index.html 添加多语言支持
Auto-add multilingual support to index.html
"""

import re
import sys

def add_lang_support(html_file='frontend/index.html'):
    """Add language support attributes to HTML file"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 读取文件: {html_file}")
        
        # 1. Add language switch buttons in header
        header_pattern = r'(<div class="header">)\s*(<h1>)'
        header_replacement = r'\1\n            <div class="lang-switch">\n                <button class="lang-btn active" onclick="switchLanguage(\'zh\')" id="langZh">中文</button>\n                <button class="lang-btn" onclick="switchLanguage(\'en\')" id="langEn">English</button>\n            </div>\n            \2'
        
        if 'lang-switch' not in content:
            content = re.sub(header_pattern, header_replacement, content)
            print("✅ 添加语言切换按钮")
        else:
            print("⏭️  语言切换按钮已存在")
        
        # 2. Add data-i18n to subtitle
        content = re.sub(
            r'<p>VEX Pushback 智能侦察与分析系统</p>',
            r'<p data-i18n="header.subtitle">VEX Pushback 智能侦察与分析系统</p>',
            content
        )
        
        # 3. Add data-i18n to section titles
        replacements = [
            (r'<div class="section-title">\s*🔍 队伍搜索\s*</div>',
             r'<div class="section-title">\n                    <span data-i18n="search.title">🔍 队伍搜索</span>\n                </div>'),
            
            (r'<label>队伍编号 Team Number</label>',
             r'<label data-i18n="search.teamNumber">队伍编号 Team Number</label>'),
            
            (r'<span>🔎 搜索历史数据</span>',
             r'<span data-i18n="search.button">🔎 搜索历史数据</span>'),
            
            (r'💡 将自动加载该队伍在所有赛事中的历史数据和统计信息',
             r'<span data-i18n="search.hint">💡 将自动加载该队伍在所有赛事中的历史数据和统计信息</span>'),
        ]
        
        for pattern, replacement in replacements:
            if 'data-i18n' not in content or pattern in content:
                content = re.sub(pattern, replacement, content)
        
        print("✅ 添加翻译属性")
        
        # 4. Add placeholder translation
        content = re.sub(
            r'(<input type="text" id="teamNumber" )(placeholder="例如: 1234A, 5678B, 9999C")',
            r'\1data-i18n-placeholder="search.placeholder" \2',
            content
        )
        
        # Save backup
        backup_file = html_file + '.backup'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 备份保存到: {backup_file}")
        
        # Save modified file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修改完成: {html_file}")
        
        print("\n" + "="*50)
        print("🎉 多语言支持添加成功!")
        print("="*50)
        print("\n📋 下一步:")
        print("1. 打开浏览器访问页面")
        print("2. 点击右上角的 'English' 按钮")
        print("3. 确认文本切换为英文")
        print("\n如有问题,可恢复备份文件:")
        print(f"  cp {backup_file} {html_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == '__main__':
    import os
    
    # Check if file exists
    html_file = 'frontend/index.html'
    if not os.path.exists(html_file):
        print(f"❌ 文件不存在: {html_file}")
        print("请确保在项目根目录运行此脚本")
        sys.exit(1)
    
    success = add_lang_support(html_file)
    sys.exit(0 if success else 1)
