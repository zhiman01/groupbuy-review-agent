"""团购复盘诊断助手工具 - 调用扣子平台已发布的 groupbuy_review_agent 工作流"""

import json
import os
import logging

import requests
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context, default_headers

logger = logging.getLogger(__name__)

WORKFLOW_ID = "7670716918810443818"


def _call_groupbuy_review_workflow(user_input: str, conversation_name: str = "Default") -> str:
    """调用 groupbuy_review_agent 工作流的公共逻辑"""
    ctx = request_context.get() or new_context(method="groupbuy_review")

    coze_api_token = os.environ.get("COZE_WORKLOAD_API_TOKEN", "")
    coze_api_base = os.environ.get("COZE_API_BASE_URL", "https://api.coze.cn")

    headers = {
        "Authorization": f"Bearer {coze_api_token}",
        "Content-Type": "application/json",
    }
    # 注入自定义请求头
    extra_headers = default_headers(ctx) if ctx else {}
    headers.update(extra_headers)

    # 支持环境变量中的额外 headers
    for pair in os.environ.get("COZE_EXTRA_HEADERS", "").split(";"):
        pair = pair.strip()
        if "=" in pair:
            k, v = pair.split("=", 1)
            headers[k.strip()] = v.strip()

    payload = {
        "workflow_id": WORKFLOW_ID,
        "parameters": {
            "USER_INPUT": user_input,
            "CONVERSATION_NAME": conversation_name,
        },
    }

    logger.info("Calling groupbuy_review_agent workflow: %s, conversation: %s", WORKFLOW_ID, conversation_name)

    response = requests.post(
        f"{coze_api_base}/v1/workflow/run",
        headers=headers,
        json=payload,
        timeout=300,
    )

    result = response.json()
    logger.info("Workflow response code: %s", result.get("code"))

    if result.get("code") != 0:
        error_msg = result.get("msg", "Unknown error")
        logger.error("Workflow call failed: %s", error_msg)
        return f"调用团购复盘助手失败: {error_msg}"

    # 提取输出
    output_data = result.get("data", "")
    if isinstance(output_data, str):
        try:
            output_json = json.loads(output_data)
            return output_json.get("output", output_data)
        except (json.JSONDecodeError, TypeError):
            return output_data
    elif isinstance(output_data, dict):
        return output_data.get("output", json.dumps(output_data, ensure_ascii=False))
    else:
        return str(output_data)


@tool
def groupbuy_review(user_input: str, conversation_name: str = "Default") -> str:
    """调用团购复盘诊断助手，对商家团购经营问题进行诊断分析。
    输入用户关于某家商家团购问题的提问（如核销率、曝光量、转化率、差评等），
    助手会判断信息是否充分，必要时追问，最终输出【运营内部分析】与【商家沟通话术】。
    conversation_name 用于绑定会话上下文，同一商家的多轮对话应使用相同的 conversation_name。
    """
    return _call_groupbuy_review_workflow(user_input, conversation_name)
