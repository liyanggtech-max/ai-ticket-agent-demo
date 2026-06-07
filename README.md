# AI Agent Incident Ticket Generator

这是一个 AI 应用开发 Demo。  
应用场景是：将用户自然语言描述的系统故障，自动整理成结构化运维工单。

## 功能

- 输入自然语言故障描述
- 自动识别故障类型
- 自动判断优先级
- 推荐负责人
- 输出初步排查建议
- 提供典型测试用例

## 技术栈

- Python
- Streamlit
- Rule-based Workflow
- AI Agent Prototype Design
- Testing / Badcase Analysis

## 项目亮点

这个项目不是底层大模型训练，而是偏 AI 应用落地。  
它模拟了 AI Agent 在技术支持和运维场景中的应用流程：

1. 用户输入故障描述
2. 系统抽取关键信息
3. 规则逻辑判断故障类别和优先级
4. 输出结构化工单和排查建议

## 后续优化方向

- 接入 DeepSeek / OpenAI API
- 增加 RAG 知识库检索
- 保存历史工单
- 加入 badcase 复盘表
- 增加日志、监控和异常告警
