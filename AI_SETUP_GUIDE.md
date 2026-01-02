# 🤖 AI 功能配置指南

## 问题诊断

如果 AI 智能分析功能提示"生成失败"或显示降级报告，通常是以下原因：

### 1. OpenAI API 配置问题

**当前配置检查：**
```bash
# 查看 backend/.env 文件
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-5  # ❌ 问题：GPT-5 不存在
```

**问题：**
- ❌ `OPENAI_MODEL=gpt-5` - GPT-5 尚未发布
- ⚠️ API Key 可能已过期或无效

---

## 解决方案

### 方案 A：使用 OpenAI GPT-4 (推荐)

1. **获取有效的 OpenAI API Key**
   - 访问: https://platform.openai.com/api-keys
   - 创建新的 API Key
   - 确保账户有充足余额

2. **修改 `backend/.env` 文件**
   ```bash
   # LLM Providers
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-your-new-api-key-here  # 替换为你的新 Key
   OPENAI_MODEL=gpt-4-turbo  # 或 gpt-4, gpt-4o
   ```

3. **重启后端服务**
   ```bash
   # 停止当前运行的后端 (Ctrl+C)
   # 重新运行
   .\start.bat
   ```

### 方案 B：使用本地 Ollama (免费)

如果不想使用付费的 OpenAI API，可以使用本地运行的 Ollama：

1. **安装 Ollama**
   - 下载: https://ollama.ai/download
   - 安装后运行: `ollama pull llama2`

2. **修改 `backend/.env` 文件**
   ```bash
   # LLM Providers
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2  # 或 mistral, codellama
   ```

3. **启动 Ollama 服务**
   ```bash
   ollama serve
   ```

4. **重启后端服务**
   ```bash
   .\start.bat
   ```

### 方案 C：继续使用降级模式 (无需 AI)

如果暂时不需要 AI 智能分析：

- ✅ 系统会自动生成基础报告
- ✅ 包含所有统计数据和 Auton 可视化
- ✅ 不需要任何额外配置
- 📊 报告包含：队伍信息、比赛统计、机器人配置、Auton 路径等

---

## 验证配置

配置完成后，测试 AI 功能：

1. **搜索任意队伍**
2. **绘制一些 Auton 路径**
3. **点击 "🚀 发送到 AI 分析"**
4. **检查结果：**
   - ✅ 成功：看到 "AI 分析报告已生成!"
   - ⚠️ 降级：看到 "报告已生成（AI 不可用，显示基础报告）"

---

## 常见错误

### 错误 1: "Invalid API Key"
**原因：** API Key 无效或过期  
**解决：** 重新生成新的 API Key

### 错误 2: "Model not found: gpt-5"
**原因：** 模型名称错误  
**解决：** 改为 `gpt-4-turbo` 或 `gpt-4`

### 错误 3: "Connection timeout"
**原因：** 网络问题或 Ollama 未启动  
**解决：** 
- 检查网络连接
- 如使用 Ollama，确保 `ollama serve` 正在运行

### 错误 4: "Insufficient quota"
**原因：** OpenAI 账户余额不足  
**解决：** 充值账户或切换到 Ollama (免费)

---

## 推荐配置

### 🏆 最佳体验 (需付费)
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo
```
- ✅ 最智能的分析
- ✅ 最详细的建议
- ⚠️ 需要付费 API

### 💰 免费方案
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```
- ✅ 完全免费
- ✅ 本地运行，隐私安全
- ⚠️ 需要下载模型 (~4GB)
- ⚠️ 质量略低于 GPT-4

### 🚀 无需配置
不修改任何配置，直接使用：
- ✅ 立即可用
- ✅ 自动生成基础报告
- ⚠️ 无 AI 智能分析

---

## 技术支持

如果以上方案都无法解决问题：

1. **查看后端日志**
   ```bash
   # 运行后端时注意控制台输出
   .\start.bat
   ```

2. **查看浏览器控制台**
   - 按 F12 打开开发者工具
   - 查看 Console 标签页的错误信息

3. **检查后端服务状态**
   - 访问: http://localhost:8000/docs
   - 测试 `/api/report/generate` 接口

4. **检查 .env 文件**
   - 确保没有多余空格
   - 确保 API Key 正确复制
   - 确保文件编码为 UTF-8

---

**更新时间：** 2026年1月2日  
**版本：** v1.0
