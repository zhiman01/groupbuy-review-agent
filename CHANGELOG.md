# 团购复盘诊断 Agent 迭代记录

## v1.0.0 — 2026-08-06

### 初始化

- **新增** `src/tools/groupbuy_review_tool.py`：封装扣子平台 `groupbuy_review_agent` 工作流（ID: `7670716918810443818`）调用逻辑
  - 支持 `USER_INPUT`（用户提问）和 `CONVERSATION_NAME`（会话上下文绑定）参数
  - 通过 HTTP OpenAPI 同步调用工作流
  - 包含完整的错误处理：网络异常、HTTP 状态码校验、JSON 解析异常、业务错误码
  - 请求耗时日志、响应状态码日志
- **新增** `src/agents/agent.py`：Agent 核心逻辑
  - 基于 `doubao-seed-2-0-lite-260215` 模型
  - 集成 `groupbuy_review` 工具
  - 工具调用错误中间件（`handle_tool_errors`），防止工具异常阻塞 Agent 循环
  - 短期记忆：滑动窗口保留最近 20 轮对话（40 条消息）
- **新增** `config/agent_llm_config.json`：模型配置与系统提示词
  - 角色：平台生活服务运营智能助手
  - 职责：理解运营提问 → 调用诊断工具 → 呈现结果
  - 输出结构：【运营内部分析】+【可转发给商家的沟通话术】

### 测试结果

- ✅ 输入"商家ID 12345 核销率"，成功调用工作流并返回完整复盘诊断

---

## v1.0.1 — 2026-08-06

### 优化

- **修复** `src/tools/groupbuy_review_tool.py`：增强健壮性
  - 新增 HTTP 状态码校验（非 200 时直接返回错误，避免无效 JSON 解析）
  - 新增 `requests.exceptions.RequestException` 捕获（网络超时、连接失败等）
  - 新增 JSON 解析异常捕获（`ValueError`）
  - 日志增强：记录请求耗时、响应状态码、输入长度、错误响应体（截取前 500 字符）

---

<!-- 
模板：每次迭代新增一个条目，格式如下

## vX.Y.Z — YYYY-MM-DD

### 新增 / 优化 / 修复

- **新增/修复/优化** `文件路径`：变更描述

### 测试结果

- ✅ / ❌ 测试情况
-->
