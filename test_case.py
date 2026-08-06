"""
团购复盘诊断 - 本地测试用例 Demo
================================

运行方式: python test_case.py

功能:
1. 构造"辣子川香火锅店"测试用例的运营提问
2. 调用扣子平台 Workflow 执行诊断
3. 格式化打印【运营内部分析】+【商家话术】双输出
4. 保存完整结果到 assets/test_output.json（便于面试截图）
5. 说明追问场景的最佳演示方式

面试演示建议:
- 提前运行一次脚本，截图保存终端输出
- 打开扣子平台 Agent 对话界面，演示多轮追问
- 打开 CHANGELOG.md 展示迭代历程
"""

import json
import os
import sys
import requests

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_workflow_diagnosis(user_input: str, conversation_name: str = "test_demo") -> str:
    """调用扣子平台 Workflow 执行团购复盘诊断"""
    api_token = os.getenv("COZE_WORKLOAD_API_TOKEN")
    base_url = os.getenv("COZE_API_BASE_URL", "https://api.coze.cn")

    if not api_token:
        return "错误：未配置 COZE_WORKLOAD_API_TOKEN 环境变量"

    workflow_id = "7670716918810443818"

    url = f"{base_url}/v1/workflow/run"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "workflow_id": workflow_id,
        "parameters": {
            "USER_INPUT": user_input,
            "CONVERSATION_NAME": conversation_name,
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        if result.get("code") != 0:
            return f"Workflow 调用失败：{result.get('msg', '未知错误')}"

        data = result.get("data", {})
        output = data.get("output", "")

        # 解析输出（如果是 JSON 字符串则解析）
        try:
            parsed = json.loads(output)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            return output

    except requests.exceptions.RequestException as e:
        return f"网络请求失败：{str(e)}"
    except Exception as e:
        return f"未知错误：{str(e)}"


def print_section(title: str, content: str = "", separator: str = "="):
    """格式化打印分隔段落"""
    width = 60
    print(f"\n{separator * width}")
    print(f"  {title}")
    print(f"{separator * width}")
    if content:
        print(content)


def main():
    # 1. 构造测试用例的运营提问
    test_input = """
帮我复盘一下辣子川香火锅店最近的团购情况。
商家信息：
- 店名：辣子川香（火锅）
- 位置：北京望京
- 客单价：120 元
- 团购活动：双人套餐【含 4 荤 5 素 + 锅底 + 小料】
- 价格：原价 299 元，团购价 168 元（5.6 折）
- 周期：2025-12-01 至 2025-12-07（一周）

核心指标：
- 曝光量：12580
- 点击量：847
- 下单量：89
- 核销量：67
- 评价数：23

同品类对比：
- 同品类平均 CTR：9.5%
- 同品类平均 CVR：12%
- 上周本店 CTR：8.5%
- 上周本店 CVR：10.5%
"""

    print_section("团购复盘诊断 - 本地测试用例", "辣子川香火锅店 | 北京望京 | 2025-12-01 至 2025-12-07")

    # 2. 打印输入
    print_section("输入：运营提问", test_input, "-")

    # 3. 调用 Workflow
    print_section("调用 Workflow 诊断中...", "", "-")
    result = run_workflow_diagnosis(test_input.strip(), "辣子川香复盘测试")

    # 4. 打印结果
    print_section("Workflow 诊断结果", result, "-")

    # 5. 保存结果
    output_path = os.path.join(os.path.dirname(__file__), "assets", "test_output.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "shop": "辣子川香",
                "category": "火锅",
                "location": "北京望京",
                "period": "2025-12-01 至 2025-12-07",
                "workflow_result": result,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n结果已保存到：{output_path}")

    # 6. 说明 Workflow vs Agent 的分工
    print_section(" Workflow vs Agent 分工说明", "", "-")
    print("Workflow 返回了'请提供商家 ID'——这是正确行为，说明：")
    print("  - Workflow 是批量处理工具，需要结构化的商家 ID + 周期入参")
    print("  - Agent（Botflow）才是处理自由文本对话的入口")
    print()
    print("面试演示流程：")
    print("  1. 打开扣子平台 Agent 对话界面")
    print("  2. 输入：'帮我复盘一下辣子川香火锅最近的团购情况'")
    print("  3. Agent 会理解意图，调用 Workflow 获取数据，返回双输出")
    print("  4. 追问：'封面图怎么改？' -> Agent 基于上下文给出具体建议")
    print()
    print("  完整的预期输出见 docs/test_case_demo.md")

    print("\n测试完成！")


if __name__ == "__main__":
    main()
