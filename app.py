import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI Agent 故障工单生成器",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Agent 故障工单生成器")
st.caption("一个面向 AI 应用开发岗位的线上 Demo：自然语言故障描述 → 结构化工单")

st.markdown("""
这个小应用模拟 AI Agent 在运维/技术支持场景中的工作流：
- 识别故障类型
- 判断优先级
- 推荐负责人
- 输出初步排查建议
- 生成结构化工单
""")

examples = {
    "请选择一个示例": "",
    "登录验证码异常": "学生端登录失败，部分用户反馈验证码收不到，影响多个用户。",
    "支付订单异常": "用户反馈购买课程时支付成功但订单没有生成，客服收到多条反馈。",
    "页面加载缓慢": "学习中心页面加载很慢，部分图片和课程列表一直刷不出来。",
    "模糊故障描述": "系统好像坏了，用户说打不开。"
}

selected = st.selectbox("快速选择测试用例：", list(examples.keys()))
default_text = examples[selected]

user_input = st.text_area(
    "请输入故障描述：",
    value=default_text,
    height=130,
    placeholder="例如：学生端登录失败，部分用户反馈验证码收不到。"
)

def generate_ticket(text: str) -> dict:
    text = text.strip()
    lower_text = text.lower()

    priority_score = 0
    issue_type = "通用系统问题"
    owner = "技术支持 / 运维负责人"
    suggestions = [
        "补充故障发生时间、影响范围和复现步骤",
        "查看系统日志、接口状态和监控指标",
        "确认是否存在近期发布、配置变更或第三方服务异常"
    ]

    if any(word in text for word in ["登录", "验证码", "认证", "密码"]):
        issue_type = "登录 / 认证问题"
        owner = "后端 / 认证服务负责人"
        priority_score += 2
        suggestions = [
            "检查登录服务、认证接口和验证码服务状态",
            "查看短信服务商或邮件服务商接口返回日志",
            "排查是否存在权限、频控、配置或缓存异常"
        ]

    if any(word in text for word in ["支付", "订单", "扣款", "购买", "交易"]):
        issue_type = "支付 / 订单问题"
        owner = "支付系统 / 订单服务负责人"
        priority_score += 3
        suggestions = [
            "检查支付回调接口与订单状态流转日志",
            "核对第三方支付服务返回码和超时情况",
            "排查是否存在重复扣款、订单未生成或消息队列积压"
        ]

    if any(word in text for word in ["页面", "加载", "卡顿", "图片", "打不开"]):
        issue_type = "前端 / 性能问题"
        owner = "前端负责人 / Web 服务负责人"
        priority_score += 1
        suggestions = [
            "检查页面资源加载情况和浏览器控制台报错",
            "查看接口响应时间、CDN 状态和静态资源是否异常",
            "确认问题是否集中在特定页面、浏览器或网络环境"
        ]

    if any(word in text for word in ["多个用户", "大量", "全量", "全部", "很多", "多条反馈"]):
        priority_score += 2

    if any(word in text for word in ["无法", "失败", "异常", "打不开", "收不到"]):
        priority_score += 1

    if priority_score >= 4:
        priority = "P1 - 高优先级"
    elif priority_score >= 2:
        priority = "P2 - 中优先级"
    else:
        priority = "P3 - 低优先级"

    summary = text[:35] + "..." if len(text) > 35 else text

    return {
        "工单编号": "INC-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "故障摘要": summary,
        "故障类型": issue_type,
        "优先级": priority,
        "建议负责人": owner,
        "初步排查建议": suggestions,
        "后续优化方向": [
            "接入大模型 API，提升自然语言信息抽取能力",
            "接入知识库 RAG，基于内部文档生成排查方案",
            "保存历史工单，用于 badcase 复盘和回归测试"
        ]
    }

if st.button("生成结构化工单", type="primary"):
    if not user_input.strip():
        st.warning("请先输入故障描述。")
    else:
        result = generate_ticket(user_input)

        st.subheader("📋 结构化工单")
        st.write(f"**工单编号：** {result['工单编号']}")
        st.write(f"**故障摘要：** {result['故障摘要']}")
        st.write(f"**故障类型：** {result['故障类型']}")
        st.write(f"**优先级：** {result['优先级']}")
        st.write(f"**建议负责人：** {result['建议负责人']}")

        st.markdown("**初步排查建议：**")
        for i, item in enumerate(result["初步排查建议"], 1):
            st.write(f"{i}. {item}")

        with st.expander("项目后续优化方向"):
            for i, item in enumerate(result["后续优化方向"], 1):
                st.write(f"{i}. {item}")

st.divider()
st.caption("Tech Stack: Python · Streamlit · Rule-based Workflow · AI Agent Prototype · Testing / Badcase Design")
