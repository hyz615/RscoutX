# 🔧 AI 功能快速修复指南

## ❌ 问题：AI 智能分析暂时不可用

### 原因诊断

检查发现配置文件中的模型名称错误：
```bash
OPENAI_MODEL=gpt-5.2-2025-12-11  # ❌ 这个模型不存在
```

---

## ✅ 解决方案

### 已修复
配置文件已自动更新为：
```bash
OPENAI_MODEL=gpt-4o  # ✅ 有效的模型
```

### 需要您做的

**1. 重启后端服务**

停止当前运行的后端（如果正在运行）：
- 在终端按 `Ctrl + C`

重新启动：
```powershell
.\start.bat
```

**2. 等待服务启动**

看到以下信息表示成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**3. 测试 AI 功能**

1. 打开浏览器访问 http://localhost:8000/docs
2. 找到 `/api/report/generate` 接口
3. 点击 "Try it out"
4. 输入测试数据：
   ```json
   {
     "team_id": 1,
     "event_id": null,
     "include_map": true,
     "include_driver": true,
     "include_robot": true,
     "language": "zh"
   }
   ```
5. 点击 "Execute"
6. 查看是否返回成功响应

**4. 在前端测试**

1. 打开 http://localhost:8000/frontend/index_new.html
2. 搜索任意队伍
3. 绘制一些 Auton 路径
4. 点击 "🚀 发送到 AI 分析"
5. 应该看到成功消息而不是降级报告

---

## 🔍 其他可能的问题

### 问题 1: API Key 无效

**症状：** 提示 "Invalid API key"

**解决：**
1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API Key
3. 替换 `.env` 文件中的 `OPENAI_API_KEY`
4. 重启后端

### 问题 2: 余额不足

**症状：** 提示 "Insufficient quota"

**解决：**
- 充值 OpenAI 账户，或
- 切换到免费的 Ollama：
  ```bash
  LLM_PROVIDER=ollama
  ```

### 问题 3: 网络问题

**症状：** 提示 "Connection timeout"

**解决：**
- 检查网络连接
- 确认能访问 OpenAI API
- 考虑使用代理或本地 Ollama

---

## 📋 有效的模型列表

您可以选择以下任一模型（按性能排序）：

| 模型名称 | 性能 | 成本 | 推荐度 |
|---------|------|------|--------|
| `gpt-4o` | ⭐⭐⭐⭐⭐ | 💰💰💰 | ⭐⭐⭐⭐⭐ 最推荐 |
| `gpt-4-turbo` | ⭐⭐⭐⭐⭐ | 💰💰💰💰 | ⭐⭐⭐⭐ |
| `gpt-4` | ⭐⭐⭐⭐⭐ | 💰💰💰💰💰 | ⭐⭐⭐ |
| `gpt-3.5-turbo` | ⭐⭐⭐ | 💰 | ⭐⭐⭐⭐ 便宜 |

**推荐配置：**
```bash
OPENAI_MODEL=gpt-4o  # 性能好，速度快，成本适中
```

---

## 🎯 验证修复

运行以下命令测试配置：

```powershell
# 1. 确保后端在运行
# 打开新的 PowerShell 窗口
.\start.bat

# 2. 在另一个 PowerShell 窗口测试 API
curl http://localhost:8000/api/teams/
```

如果返回 JSON 数据，说明后端正常运行。

---

## 💡 临时降级方案

如果仍然无法使用 AI 功能，系统会自动使用降级报告：

**降级报告包含：**
- ✅ 完整的队伍统计数据
- ✅ 所有 Auton 路径可视化
- ✅ 机器人配置信息
- ✅ 驾驶员习惯笔记
- ⚠️ 无 AI 智能建议

这不影响其他功能的使用，只是没有 AI 生成的分析和建议。

---

## 📞 仍然有问题？

**查看后端日志：**
```powershell
# 运行后端时注意控制台输出
.\start.bat
# 查看是否有错误信息
```

**查看浏览器控制台：**
1. 按 F12 打开开发者工具
2. 切换到 Console 标签
3. 查看是否有红色错误信息
4. 复制错误信息以便调试

**常见错误日志：**
```
❌ "model_not_found: The model 'gpt-5.2-2025-12-11' does not exist"
   → 解决：已修复，重启后端

❌ "invalid_api_key: Incorrect API key provided"
   → 解决：更新 API Key

❌ "insufficient_quota: You exceeded your current quota"
   → 解决：充值或使用 Ollama
```

---

**最后更新：** 2026年1月2日  
**修复内容：** 将 `gpt-5.2-2025-12-11` 改为 `gpt-4o`  
**状态：** ✅ 配置已修复，需要重启后端生效
