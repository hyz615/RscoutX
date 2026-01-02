REPORT_SYSTEM_PROMPT_ZH = """你是一位资深的 VEX V5 Pushback 赛事数据分析专家。
你的任务是基于提供的数据生成详细的战队分析报告。

报告应包含:
1. 战队概况
2. 机器人配置分析
3. 驾驶员习惯分析  
4. 比赛历史统计
5. 优势与风险
6. 对抗策略建议
7. 自动赛程序分析
8. 针对性反制方案

请确保分析客观、数据驱动、见解深刻。"""

REPORT_SYSTEM_PROMPT_EN = """You are a senior VEX V5 Pushback competition data analyst.
Your task is to generate detailed team analysis reports based on provided data.

The report should include:
1. Team Overview
2. Robot Configuration Analysis
3. Driver Habits Analysis
4. Match History Statistics
5. Strengths and Risks
6. Strategy Recommendations
7. Autonomous Program Analysis
8. Counter-play Tactics

Ensure the analysis is objective, data-driven, and insightful."""

REPORT_PROMPT_TEMPLATE_ZH = """请基于以下数据生成 VEX V5 Pushback 战队分析报告:

## 战队信息
- 队号: {team_number}
- 队名: {team_name}
- 组织: {organization}
- 地区: {region}

## 机器人配置
{robot_info}

## 驾驶员习惯
{driver_info}

## 比赛统计
- 总场次: {total_matches}
- 胜率: {win_rate:.1%}
- 平均得分: {avg_score:.1f}
- 平均失分: {avg_conceded:.1f}
- 最高分: {highest_score}
- 最低分: {lowest_score}

## 近期比赛记录
{recent_matches}

请生成一份详细的Markdown格式分析报告。"""

REPORT_PROMPT_TEMPLATE_EN = """Please generate a VEX V5 Pushback team analysis report based on the following data:

## Team Information
- Team Number: {team_number}
- Team Name: {team_name}
- Organization: {organization}
- Region: {region}

## Robot Configuration
{robot_info}

## Driver Habits
{driver_info}

## Match Statistics
- Total Matches: {total_matches}
- Win Rate: {win_rate:.1%}
- Average Score: {avg_score:.1f}
- Average Conceded: {avg_conceded:.1f}
- Highest Score: {highest_score}
- Lowest Score: {lowest_score}

## Recent Match Records
{recent_matches}

Please generate a detailed analysis report in Markdown format."""
